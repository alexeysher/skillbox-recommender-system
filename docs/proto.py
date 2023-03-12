import time
from pickle import load
from pathlib import Path
import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import pandas as pd

from recommender import Recommender
from kaggle import Kaggle
from auxilary import set_text_style, InstacartColors

COMPETITION = 'skillbox-recommender-system'  # Название соревнования на платформе Kaggle
DATA_PATH = Path('D:/skillbox-recommender-system/data')  # Путь к папке данных
TRANSACTIONS_PATH = DATA_PATH / 'transactions.csv'  # Путь к файлу логов транзакций
PRODUCTS_PATH = DATA_PATH / 'products.csv'  # Путь к файлу справочника продуктов
WORKERS = 4  # Количество процессов параллельных вычислений
QUARTILES_COMBINATIONS = [[1, 0, 0, 0],
                          [0, 1, 0, 0],
                          [0, 0, 1, 0],
                          [0, 0, 0, 1],
                          [1, 1, 0, 0],
                          [0, 1, 1, 0],
                          [0, 0, 1, 1],
                          [1, 1, 1, 0],
                          [0, 1, 1, 1],
                          [1, 1, 1, 1]]  # Комбинации квартилей транзакций для построения моделей


def prepare_data():
    """
    Подготовка данных:
    - разделение транзакций на квартили
    - списки продуктов в квартилях транзакций
    - обучение моделей на комбинациях квартилей транзакций: 1, 2, 3, 4, 1+2, 2+3, 3+4, 1+2+3, 2+3+4, 1+2+3+4
    """

    from pickle import dump, load
    import time
    from shutil import unpack_archive
    import pandas as pd

    global COMPETITION, TRANSACTIONS_PATH, PRODUCTS_PATH, QUARTILES_COMBINATIONS

    if 'data_prepared' in st.session_state:
        return

    with st.spinner('Подготовка данных...'):
        # Создание папки данных
        if not DATA_PATH.exists():
            DATA_PATH.mkdir()
            print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: '
                  f'data dir created: {DATA_PATH}.')

        # Загрузка данных из соревнования Kaggle
        kaggle = Kaggle(COMPETITION)
        if not TRANSACTIONS_PATH.with_suffix('.dmp').exists():
            if not TRANSACTIONS_PATH.with_suffix('.csv.zip').exists():
                kaggle.download_data_files([TRANSACTIONS_PATH.name], DATA_PATH.as_posix())
                print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: '
                      f'transactions archive downloaded: {TRANSACTIONS_PATH.with_suffix(".csv.zip")}.')
            if TRANSACTIONS_PATH.with_suffix('.csv.zip').exists():
                unpack_archive(TRANSACTIONS_PATH.with_suffix('.csv.zip'), DATA_PATH)
                print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: '
                      f'transactions data extracted: {TRANSACTIONS_PATH}.')
            transactions = pd.read_csv(TRANSACTIONS_PATH)
            file_path = TRANSACTIONS_PATH.with_suffix('.dmp')
            with open(file_path, 'wb') as fp:
                dump(transactions, fp)

        if not PRODUCTS_PATH.with_suffix('.dmp').exists():
            if not PRODUCTS_PATH.with_suffix('.csv.zip').exists():
                kaggle.download_data_files([PRODUCTS_PATH.name], DATA_PATH.as_posix())
                print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: '
                      f'products archive downloaded: {PRODUCTS_PATH.with_suffix(".csv.zip")}.')
            if PRODUCTS_PATH.with_suffix('.csv.zip').exists():
                unpack_archive(PRODUCTS_PATH.with_suffix('.csv.zip'), DATA_PATH)
                print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: '
                      f'products data extracted: {PRODUCTS_PATH}.')
            products = pd.read_csv(PRODUCTS_PATH)
            file_path = PRODUCTS_PATH.with_suffix('.dmp')
            with open(file_path, 'wb') as fp:
                dump(products, fp)

        # Создание квартилей данных
        transactions_quartiles = []
        file_paths = [TRANSACTIONS_PATH.with_name(f'transactions_{index}.dmp') for index in range(1, 5)]
        if all(file_path.exists() for file_path in file_paths):
            for file_path in file_paths:
                with open(file_path, 'rb') as fp:
                    transactions_quartiles.append(load(fp))
            print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: '
                  f'transaction quartiles loaded.')
        else:
            file_path = TRANSACTIONS_PATH.with_suffix('.dmp')
            with open(file_path, 'rb') as fp:
                transactions = load(fp)
            orders = transactions[['user_id', 'order_number']] \
                .groupby(['user_id', 'order_number']).head(1)
            quartile_size = orders.shape[0] // 4
            for index in range(1, 5):
                start_iloc = (index - 1) * quartile_size
                end_iloc = start_iloc + quartile_size if index < 4 else -1
                orders_quartile = orders.iloc[start_iloc: end_iloc]
                transactions_quartile = transactions \
                    .merge(orders_quartile, on=['user_id', 'order_number'], how='right')
                file_path = TRANSACTIONS_PATH.with_name(f'transactions_{index}.dmp')
                with open(file_path, 'wb') as fp:
                    dump(transactions_quartile, fp)
                transactions_quartiles.append(transactions_quartile)
            print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: '
                  f'transaction quartiles saved.')

        file_paths = [PRODUCTS_PATH.with_name(f'products_{index}.dmp') for index in range(1, 5)]
        products_quartiles = []
        if all(file_path.exists() for file_path in file_paths):
            for file_path in file_paths:
                with open(file_path, 'rb') as fp:
                    products_quartiles.append(load(fp))
            print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: '
                  f'product quartiles loaded.')
        else:
            file_path = PRODUCTS_PATH.with_suffix('.dmp')
            with open(file_path, 'rb') as fp:
                products = load(fp)
            for transactions_quartile in transactions_quartiles:
                products_quartile = products.loc[
                    products['product_id'].isin(transactions_quartile['product_id'].unique())]
                products_quartiles.append(products_quartile)
            for index, products_quartile in enumerate(products_quartiles):
                file_path = PRODUCTS_PATH.with_name(f'products_{index + 1}.dmp')
                with open(file_path, 'wb') as fp:
                    dump(products_quartile, fp)
            print(f'{time.strftime("%H:%M:%S", time.localtime(time.time()))}: '
                  f'product quartiles saved.')

        # Создание моделей, обученных на различных комбинациях квартилей
        file_paths = [DATA_PATH / f'recommender_{quartiles_combination}.dmp'
                      for quartiles_combination in QUARTILES_COMBINATIONS]
        if any(not file_path.exists() for file_path in file_paths):
            for quartiles_combination in QUARTILES_COMBINATIONS:
                quartile_index = 3 - quartiles_combination[::-1].index(1)
                if quartiles_combination.count(1) == 1:
                    recommender = Recommender(workers=WORKERS)
                else:
                    prior_quartiles_combination = quartiles_combination.copy()
                    prior_quartiles_combination[quartile_index] = 0
                    file_path = DATA_PATH / f'recommender_{prior_quartiles_combination}.dmp'
                    with open(file_path, 'rb') as fp:
                        recommender = load(fp)
                recommender.append_transactions(transactions_quartiles[quartile_index])
                recommender.append_products(products_quartiles[quartile_index])
                recommender.build()
                file_path = DATA_PATH / f'recommender_{quartiles_combination}.dmp'
                with open(file_path, 'wb') as fp:
                    dump(recommender, fp)

    st.session_state['data_prepared'] = True


