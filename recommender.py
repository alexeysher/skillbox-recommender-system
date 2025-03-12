import sys
import subprocess
import time
from os import PathLike

import numpy as np
import pandas as pd
import functions as f
import tempfile
import pathlib
import pickle


class Recommender:
    """
    Recommendation model for online grocery hypermarket.
    Filters products by:
    - frequency
    - time
    - add to cart order
    - popularity.

    Fills in missing recommendations with the most popular products among the other users.
    """
    __days_rate_points = np.linspace(0.0, 0.1, 21)
    __days_rate_degree = 7
    __cart_rate_points = np.linspace(0.0, 0.05, 21)
    __cart_rate_degree = 3
    __total_rate_points = np.linspace(0.0, 1.0, 21)
    __total_rate_degree = 3

    def __init__(self):
        self.__days_rate = 0.
        self.__days_map10 = 0.
        self.__cart_rate = 0.
        self.__cart_map10 = 0.
        self.__total_rate = 0.
        self.__total_map10 = 0.
        self.__weights = pd.DataFrame()
        self.__ratings = pd.DataFrame()
        self.__products = pd.DataFrame()
        self.__aisle_ranks = pd.DataFrame()
        self.__inside_aisle_ranks = pd.DataFrame()
        self.__tmpdir = ''
        self.__workers = 0
        self.__user_ids = []
        self.__fitted = False

    @staticmethod
    def __check_fitted(func):
        def wrapper(self, *args, **kwargs):
            assert self.__fitted, 'Model is not fitted. Please fit model first.'
            result = func(self, *args, **kwargs)
            return result

        return wrapper

    def __multiprocessing(self, points: np.array, func: str):
        """
        Runs the parallel computing script multiproc.py with the required parameters.
        :param points: filter rate values.
        :param func: MAP@10 calculation function.
        :return: MAP@10 values dataframe.
        """

        cmd = f'{sys.executable} multiproc.py --workers={self.__workers} --data_path={self.__tmpdir} ' \
              f'--start={points[0]} --stop={points[-1]} --num={len(points)} --func={func} ' \
              f'--days_rate={self.__days_rate} --cart_rate={self.__cart_rate}'
        subprocess.run(cmd)
        with open(f'{self.__tmpdir}/precisions.pkl', 'rb') as fp:
            # noinspection PyTypeChecker
            map10 = pickle.load(fp)
        return map10

    def __search_optimal_days_rate(self, prior_transactions: pd.DataFrame, last_products: [int]):
        """
        Searches for the optimal value of the filtration rate over time.
        """
        
        self.__days_rate_map10 = self.__multiprocessing(self.__days_rate_points, 'get_map10_by_days_rates')
        print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: '
              f'`days_rates` points: {self.__days_rate_map10}')
        self.__days_rate_map10_predicted, self.__days_rate = \
            f.approximate_precision_by_rate(self.__days_rate_points, self.__days_rate_map10, self.__days_rate_degree)
        self.__days_map10 = f.get_prediction_precision(
            last_products, f.get_prediction(
                f.get_ratings(
                    f.get_weights(
                        prior_transactions, self.__days_rate))))
        print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: '
              f'optimal `days_rate` value found: {self.__days_rate:.5f}, MAP@10={self.__days_map10:.5f}')

    def __search_optimal_cart_rate(self, prior_transactions: pd.DataFrame, last_products: [int]):
        """
        Searches for the optimal value of the filter rate by the number of adding a product to the cart.
        """
        
        self.__cart_rate_map10 = self.__multiprocessing(self.__cart_rate_points, 'get_map10_by_cart_rates')
        print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: '
              f'`cart_rates` points: {self.__cart_rate_map10}')
        self.__cart_rate_map10_predicted, self.__cart_rate = \
            f.approximate_precision_by_rate(self.__cart_rate_points, self.__cart_rate_map10, self.__cart_rate_degree)
        self.__cart_map10 = f.get_prediction_precision(
            last_products, f.get_prediction(
                f.get_ratings(
                    f.get_weights(
                        prior_transactions, self.__days_rate, self.__cart_rate))))
        print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: '
              f'optimal `cart_rate` value found: {self.__cart_rate:.5f}, MAP@10={self.__cart_map10:.5f}')

    def __search_optimal_total_rate(self, prior_transactions: pd.DataFrame, last_products: [int]):
        """
        Searches for the optimal value of the filter rate by popularity.
        """
        
        self.__total_rate_map10 = self.__multiprocessing(self.__total_rate_points, 'get_map10_by_total_rates')
        print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: '
              f'`total_rate` points: {self.__total_rate_map10}')
        self.__total_rate_map10_predicted, self.__total_rate = \
            f.approximate_precision_by_rate(self.__total_rate_points, self.__total_rate_map10, self.__total_rate_degree)
        self.__total_map10 = f.get_prediction_precision(
            last_products, f.get_prediction(
                f.get_ratings(f.get_weights(
                    prior_transactions, self.__days_rate, self.__cart_rate),
                    self.__total_rate)))
        print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: '
              f'optimal `total_rate` value found: {self.__total_rate:.5f}, MAP@10={self.__total_map10:.5f}')

    def fit(self, products: pd.DataFrame, transactions: pd.DataFrame, workers: int = 4):
        """
        Computes optimal rates for filtering.
        :var products: Products registry.
        :var transactions: Transactions log.
        """

        print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: fitting...')
        self.__products = products
        prior_transactions, last_transactions, last_products = f.preprocess_transactions(transactions)
        transactions = prior_transactions.copy()
        transactions['days_before_last_order'] += transactions['days_before_last_order_shift']
        transactions = pd.concat([transactions, last_transactions])
        self.__workers = workers

        with tempfile.TemporaryDirectory() as tmpdir:
            self.__tmpdir = pathlib.Path(tmpdir)
            with open(self.__tmpdir / 'prior_transactions.pkl', 'wb') as fp:
                # noinspection PyTypeChecker
                pickle.dump(prior_transactions, fp)
            with open(self.__tmpdir / 'last_products.pkl', 'wb') as fp:
                # noinspection PyTypeChecker
                pickle.dump(last_products, fp)
            self.__search_optimal_days_rate(prior_transactions, last_products)
            self.__search_optimal_cart_rate(prior_transactions, last_products)
            self.__search_optimal_total_rate(prior_transactions, last_products)


        self.__weights = f.get_weights(transactions, self.__days_rate, self.__cart_rate)
        print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: weights calculated.')
        self.__ratings = f.get_ratings(self.__weights, self.__total_rate)
        print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: ratings compiled.')
        self.__aisle_ranks = f.get_aisle_ranks(self.__ratings, self.__products)
        print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: aisles ranked.')
        self.__inside_aisle_ranks = f.get_inside_aisle_ranks(self.__ratings, self.__products)
        print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: products inside aisles ranked.')
        print('-----------------------------------------------------------------')

        self.__user_ids = self.__ratings['user_id'].unique().tolist()

        self.__fitted = True

    def load(self, path: str | PathLike):
        """
        Loads model state from files in specified directory.
        :param path: Path to model directory.
        :return:
        """
        if isinstance(path, str):
            path = pathlib.Path(path)

        file_path = path / 'days.pkl'
        with open(file_path, 'rb') as fp:
            self.__days_rate, self.__days_map10 = pickle.load(fp)

        file_path = path / 'cart.pkl'
        with open(file_path, 'rb') as fp:
            self.__cart_rate, self.__cart_map10 = pickle.load(fp)

        file_path = path / 'total.pkl'
        with open(file_path, 'rb') as fp:
            self.__total_rate, self.__total_map10 = pickle.load(fp)

        file_path = path / 'weights.zip'
        self.__weights = pd.read_pickle(file_path)

        file_path = path / 'ratings.zip'
        self.__ratings = pd.read_pickle(file_path)

        file_path = path / 'aisle_ranks.zip'
        self.__aisle_ranks = pd.read_pickle(file_path)

        file_path = path / 'inside_aisle_ranks.zip'
        self.__inside_aisle_ranks = pd.read_pickle(file_path)

        file_path = path / 'products.zip'
        self.__products = pd.read_pickle(file_path)

        self.__user_ids = self.__ratings['user_id'].unique().tolist()

        self.__fitted = True

    @__check_fitted
    def save(self, path: str | PathLike):
        """
        Saves model state to files in specified directory.
        :param path: Path to model directory.
        """

        if isinstance(path, str):
            path = pathlib.Path(path)
        path.mkdir(exist_ok=True)

        file_path = path / 'days.pkl'
        with open(file_path, 'wb') as fp:
            # noinspection PyTypeChecker
            pickle.dump((self.__days_rate, self.__days_map10), fp)

        file_path = path / 'cart.pkl'
        with open(file_path, 'wb') as fp:
            # noinspection PyTypeChecker
            pickle.dump((self.__cart_rate, self.__cart_map10), fp)

        file_path = path / 'total.pkl'
        with open(file_path, 'wb') as fp:
            # noinspection PyTypeChecker
            pickle.dump((self.__total_rate, self.__total_map10), fp)

        file_path = path / 'weights.zip'
        self.__weights.to_pickle(file_path)

        file_path = path / 'ratings.zip'
        self.__ratings.to_pickle(file_path)

        file_path = path / 'aisle_ranks.zip'
        self.__aisle_ranks.to_pickle(file_path)

        file_path = path / 'inside_aisle_ranks.zip'
        self.__inside_aisle_ranks.to_pickle(file_path)

        file_path = path / 'products.zip'
        self.__products.to_pickle(file_path)

    @__check_fitted
    def recommend(self, user_id: int | list[int] | None = None, k: int = 10) -> (pd.DataFrame, float):
        """
        Generates recommendations for a single/multiple/all users.
        :param user_id: ID of users to get recommendation:
        - `int` - for single user
        - list of `int` - for multiple users
        - `None` - for all users
        :param k: Size of recommendations.
        :return: Recommendation as `pandas.Dataframe`.
        """
        if isinstance(user_id, list):
            if len(user_id) == 0:
                user_id = None

        if user_id is None:
            ratings = self.__ratings
            print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: '
                  f'predicting {k} products for all users...')
        elif isinstance(user_id, int):
            ratings = self.__ratings.loc[self.__ratings['user_id'] == user_id]
            print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: '
                  f'predicting {k} products for user with {user_id} ID...')
        elif isinstance(user_id, list):
            ratings = self.__ratings.loc[self.__ratings['user_id'].isin(user_id)]
            print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: '
                  f'predicting {k} products for ({len(user_id)}) users...')
        else:
            raise TypeError()

        prediction = f.get_prediction_table(f.fill_up_prediction(
            f.get_prediction(ratings, k=k),
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

    @__check_fitted
    def get_rate(self, filtering):
        """
        Returns the filtering rate.
        :param filtering: Filtering name:
        - ``days``- by time.
        - ``cart`` - by product addition number to cart.
        - ``total`` - by popularity.
        :return: filtering rate.
        """

        match filtering:
            case 'days':
                return self.__days_rate
            case 'days':
                return self.__cart_rate
            case 'days':
                return self.__total_rate
            case _:
                raise ValueError()

    @__check_fitted
    def get_eval_map10(self, filtering):
        """
        Returns the MAP@10 for filtering.
        :param filtering: Filtering name:
        - ``days``- by time.
        - ``cart`` - by product addition number to cart.
        - ``total`` - by popularity.
        :return: filtering rate.
        """

        match filtering:
            case 'days':
                return self.__days_map10
            case 'days':
                return self.__cart_map10
            case 'days':
                return self.__total_map10
            case _:
                raise ValueError()

    @property
    @__check_fitted
    def users(self) -> [int]:
        """
        List of User IDs.
        """

        return self.__user_ids

