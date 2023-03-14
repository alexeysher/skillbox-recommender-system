from pathlib import Path
import streamlit as st
import matplotlib.pyplot as plt

from auxiliary import set_text_style, InstacartColors

DATA_PATH = Path('D:/skillbox-recommender-system/data')  # Путь к папке данных
TRANSACTIONS_PATH = DATA_PATH / 'transactions.csv'  # Путь к файлу логов транзакций
PRODUCTS_PATH = DATA_PATH / 'products.csv'  # Путь к файлу справочника продуктов


@st.cache_data
def load_data():
    global DATA_PATH
    from pickle import load

    data = []
    for file_name in [
        'frequency_ratings.dmp',
        'frequency_map_10.dmp',
        'days_rate.dmp',
        'days_ratings.dmp',
        'days_map10.dmp',
        'map10_days.dmp',
        'map10_days_pred.dmp',
        'cart_rate.dmp',
        'cart_ratings.dmp',
        'cart_map10.dmp',
        'map10_cart.dmp',
        'map10_cart_pred.dmp',
        'total_rate.dmp',
        'total_ratings.dmp',
        'total_map10.dmp',
        'map10_total.dmp',
        'map10_total_pred.dmp',
        'missed_last_products.dmp',
    ]:
        file_path = DATA_PATH / file_name
        with open(file_path, 'rb') as fp:
            data.append(load(fp))
    return data


@st.cache_resource
def plot_ratings_hist(frequency_ratings, frequency_map_10):
    fig, ax = plt.subplots(facecolor=InstacartColors.Cashew)
    bins = range(frequency_ratings['rating'].min(), frequency_ratings['rating'].max())
    ax.hist(frequency_ratings['rating'], color=InstacartColors.IllustrationBlue, bins=bins)
    ax.set_xlabel('$r_{u, i}$', fontfamily='sans serif', fontsize=14, color=InstacartColors.Kale)
    ax.set_xlim(1, 11)
    # ax.set_ylabel('Количество продуктов', fontfamily='sans serif', fontsize=14, color=InstacartColors.Kale)
    ax.grid()
    return fig


@st.cache_resource
def plot_days_hist(days_ratings, frequency_ratings):
    fig, ax = plt.subplots(facecolor=InstacartColors.Cashew)
    bins = range(int(frequency_ratings['rating'].min()), int(frequency_ratings['rating'].max()) + 1)
    ax.hist(days_ratings['rating'], color=InstacartColors.IllustrationBlue, bins=bins)
    ax.set_xlabel('$r_{u, i}$', fontfamily='sans serif', fontsize=14, color=InstacartColors.Kale)
    ax.set_xlim(1, 11)
    # ax.set_ylabel('Количество продуктов', fontfamily='sans serif', fontsize=14, color=InstacartColors.Kale)
    ax.grid()
    return fig


@st.cache_resource
def plot_days(map10_days, days_map10, _map10_days_pred, days_rate):
    fig, ax = plt.subplots(facecolor=InstacartColors.Cashew)
    ax.plot(map10_days, color=InstacartColors.IllustrationBlue, linewidth=2)
    ax.plot(map10_days.index.values, _map10_days_pred, linestyle='--', color=InstacartColors.IllustrationPink,
            linewidth=2)
    ax.scatter(days_rate, days_map10, color=InstacartColors.IllustrationRed, linewidth=1)
    ax.axvline(days_rate, color=InstacartColors.IllustrationRed, linestyle='--', linewidth=1)
    ax.axhline(days_map10, color=InstacartColors.IllustrationRed, linestyle='--', linewidth=1)
    ax.set_xlabel('$a_d$', fontfamily='sans serif', fontsize=14, color=InstacartColors.Kale)
    ax.set_ylabel('MAP@10', fontfamily='sans serif', fontsize=14, color=InstacartColors.Kale)
    ax.grid()
    _ = ax.legend(['Реальные значения', 'Аппроксимация', 'Пик'])
    return fig


@st.cache_resource
def plot_cart(map10_cart, cart_map10, _map10_cart_pred, cart_rate):
    fig, ax = plt.subplots(facecolor=InstacartColors.Cashew)
    ax.plot(map10_cart, color=InstacartColors.IllustrationBlue, linewidth=2)
    ax.plot(map10_cart.index.values, _map10_cart_pred, linestyle='--', color=InstacartColors.IllustrationPink,
            linewidth=2)
    ax.scatter(cart_rate, cart_map10, color=InstacartColors.IllustrationRed, linewidth=1)
    ax.axvline(cart_rate, color=InstacartColors.IllustrationRed, linestyle='--', linewidth=1)
    ax.axhline(cart_map10, color=InstacartColors.IllustrationRed, linestyle='--', linewidth=1)
    ax.set_xlabel('$a_d$', fontfamily='sans serif', fontsize=14, color=InstacartColors.Kale)
    ax.set_ylabel('MAP@10', fontfamily='sans serif', fontsize=14, color=InstacartColors.Kale)
    ax.grid()
    _ = ax.legend(['Реальные значения', 'Аппроксимация', 'Пик'])
    return fig