@st.cache_resource
def load_model(combination):

    global DATA_PATH

    file_path = DATA_PATH / f'recommender_{combination}.dmp'
    with open(file_path, 'rb') as fp:
        model = load(fp)
    return model


def main():
    # prepare_data()
    quartiles_combination_labels = ["0-25%", "25-50%", "50-75%", "75-100%",
                                    "0-50%", "25-75%", "50-100%",
                                    "0-75%", "25-100%", "0-100%"]
    with st.sidebar:
        quartiles_combination_label = st.radio('Набор данных:', quartiles_combination_labels, horizontal=False)
        quartiles_combination = QUARTILES_COMBINATIONS[quartiles_combination_labels.index(quartiles_combination_label)]

    recommender = load_model(quartiles_combination)
    choice = option_menu('', ['Обучение модели', 'Рекомендации для всех пользователей',
                              'Рекомендации для отдельных пользователей'],
                         icons=['tools', 'people', 'person'],
                         orientation='horizontal',
                         styles={"container": {"padding": "0!important", "background-color": "#fafafa"}}
                         )

    if choice == 'Обучение модели':
        days_rate, days_map10 = recommender.get_rate('days')
        days_rates, days_map10_true, days_map10_predicted = recommender.get_map10_by_rate_approximations('days')
        cart_rate, cart_map10 = recommender.get_rate('cart')
        cart_rates, cart_map10_true, cart_map10_predicted = recommender.get_map10_by_rate_approximations('cart')
        total_rate, total_map10 = recommender.get_rate('total')
        total_rates, total_map10_true, total_map10_predicted = recommender.get_map10_by_rate_approximations('total')
        c1, c2, c3 = st.columns(3, gap='large')
        c1.markdown('**' + set_text_style('Фильтрация по времени покупок',
                                          size=20, align='center') + '**',
                    unsafe_allow_html=True)
        c2.markdown('**' + set_text_style('Фильтрация по номеру добавления продукта в корзину',
                                          size=20, align='center') + '**',
                    unsafe_allow_html=True)
        c3.markdown('**' + set_text_style('Фильтрация по популярности продуктов',
                                          size=20, align='center') + '**',
                    unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3, gap='large')
        c1.latex('r_{u,i}=\sum_{t \in T_u}s_{u,i,t}·e^{-d_{u,t}·a_d}')
        c2.latex('r_{u,i}=\sum_{t \in T_u}s_{u,i,t}·e^{-d_{u,t}·a_d}·e^{-c_{u,i,t}·a_c}')
        c3.latex('r^*_{u,i}=r_{u,i}·e^{\sum_{u \in U}r_{u,i} \over |U|}')

        c1, c2, c3 = st.columns(3, gap='large')
        with c1:
            fig, ax = plt.subplots(facecolor=InstacartColors.Cashew)
            days_map10_true.plot(ax=ax,
                                 # title='Точность предсказаний продуктов в следующей покупке'
                                 #              '\nот коэффициента фильтрации по времени покупок\n',
                                 xlabel='$a_d$', ylabel='$MAP@10$',
                                 grid=True, fontsize=10, legend=False, alpha=0.75)
            ax.plot(days_rates, days_map10_predicted, linestyle='--', color='#ff7f0e', alpha=0.75)
            ax.scatter(days_rate, days_map10, color='#d62728', linewidth=1, alpha=0.75)
            ax.axvline(days_rate, color='#d62728', linestyle='--', linewidth=1, alpha=0.75)
            ax.axhline(days_map10, color='#d62728', linestyle='--', linewidth=1, alpha=0.75)
            _ = ax.legend(['Реальные значения', 'Аппроксимация', 'Пик'])
            st.pyplot(fig)
        with c2:
            fig, ax = plt.subplots(facecolor=InstacartColors.Cashew)
            cart_map10_true.plot(ax=ax,
                                 # title='Точность предсказаний продуктов в следующей покупке\n'
                                 #              'в зависимости от коэффициента фильтрации\n'
                                 #              'по номеру добавления продукта в корзину',
                                 xlabel='$a_c$', ylabel='$MAP@10$',
                                 grid=True, fontsize=10, legend=False, alpha=0.75)
            ax.plot(cart_rates, cart_map10_predicted, linestyle='--', color='#ff7f0e', alpha=0.75)
            ax.scatter(cart_rate, cart_map10, color='#d62728', linewidth=1, alpha=0.75)
            ax.axvline(cart_rate, color='#d62728', linestyle='--', linewidth=1, alpha=0.75)
            ax.axhline(cart_map10, color='#d62728', linestyle='--', linewidth=1, alpha=0.75)
            _ = ax.legend(['Реальные значения', 'Аппроксимация', 'Пик'])
            st.pyplot(fig)
        with c3:
            fig, ax = plt.subplots(facecolor=InstacartColors.Cashew)
            total_map10_true.plot(ax=ax,
                                  # title='Точность предсказаний продуктов в следующей покупке'
                                  #              '\nот коэффициента фильтрации по популярности продуктов\n',
                                  xlabel='$a_p$', ylabel='$MAP@10$',
                                  grid=True, fontsize=10, legend=False, alpha=0.75)
            ax.plot(total_rates, total_map10_predicted, linestyle='--', color='#ff7f0e', alpha=0.75)
            ax.scatter(total_rate, total_map10, color='#d62728', linewidth=1, alpha=0.75)
            ax.axvline(total_rate, color='#d62728', linestyle='--', linewidth=1, alpha=0.75)
            ax.axhline(total_map10, color='#d62728', linestyle='--', linewidth=1, alpha=0.75)
            _ = ax.legend(['Реальные значения', 'Аппроксимация', 'Пик'])
            st.pyplot(fig)

        c1, c2, c3 = st.columns(3, gap='large')
        c1.latex(f'a_d={days_rate:.5f}')
        c1.latex(f'MAP@10={days_map10:.5f}')
        c2.latex(f'a_c={cart_rate:.5f}')
        c2.latex(f'MAP@10={cart_map10:.5f}')
        c3.latex(f'a_p={total_rate:.5f}')
        c3.latex(f'MAP@10={total_map10:.5f}')

        st.markdown('---')
        c1, c2, _, _ = st.columns([18, 25, 17, 40], gap='large')
        if c1.button('Обучить заново...'):
            with c2:
                start_time = time.time()
                with st.spinner('Обучение...'):
                    recommender.build()
                end_time = time.time()
                exec_time = end_time - start_time
                st.metric('Время выполнения', f'{exec_time:.3f} с')
    elif choice == 'Рекомендации для всех пользователей':
        c1, c2, c3, _ = st.columns([17, 18, 25, 40], gap='large')
        k = c1.number_input('Размер рекомендаций', 1, 10, key='total_k')
        if c2.button('Сформировать рекомендации...', key='total_predict'):
            with c3:
                start_time = time.time()
                with st.spinner('Формирование рекомендаций...'):
                    recommendation = recommender.get_recommendation(k)
                end_time = time.time()
                exec_time = end_time - start_time
                st.metric('Время выполнения', f'{exec_time:.3f} с')
            recommendation.index.name = 'ИН'
            recommendation.columns = [f'Продукт #{i}' for i in range(1, k + 1)]
            st.dataframe(recommendation, use_container_width=True)
    else:
        c1, c2, c3, c4 = st.columns([40, 17, 18, 25], gap='large')
        user_ids = c1.multiselect('ИН пользователей', recommender.get_users())
        k = c2.number_input('Размер рекомендаций', 1, 10, key='user_k')
        if c3.button('Сформировать рекомендации...', key='user_predict', disabled=len(user_ids) == 0):
            with c4:
                start_time = time.time()
                with st.spinner('Формирование рекомендаций...'):
                    recommendation = pd.concat([recommender.get_user_recommendation(user_id, k)
                                                for user_id in user_ids])
                end_time = time.time()
                exec_time = end_time - start_time
                st.metric('Время выполнения', f'{exec_time:.3f} с')
            recommendation.index.name = 'ИН'
            recommendation.columns = [f'Продукт #{i}' for i in range(1, k + 1)]
            st.dataframe(recommendation, use_container_width=True)