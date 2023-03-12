import sys
import subprocess
import time
import numpy as np
import pandas as pd
import functions as f
from tempfile import TemporaryDirectory
from pathlib import Path
from pickle import dump, load


class Recommender:
    """
    Модель рекомендаций.
    """
    __prior_transactions = None
    __last_transactions = None
    __last_products = None
    __days_rate = None
    __days_map10 = None
    __days_rate_points = np.linspace(0.0, 0.1, 21)
    __days_rate_degree = 7
    __cart_rate = None
    __cart_map10 = None
    __cart_rate_points = np.linspace(0.0, 0.05, 21)
    __cart_rate_degree = 3
    __total_rate = None
    __total_map10 = None
    __total_rate_points = np.linspace(0.0, 1.0, 21)
    __total_rate_degree = 3
    __weights = None
    __ratings = None
    __products = None
    __aisle_ranks = None
    __inside_aisle_ranks = None
    __workers = None
    __tmpdir = None

    def __init__(self, transactions: pd.DataFrame = None, products: pd.DataFrame = None,
                 days_rate: float = None, cart_rate: float = None, total_rate: float = None, workers: int = 4):
        """
        Инициализация.
        :param transactions: журнал транзакций.
        :param products: справочник продуктов.
        :param days_rate: коэффициент фильтрации по времени.
        :param cart_rate:  коэффициент фильтрации по номеру добавления продукта в корзину.
        :param total_rate:  коэффициент фильтрации по популярности.
        :param workers: количество процессов параллельных вычислений.
        """
        print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: initializing...')
        self.append_transactions(transactions)
        self.append_products(products)
        self.__days_rate = days_rate
        self.__cart_rate = cart_rate
        self.__total_rate = total_rate
        self.__workers = workers
        print('-----------------------------------------------------------------')

    def __multiprocessing(self, points: np.array, func: str):
        """
        Запускает скрипт параллельных вычислений multiproc.py с требуемыми параметрами.
        :param points: значения коэффициента фильтрации.
        :param func: функция вычисления MAP@10.
        :return: датафрейм значений MAP@10.
        """
        cmd = f'{sys.executable} multiproc.py --workers={self.__workers} --data_path={self.__tmpdir} ' \
              f'--start={points[0]} --stop={points[-1]} --num={len(points)} --func={func} ' \
              f'--days_rate={self.__days_rate} --cart_rate={self.__cart_rate}'
        subprocess.run(cmd)
        with open(self.__tmpdir / 'precisions.dmp', 'rb') as fp:
            map10 = load(fp)
        return map10

    def __search_optimal_days_rate(self):
        """
        Поиск оптимального значения коэффициента фильтрации по времени.
        """
        self.__days_rate_map10 = self.__multiprocessing(self.__days_rate_points, 'get_map10_by_days_rates')
        print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: '
              f'`days_rates` points: {self.__days_rate_map10}')
        self.__days_rate_map10_predicted, self.__days_rate = \
            f.approximate_precision_by_rate(self.__days_rate_points, self.__days_rate_map10, self.__days_rate_degree)
        self.__days_map10 = f.get_prediction_precision(
            self.__last_products, f.get_prediction(
                f.get_ratings(
                    f.get_weights(
                        self.__prior_transactions, self.__days_rate))))
        print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: '
              f'optimal `days_rate` value found: {self.__days_rate:.5f}, MAP@10={self.__days_map10:.5f}')

    def __search_optimal_cart_rate(self):
        """
        Поиск оптимального значения коэффициента фильтрации по номеру добавления продукта в корзину.
        """
        self.__cart_rate_map10 = self.__multiprocessing(self.__cart_rate_points, 'get_map10_by_cart_rates')
        print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: '
              f'`cart_rates` points: {self.__cart_rate_map10}')
        self.__cart_rate_map10_predicted, self.__cart_rate = \
            f.approximate_precision_by_rate(self.__cart_rate_points, self.__cart_rate_map10, self.__cart_rate_degree)
        self.__cart_map10 = f.get_prediction_precision(
            self.__last_products, f.get_prediction(
                f.get_ratings(
                    f.get_weights(
                        self.__prior_transactions, self.__days_rate, self.__cart_rate))))
        print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: '
              f'optimal `cart_rate` value found: {self.__cart_rate:.5f}, MAP@10={self.__cart_map10:.5f}')

    def __search_optimal_total_rate(self):
        """
        Поиск оптимального значения коэффициента фильтрации по популярности.
        """
        self.__total_rate_map10 = self.__multiprocessing(self.__total_rate_points, 'get_map10_by_total_rates')
        print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: '
              f'`total_rate` points: {self.__total_rate_map10}')
        self.__total_rate_map10_predicted, self.__total_rate = \
            f.approximate_precision_by_rate(self.__total_rate_points, self.__total_rate_map10, self.__total_rate_degree)
        self.__total_map10 = f.get_prediction_precision(
            self.__last_products, f.get_prediction(
                f.get_ratings(f.get_weights(
                    self.__prior_transactions, self.__days_rate, self.__cart_rate),
                    self.__total_rate)))
        print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: '
              f'optimal `total_rate` value found: {self.__total_rate:.5f}, MAP@10={self.__total_map10:.5f}')

    def build(self):
        """
        Обучение модели.
        """

        print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: building...')
        if (self.__prior_transactions is None) or (self.__last_transactions is None) or (self.__products is None):
            return

        with TemporaryDirectory() as tmpdir:
            self.__tmpdir = Path(tmpdir)
            with open(self.__tmpdir / 'prior_transactions.dmp', 'wb') as fp:
                dump(self.__prior_transactions, fp)
            with open(self.__tmpdir / 'last_products.dmp', 'wb') as fp:
                dump(self.__last_products, fp)
            self.__search_optimal_days_rate()
            self.__search_optimal_cart_rate()
            self.__search_optimal_total_rate()

        transactions = self.__prior_transactions.copy()
        transactions['days_before_last_order'] += transactions['days_before_last_order_shift']
        transactions = pd.concat([transactions, self.__last_transactions])
        self.__weights = f.get_weights(transactions, self.__days_rate, self.__cart_rate)
        print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: weights calculated.')
        self.__ratings = f.get_ratings(self.__weights, self.__total_rate)
        print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: ratings compiled.')
        self.__aisle_ranks = f.get_aisle_ranks(self.__ratings, self.__products)
        print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: aisles ranked.')
        self.__inside_aisle_ranks = f.get_inside_aisle_ranks(self.__ratings, self.__products)
        print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: products inside aisles ranked.')
        print('-----------------------------------------------------------------')

    def get_recommendation(self, k: int = 10) -> (pd.DataFrame, float):
        """
        Формирование рекомендаций для всех пользователей.
        :param k: размер рекомендаций.
        :return: датафрейм рекомендаций.
        """

        print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: predicting {k} products...')
        prediction = f.get_prediction_table(f.fill_up_prediction(f.get_prediction(self.__ratings, k),
                                                                 self.__aisle_ranks, self.__inside_aisle_ranks, k))
        prediction.reset_index(inplace=True)
        for column in range(1, k + 1):
            prediction = prediction.merge(
                self.__products[['product_id', 'product_name']],
                left_on=column,
                right_on='product_id'
            ).drop(columns=[column, 'product_id']).rename(columns={'product_name': f'product_#{column}'})
        prediction.sort_values('user_id', inplace=True)
        prediction.set_index('user_id', inplace=True)
        print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: prediction compiled.')
        print('-----------------------------------------------------------------')
        return prediction

    def get_user_recommendation(self, user_id: int, k: int) -> (pd.DataFrame, float):
        """
        Формирование рекомендаций для отдельного пользователя.
        :param user_id: ИН пользователя.
        :param k: размер рекомендаций.
        :return: датафрейм рекомендаций.
        """

        print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: '
              f'predicting {k} products for user `{user_id}`...')
        prediction = f.get_prediction_table(f.fill_up_prediction(
            f.get_prediction(self.__ratings.loc[self.__ratings['user_id'] == user_id], k=k),
            self.__aisle_ranks, self.__inside_aisle_ranks, k))
        prediction.reset_index(inplace=True)
        for column in range(1, k + 1):
            prediction = prediction.merge(
                self.__products[['product_id', 'product_name']],
                left_on=column,
                right_on='product_id'
            ).drop(columns=[column, 'product_id']).rename(columns={'product_name': f'product_#{column}'})
        prediction.sort_values('user_id', inplace=True)
        prediction.set_index('user_id', inplace=True)
        print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: prediction compiled.')
        print('-----------------------------------------------------------------')
        return prediction

    def append_transactions(self, transactions: pd.DataFrame):
        """
        Добавление транзакций в журнал.
        :param transactions: датафрейм добавлений.
        """
        if transactions is None:
            return
        print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: '
              f'{transactions.shape[0]} transactions appending...')
        if (self.__prior_transactions is not None) and (self.__last_transactions is not None):
            self.__prior_transactions['days_before_last_order'] += \
                self.__prior_transactions['days_before_last_order_shift']
            transactions = pd.concat([self.__prior_transactions, self.__last_transactions, transactions]) \
                .drop(columns=['days_before_last_order', 'days_before_last_order_shift']) \
                .drop_duplicates(['user_id', 'order_number', 'product_id'], keep='last') \
                .reset_index(drop=True)
        self.__prior_transactions, self.__last_transactions, self.__last_products \
            = f.preprocess_transactions(transactions)
        print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: '
              f'transactions appended: {transactions.shape[0]} total.')
        print('-----------------------------------------------------------------')

    def append_products(self, products: pd.DataFrame):
        """
        Добавление/замена продуктов в справочнике.
        :param products: датафрейм замен/добавлений.
        """
        if products is None:
            return
        if self.__products is None:
            self.__products = products
        else:
            print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: '
                  f'{products.shape[0]} products appending...')
            self.__products = pd.concat([self.__products, products]) \
                .drop_duplicates('product_id', keep='last') \
                .reset_index(drop=True)
        print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: '
              f'products appended: {self.__products.shape[0]} total.')
        print('-----------------------------------------------------------------')

    def get_rate(self, filtering):
        """
        Возвращает коэффициент фильтрации.
        :param filtering: название фильтрации:
        - ``days``- по времени.
        - ``cart`` - по номеру добавления продукта в корзину.
        - ``total`` - по популярности.
        :return: коэффициент фильтрации.
        """
        if filtering == 'days':
            return self.__days_rate, self.__days_map10
        elif filtering == 'cart':
            return self.__cart_rate, self.__cart_map10
        elif filtering == 'total':
            return self.__total_rate, self.__total_map10

    def get_map10_by_rate_approximations(self, filtering):
        """
        Возвращает значения функции аппроксимации зависимости MAP@10 от значения коэффициента фильтрации,
        используемой для поиска оптимального значения коэффициента.
        :param filtering: название фильтрации:
        - ``days``- по времени.
        - ``cart`` - по номеру добавления продукта в корзину.
        - ``total`` - по популярности.
        :return: pd.Series значений функции аппроксимации.
        """
        if filtering == 'days':
            return self.__days_rate_points, self.__days_rate_map10, self.__days_rate_map10_predicted
        elif filtering == 'cart':
            return self.__cart_rate_points, self.__cart_rate_map10, self.__cart_rate_map10_predicted
        elif filtering == 'total':
            return self.__total_rate_points, self.__total_rate_map10, self.__total_rate_map10_predicted

    def get_users(self):
        """
        Возвращает список пользователей из журнала транзакций.
        :return: список пользователей.
        """
        return self.__last_transactions['user_id'].unique().tolist()