@st.cache_resource
def plot_cart_hist(cart_ratings, frequency_ratings):
    fig, ax = plt.subplots(facecolor=InstacartColors.Cashew)
    # min_value
    bins = range(int(frequency_ratings['rating'].min()), int(frequency_ratings['rating'].max()) + 1)
    ax.hist(cart_ratings['rating'], color=InstacartColors.IllustrationBlue, bins=bins)
    ax.set_xlabel('$r_{u, i}$', fontfamily='sans serif', fontsize=14, color=InstacartColors.Kale)
    ax.set_xlim(1, 11)
    # ax.set_ylabel('Количество продуктов', fontfamily='sans serif', fontsize=14, color=InstacartColors.Kale)
    ax.grid()
    return fig


@st.cache_resource
def plot_total(map10_total, total_map10, _map10_total_pred, total_rate):
    fig, ax = plt.subplots(facecolor=InstacartColors.Cashew)
    ax.plot(map10_total, color=InstacartColors.IllustrationBlue, linewidth=2)
    ax.plot(map10_total.index.values, _map10_total_pred, linestyle='--', color=InstacartColors.IllustrationPink,
            linewidth=2)
    ax.scatter(total_rate, total_map10, color=InstacartColors.IllustrationRed, linewidth=1)
    ax.axvline(total_rate, color=InstacartColors.IllustrationRed, linestyle='--', linewidth=1)
    ax.axhline(total_map10, color=InstacartColors.IllustrationRed, linestyle='--', linewidth=1)
    ax.set_xlabel('$a_d$', fontfamily='sans serif', fontsize=14, color=InstacartColors.Kale)
    ax.set_ylabel('MAP@10', fontfamily='sans serif', fontsize=14, color=InstacartColors.Kale)
    ax.grid()
    _ = ax.legend(['Реальные значения', 'Аппроксимация', 'Пик'])
    return fig


@st.cache_resource
def plot_total_hist(total_ratings, frequency_ratings):
    fig, ax = plt.subplots(facecolor=InstacartColors.Cashew)
    # min_value
    bins = range(int(frequency_ratings['rating'].min()), int(frequency_ratings['rating'].max()) + 1)
    ax.hist(total_ratings['rating'], color=InstacartColors.IllustrationBlue, bins=bins)
    ax.set_xlabel('$r_{u, i}$', fontfamily='sans serif', fontsize=14, color=InstacartColors.Kale)
    ax.set_xlim(1, 11)
    # ax.set_ylabel('Количество продуктов', fontfamily='sans serif', fontsize=14, color=InstacartColors.Kale)
    ax.grid()
    return fig


@st.cache_resource
def plot_missed_hist(missed_last_products):
    fig, ax = plt.subplots(facecolor=InstacartColors.Cashew)
    bins = range(0, 1001, 10)
    ax.hist(missed_last_products['total_rank'], color=InstacartColors.IllustrationBlue, bins=bins)
    ax.set_xlabel('Ранг', fontfamily='sans serif', fontsize=14, color=InstacartColors.Kale)
    ax.set_xlim(1, 1000)
    ax.set_ylabel('Количество продуктов', fontfamily='sans serif', fontsize=14, color=InstacartColors.Kale)
    ax.grid()
    return fig


def main():

    frequency_ratings, frequency_map_10,\
        days_rate, days_ratings, days_map10, map10_days, map10_days_pred, \
        cart_rate, cart_ratings, cart_map10, map10_cart, map10_cart_pred, \
        total_rate, total_ratings, total_map10, map10_total, map10_total_pred, \
        missed_last_products = load_data()

    # st.markdown('---')
    st.markdown('**' + set_text_style('Фильтрация по частоте', size=48, color=InstacartColors.Carrot, align='center') +
                '**', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap='large')
    col_title = 'Количество' + set_text_style('▲', tag='span', color=InstacartColors.Lime) + \
                '&nbsp;→&nbsp;Рейтинг' + set_text_style('▲', tag='span', color=InstacartColors.Lime)
    col_title = set_text_style(col_title, size=24, align='center')
    c1.markdown(col_title, unsafe_allow_html=True)
    c1.markdown('---')
    c1.latex('\large r_{u,i}=\sum_{t \in T_u}s_{u,i,t}')
    c1.markdown(
        '''
    | Обозначение | Описание    |
    | ----------- | ----------- |
    | $r_{u,i}$   | рейтинг продукта с номером $i$ у пользователя с номером $u$   |
    | $T_u$       | номера транзакций, совершенных пользователем с номером $u$    |
    | $s_{u,i,t}$ | присутствие продукта с номером $i$ в транзакции с номером $t$ пользователя с номером $u$: $0$-нет, $1$-да |
        ''', unsafe_allow_html=True)
    c1.markdown('---')
    map10_value = set_text_style('MAP@10 = ', size=32, tag='span') + '**' + \
                  set_text_style(f'{frequency_map_10:.6f}', size=32, tag='span') + '**'
    c1.markdown(map10_value, unsafe_allow_html=True)

    col_title = set_text_style('Распределение рейтингов '
                               'ранее купленных продуктов',
                               size=24, align='center')
    c2.markdown(col_title, unsafe_allow_html=True)
    fig = plot_ratings_hist(frequency_ratings, frequency_map_10)
    c2.pyplot(fig)

    st.markdown('---')
    st.markdown('**' + set_text_style('Фильтрация по времени', size=48, color=InstacartColors.Carrot, align='center') +
                '**', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap='large')
    col_title = 'Время' + set_text_style('▲', tag='span', color=InstacartColors.Lime) + \
                '&nbsp;→&nbsp;Вес' + set_text_style('▼', tag='span', color=InstacartColors.IllustrationRed)
    col_title = set_text_style(col_title, size=24, align='center')
    c1.markdown(col_title, unsafe_allow_html=True)
    c1.markdown('---')
    c1.latex('\large w_{u,t}=e^{-d_{u,t}·a_d}')
    c1.latex('\large r_{u,i}=\sum_{t \in T_u}s_{u,i,t}·w_{u,t}')
    c1.markdown(
        '''
    | Обозначение | Описание                                                                                 |
    | ----------- | ---------------------------------------------------------------------------------------- |
    | $w_{u,t}$   | вес транзакции с номером $t$ пользователя с номером $u$                                  |
    | $d_{u,t}$   | время совершения транзакции с номером $t$ пользователя с номером $u$                     |
    | $a_d$       | коэффициент фильтрации (положительное число)                                             |
    | $r_{u,i}$   | рейтинг продукта с номером $i$ у пользователя с номером $u$                              |
    | $T_u$       | номера транзакций, совершенных пользователем с номером $u$                               |
    | $s_{u,i,t}$ | присутствие продукта с номером $i$ в транзакции с номером $t$ пользователя с номером $u$ |
        '''
    )
    c1.markdown('---')
    map10_value = set_text_style('MAP@10 = ', size=32, tag='span') + '**' + \
                  set_text_style(f'{days_map10:.6f} ', size=32, tag='span') + \
                  set_text_style(f'▲{days_map10 - frequency_map_10:.6f}', size=24, color=InstacartColors.Lime,
                                 tag='span') + '**'
    c1.markdown(map10_value, unsafe_allow_html=True)

    col_title = set_text_style('Зависимость точности предсказаний '
                               'от коэффициента фильтрации',
                               size=24, align='center')
    c2.markdown(col_title, unsafe_allow_html=True)
    fig = plot_days(map10_days, days_map10, map10_days_pred, days_rate)
    c2.pyplot(fig)
    col_title = set_text_style('Распределение рейтингов '
                               'ранее купленных продуктов',
                               size=24, align='center')
    c2.markdown(col_title, unsafe_allow_html=True)
    fig = plot_days_hist(days_ratings, frequency_ratings)
    c2.pyplot(fig)

    st.markdown('---')
    st.markdown('**' + set_text_style('Фильтрация по номеру добавления в корзину', size=48, color=InstacartColors.Carrot,
                                      align='center') + '**', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap='large')
    col_title = 'Номер' + set_text_style('▲', tag='span', color=InstacartColors.Lime) + \
                '&nbsp;→&nbsp;Вес' + set_text_style('▼', tag='span', color=InstacartColors.IllustrationRed)
    col_title = set_text_style(col_title, size=24, align='center')
    c1.markdown(col_title, unsafe_allow_html=True)
    c1.markdown('---')
    c1.latex('\large w_{u,i,t} = e^{-d_{u,t}·a_d}·e^{-c_{u,i,t}·a_c}')
    c1.latex('\large r_{u,i}=\sum_{t \in T_u}s_{u,i,t}·w_{u,i,t}')
    c1.markdown(
        '''
    | Обозначение | Описание                                                                                 |
    | ----------- | ---------------------------------------------------------------------------------------- |
    | $w_{u,i,t}$ | вес продукта с номером $i$ в транзакции с номером $t$ пользователя с номером $u$         |
    | $d_{u,t}$   | время совершения транзакции с номером $t$ пользователя с номером $u$                     |
    | $a_d$       | коэффициент фильтрации (положительное число)                                             |
    | $c_{u,i,t}$ | порядковый номер добавления продукта с номером $i$ в корзину в транзакции с номером $t$  |
    | $a_c$       | коэффициент фильтрации по номеру добавления продукта в корзину                           |
    | $r_{u,i}$   | рейтинг продукта с номером $i$ у пользователя с номером $u$                              |
    | $T_u$       | номера транзакций, совершенных пользователем с номером $u$                               |
    | $s_{u,i,t}$ | присутствие продукта с номером $i$ в транзакции с номером $t$ пользователя с номером $u$ |
        '''
    )
    c1.markdown('---')
    map10_value = set_text_style('MAP@10 = ', size=32, tag='span') + '**' + \
                  set_text_style(f'{cart_map10:.6f} ', size=32, tag='span') + \
                  set_text_style(f'▲{cart_map10 - days_map10:.6f}', size=24, color=InstacartColors.Lime,
                                 tag='span') + '**'
    c1.markdown(map10_value, unsafe_allow_html=True)

    col_title = set_text_style('Зависимость точности предсказаний '
                               'от коэффициента фильтрации',
                               size=24, align='center')
    c2.markdown(col_title, unsafe_allow_html=True)
    fig = plot_cart(map10_cart, cart_map10, map10_cart_pred, cart_rate)
    c2.pyplot(fig)
    col_title = set_text_style('Распределение рейтингов '
                               'ранее купленных продуктов',
                               size=24, align='center')
    c2.markdown(col_title, unsafe_allow_html=True)
    fig = plot_cart_hist(cart_ratings, frequency_ratings)
    c2.pyplot(fig)

    st.markdown('---')
    st.markdown('**' + set_text_style('Фильтрация по популярности', size=48, color=InstacartColors.Carrot, align='center') +
                '**', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap='large')
    col_title = 'Популярность' + set_text_style('▲', tag='span', color=InstacartColors.Lime) + \
                '&nbsp;→&nbsp;Рейтинг' + set_text_style('▲', tag='span', color=InstacartColors.Lime)
    col_title = set_text_style(col_title, size=24, align='center')
    fig = plot_missed_hist(missed_last_products)
    col_title = set_text_style('Распределение глобального ранга среди продуктов, '
                               'не попавших в рекомендации',
                               size=24, align='center')
    c1.markdown(col_title, unsafe_allow_html=True)
    c1.pyplot(fig)
    c1.markdown(col_title, unsafe_allow_html=True)
    c1.markdown('---')
    c1.latex('\large r^g_i={\sum_{u \in U}r_{u,i} \over |U|}')
    c1.latex('\large r^*_{u,i}=r_{u,i}·e^{r^g_i·a_p}')
    c1.markdown(
        '''
    | Обозначение | Описание                                                             |
    | ----------- | -------------------------------------------------------------------- |
    | $r^g_i$     | глобальный рейтинг продукта с номером $i$                            |
    | $r_{u,i}$   | рейтинг продукта с номером $i$ у пользователя с номером $u$          |
    | $U$         | множество номеров пользователей в транзакциях                        |
    | $a_p$       | коэффициент фильтрации продуктов по популярности                     |
        '''
    )
    c1.markdown('---')
    map10_value = set_text_style('MAP@10 = ', size=32, tag='span') + '**' + \
                  set_text_style(f'{total_map10:.6f} ', size=32, tag='span') + \
                  set_text_style(f'▲{total_map10 - cart_map10:.6f}', size=24, color=InstacartColors.Lime,
                                 tag='span') + '**'
    c1.markdown(map10_value, unsafe_allow_html=True)

    col_title = set_text_style('Зависимость точности предсказаний '
                               'от коэффициента фильтрации',
                               size=24, align='center')
    c2.markdown(col_title, unsafe_allow_html=True)
    fig = plot_total(map10_total, total_map10, map10_total_pred, total_rate)
    c2.pyplot(fig)
    col_title = set_text_style('Распределение рейтингов '
                               'ранее купленных продуктов',
                               size=24, align='center')
    c2.markdown(col_title, unsafe_allow_html=True)
    fig = plot_total_hist(total_ratings, frequency_ratings)
    c2.pyplot(fig)
