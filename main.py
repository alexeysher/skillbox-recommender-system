import shutil

import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
from auxiliary import set_text_style, InstacartColors
from pickle import load
from pathlib import Path
import gdown

DATA_PATH = 'data'  # Путь к папке данных

products_reordering = None


def load_data(var_name: str):
    zip_file = Path(var_name).with_suffix('.zip')
    data_file = Path(var_name).with_suffix('.dmp')
    gdown.cached_download(st.secrets['urls'][var_name], path=zip_file.as_posix(), fuzzy=True)
    shutil.unpack_archive(zip_file, '.')
    st.markdown(f'{zip_file.as_posix()}; exists = {zip_file.exists()}')
    st.markdown(f'{data_file.as_posix()}; exists = {data_file.exists()}')
    with open(data_file, 'rb') as fp:
        data = load(fp)
    zip_file.unlink()
    data_file.unlink()
    st.markdown(f'{zip_file.as_posix()}; exists = {zip_file.exists()}')
    st.markdown(f'{data_file.as_posix()}; exists = {data_file.exists()}')
    return data


@st.cache_data(show_spinner='Загрузка данных...')
def prepare_data():
    global products_reordering
    products_reordering = load_data('products_reordering')
    plot_reordering_prop()
    del products_reordering
    # for file_name in [
    #     'products_reordering.dmp',
    #     'products_reordering_percentages.dmp',
    #     'days_bins.dmp',
    #     'days_total_counts.dmp',
    #     'days_reordered_counts.dmp',
    #     'cart_bins.dmp',
    #     'cart_total_counts.dmp',
    #     'cart_reordered_counts.dmp',
    #     'frequency_ratings.dmp',
    #     'frequency_map_10.dmp',
    #     'days_rate.dmp',
    #     'days_ratings.dmp',
    #     'days_map10.dmp',
    #     'map10_days.dmp',
    #     'map10_days_pred.dmp',
    #     'cart_rate.dmp',
    #     'cart_ratings.dmp',
    #     'cart_map10.dmp',
    #     'map10_cart.dmp',
    #     'map10_cart_pred.dmp',
    #     'total_rate.dmp',
    #     'total_ratings.dmp',
    #     'total_map10.dmp',
    #     'map10_total.dmp',
    #     'map10_total_pred.dmp',
    #     'missed_last_products.dmp',
    #     'test_results.dmp',
    #     # 'filled_up_map10.dmp',
    #     # 'total_map10.dmp',
    # ]:
    #     file_path = data_path / file_name
    #     with open(file_path, 'rb') as fp:
    #         data.append(load(fp))
    # shutil.rmtree(data_path)
    # data_zip_file.unlink()
    # return data


@st.cache_resource
def plot_reordering_prop():
    fig, ax = plt.subplots(facecolor=InstacartColors.Cashew)
    prior_ordered_fraction = products_reordering['days_before_last_order'].count() / \
                             products_reordering['days_before_last_order'].size * 100
    bars = ax.bar(['Да', 'Нет'], [prior_ordered_fraction, 100 - prior_ordered_fraction])
    bars[0].set_color(InstacartColors.IllustrationBlue)
    bars[1].set_color(InstacartColors.IllustrationPink)
    ax.set_xlabel('Присутствие в предыдущих покупках', fontfamily='sans serif', fontsize=14,
                  color=InstacartColors.Kale)
    ax.set_ylabel('Доля [%]', fontfamily='sans serif', fontsize=14,
                  color=InstacartColors.Kale)
    ax.grid()
    return fig


@st.cache_resource
def plot_reordering_hist(products_reordering_percentages):
    fig, ax = plt.subplots(facecolor=InstacartColors.Cashew)
    _, _, bars = ax.hist(products_reordering_percentages['reordered_percentage'], bins=20)
    for bar in bars[:-4]:
        bar.set_color(InstacartColors.IllustrationBlue)
    for bar in bars[-4:]:
        bar.set_color(InstacartColors.IllustrationPink)
    ax.set_xlabel('Доля ранее покупавшихся продуктов [%]', fontfamily='sans serif', fontsize=14,
                  color=InstacartColors.Kale)
    ax.set_ylabel('Количество пользователей', fontfamily='sans serif', fontsize=14,
                  color=InstacartColors.Kale)
    ax.grid()
    return fig


@st.cache_resource
def plot_days_reordering(days_bins, days_total_counts, days_reordered_counts):
    fig, ax = plt.subplots(facecolor=InstacartColors.Cashew)
    x = [(x1 + x2) / 2 for x1, x2 in zip(days_bins[:-1], days_bins[1:])]
    y = [reordered_count / total_count * 100 for total_count, reordered_count
         in zip(days_total_counts, days_reordered_counts)]
    line, = ax.plot(x, y)
    line.set_linewidth(4)
    # line.set_alpha(0.75)
    line.set_color(InstacartColors.IllustrationBlue)
    ax.set_xlabel('Время заказа [дни]', fontfamily='sans serif', fontsize=14, color=InstacartColors.Kale)
    ax.set_ylabel('Доля продуктов [%]', fontfamily='sans serif', fontsize=14, color=InstacartColors.Kale)
    ax.grid()
    return fig


@st.cache_resource
def plot_cart_reordering(cart_bins, cart_total_counts, cart_reordered_counts):
    fig, ax = plt.subplots(facecolor=InstacartColors.Cashew)
    x = [(x1 + x2) / 2 for x1, x2 in zip(cart_bins[:-1], cart_bins[1:])]
    y = [reordered_count / total_count * 100 for total_count, reordered_count
         in zip(cart_total_counts, cart_reordered_counts)]
    line, = ax.plot(x, y)
    line.set_color(InstacartColors.IllustrationPink)
    line.set_linewidth(4)
    # line.set_alpha(0.75)
    ax.set_xlabel('Номер', fontfamily='sans serif', fontsize=14, color=InstacartColors.Kale)
    ax.set_ylabel('Доля продуктов [%]', fontfamily='sans serif', fontsize=14, color=InstacartColors.Kale)
    ax.grid()
    return fig


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


@st.cache_resource
def plot_aisle_rank_hist(missed_last_products):
    fig, ax = plt.subplots(facecolor=InstacartColors.Cashew)
    bins = int(missed_last_products['aisle_rank'].max())
    ax.hist(missed_last_products['aisle_rank'], color=InstacartColors.IllustrationBlue, bins=bins)
    ax.set_xlabel('Ранг', fontfamily='sans serif', fontsize=14, color=InstacartColors.Kale)
    ax.set_xlim(1, 25)
    ax.set_ylabel('Количество продуктов', fontfamily='sans serif', fontsize=14, color=InstacartColors.Kale)
    ax.grid()
    return fig


@st.cache_resource
def plot_in_aisle_rank_hist(missed_last_products):
    import matplotlib.pyplot as plt
    from auxiliary import InstacartColors

    fig, ax = plt.subplots(facecolor=InstacartColors.Cashew)
    bins = int(missed_last_products['inside_aisle_rank'].max())
    ax.hist(missed_last_products['inside_aisle_rank'], color=InstacartColors.IllustrationBlue, bins=bins)
    ax.set_xlabel('Ранг', fontfamily='sans serif', fontsize=14, color=InstacartColors.Kale)
    ax.set_xlim(1, 25)
    ax.set_ylabel('Количество продуктов', fontfamily='sans serif', fontsize=14, color=InstacartColors.Kale)
    ax.grid()
    return fig


def intro():
    """
    Титульная страница.
    """
    title = set_text_style('<b>Рекомендательная система для онлайн-гипермаркета Instacart</b>', font_size=80)
    st.markdown(title, unsafe_allow_html=True)
    st.markdown(set_text_style('&nbsp;', font_size=32), unsafe_allow_html=True)
    author = set_text_style('Автор: ', color=InstacartColors.Kale, tag='span') + \
             set_text_style('<b>Алексей Шерстобитов</b>', color=InstacartColors.Carrot, tag='span')
    author = set_text_style(author, font_size=48)
    st.markdown(author, unsafe_allow_html=True)


def goals():
    """
    Цели и задачи.
    """
    title = set_text_style('<b>Чем занимается Instacart?</b>', font_size=48, color=InstacartColors.Carrot,
                           text_align='center')
    st.markdown(title, unsafe_allow_html=True)
    title = set_text_style('<b>Сервис по доставке продовольствия. Предлагает свои услуги через мобильное приложение и '
                           'веб-сайт. Сервис позволяет пользователям заказывать необходимые продукты из магазинов.</b>',
                           font_size=32, color=InstacartColors.Kale)
    st.markdown(title, unsafe_allow_html=True)
    st.markdown(set_text_style('&nbsp;', font_size=32), unsafe_allow_html=True)
    title = set_text_style('<b>Что нужно Instacart?</b>', font_size=48, color=InstacartColors.Carrot,
                           text_align='center')
    st.markdown(title, unsafe_allow_html=True)
    title = set_text_style('<b>Система помощи пользователю, которая показывает ему те товары, которые он, скорее всего, '
                           'захочет купить.</b>', font_size=32, color=InstacartColors.Kale)
    st.markdown(title, unsafe_allow_html=True)

    # title = set_text_style('<b>Рекомендательная система для онлайн-гипермаркета Instacart</b>', font_size=80)
    # st.markdown(title, unsafe_allow_html=True)
    # author = set_text_style('Автор: ', color=InstacartColors.Kale, tag='span') + \
    #          set_text_style('<b>Алексей Шерстобитов</b>', color=InstacartColors.Carrot, tag='span')
    # author = set_text_style(author, font_size=48)
    # 'Поэтому мы хотим помогать пользователю и показывать ему те товары, которые он, скорее всего, захочет купить.'
    # st.markdown(author, unsafe_allow_html=True)


def features():
    title = '**' + set_text_style('Повторяемость', font_size=48, color=InstacartColors.Carrot,
                                  text_align='center') + '**'
    st.markdown(title, unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap='large')
    col_title = set_text_style('Соотношение продуктов в зависимости от присутствия в предыдущих заказах',
                               font_size=24, text_align='center')
    c1.markdown(col_title, unsafe_allow_html=True)
    col_title = set_text_style('Распределение долей покупавшихся ранее продуктов в последних заказах',
                               font_size=24, text_align='center')
    c2.markdown(col_title, unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap='large')
    fig = plot_reordering_prop()
    c1.pyplot(fig)
    # fig = plot_reordering_hist(products_reordering_percentages)
    # c2.pyplot(fig)
    #
    # # Плавное изменение и Сначала важные
    # c1, c2 = st.columns(2, gap='large')
    # c1.markdown('---')
    # c2.markdown('---')
    # col_title = '**' + set_text_style('Плавное изменение', font_size=48, color=InstacartColors.Carrot,
    #                                   text_align='center') + '**'
    # c1.markdown(col_title, unsafe_allow_html=True)
    # col_title = '**' + set_text_style('Сначала важные', font_size=48, color=InstacartColors.Carrot,
    #                                   text_align='center') + '**'
    # c2.markdown(col_title, unsafe_allow_html=True)
    # c1, c2 = st.columns(2, gap='large')
    # col_title = set_text_style('Зависимость доли продуктов, присутствующих в последующих заказах, '
    #                            'в зависимости от времени заказа', font_size=24, text_align='center')
    # c1.markdown(col_title, unsafe_allow_html=True)
    # col_title = set_text_style('Зависимость доли продуктов, присутствующих в последующих заказах, '
    #                            'в зависимости от номера добавления продукта в корзину', font_size=24,
    #                            text_align='center')
    # c2.markdown(col_title, unsafe_allow_html=True)
    # c1, c2 = st.columns(2, gap='large')
    # fig = plot_days_reordering(days_bins, days_total_counts, days_reordered_counts)
    # c1.pyplot(fig)
    # fig = plot_cart_reordering(cart_bins, cart_total_counts, cart_reordered_counts)
    # c2.pyplot(fig)


def filtering(frequency_ratings, frequency_map_10,
              days_rate, days_ratings, days_map10, map10_days, map10_days_pred,
              cart_rate, cart_ratings, cart_map10, map10_cart, map10_cart_pred,
              total_rate, total_ratings, total_map10, map10_total, map10_total_pred,
              missed_last_products):
    st.markdown('**' + set_text_style('Фильтрация по частоте', font_size=48, color=InstacartColors.Carrot,
                                      text_align='center') +
                '**', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap='large')
    col_title = 'Количество' + set_text_style('▲', tag='span', color=InstacartColors.Lime) + \
                '&nbsp;→&nbsp;Рейтинг' + set_text_style('▲', tag='span', color=InstacartColors.Lime)
    col_title = set_text_style(col_title, font_size=24, text_align='center')
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
    map10_value = set_text_style('MAP@10 = ', font_size=32, tag='span') + '**' + \
                  set_text_style(f'{frequency_map_10:.6f}', font_size=32, tag='span') + '**'
    c1.markdown(map10_value, unsafe_allow_html=True)

    col_title = set_text_style('Распределение рейтингов '
                               'ранее купленных продуктов',
                               font_size=24, text_align='center')
    c2.markdown(col_title, unsafe_allow_html=True)
    fig = plot_ratings_hist(frequency_ratings, frequency_map_10)
    c2.pyplot(fig)

    st.markdown('---')
    st.markdown('**' + set_text_style('Фильтрация по времени', font_size=48, color=InstacartColors.Carrot,
                                      text_align='center') + '**', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap='large')
    col_title = 'Время' + set_text_style('▲', tag='span', color=InstacartColors.Lime) + \
                '&nbsp;→&nbsp;Вес' + set_text_style('▼', tag='span', color=InstacartColors.IllustrationRed)
    col_title = set_text_style(col_title, font_size=24, text_align='center')
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
    map10_value = set_text_style('MAP@10 = ', font_size=32, tag='span') + '**' + \
                  set_text_style(f'{days_map10:.6f} ', font_size=32, tag='span') + \
                  set_text_style(f'▲{days_map10 - frequency_map_10:.6f}', font_size=24, color=InstacartColors.Lime,
                                 tag='span') + '**'
    c1.markdown(map10_value, unsafe_allow_html=True)

    col_title = set_text_style('Зависимость точности предсказаний '
                               'от коэффициента фильтрации',
                               font_size=24, text_align='center')
    c2.markdown(col_title, unsafe_allow_html=True)
    fig = plot_days(map10_days, days_map10, map10_days_pred, days_rate)
    c2.pyplot(fig)
    col_title = set_text_style('Распределение рейтингов '
                               'ранее купленных продуктов',
                               font_size=24, text_align='center')
    c2.markdown(col_title, unsafe_allow_html=True)
    fig = plot_days_hist(days_ratings, frequency_ratings)
    c2.pyplot(fig)

    st.markdown('---')
    st.markdown(
        '**' + set_text_style('Фильтрация по номеру добавления в корзину', font_size=48, color=InstacartColors.Carrot,
                              text_align='center') + '**', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap='large')
    col_title = 'Номер' + set_text_style('▲', tag='span', color=InstacartColors.Lime) + \
                '&nbsp;→&nbsp;Вес' + set_text_style('▼', tag='span', color=InstacartColors.IllustrationRed)
    col_title = set_text_style(col_title, font_size=24, text_align='center')
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
    map10_value = set_text_style('MAP@10 = ', font_size=32, tag='span') + '**' + \
                  set_text_style(f'{cart_map10:.6f} ', font_size=32, tag='span') + \
                  set_text_style(f'▲{cart_map10 - days_map10:.6f}', font_size=24, color=InstacartColors.Lime,
                                 tag='span') + '**'
    c1.markdown(map10_value, unsafe_allow_html=True)

    col_title = set_text_style('Зависимость точности предсказаний '
                               'от коэффициента фильтрации',
                               font_size=24, text_align='center')
    c2.markdown(col_title, unsafe_allow_html=True)
    fig = plot_cart(map10_cart, cart_map10, map10_cart_pred, cart_rate)
    c2.pyplot(fig)
    col_title = set_text_style('Распределение рейтингов '
                               'ранее купленных продуктов',
                               font_size=24, text_align='center')
    c2.markdown(col_title, unsafe_allow_html=True)
    fig = plot_cart_hist(cart_ratings, frequency_ratings)
    c2.pyplot(fig)

    st.markdown('---')
    st.markdown('**' + set_text_style('Фильтрация по популярности', font_size=48, color=InstacartColors.Carrot,
                                      text_align='center') + '**', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap='large')
    col_title = 'Популярность' + set_text_style('▲', tag='span', color=InstacartColors.Lime) + \
                '&nbsp;→&nbsp;Рейтинг' + set_text_style('▲', tag='span', color=InstacartColors.Lime)
    col_title = set_text_style(col_title, font_size=24, text_align='center')
    fig = plot_missed_hist(missed_last_products)
    col_title = set_text_style('Распределение глобального ранга среди продуктов, '
                               'не попавших в рекомендации',
                               font_size=24, text_align='center')
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
    map10_value = set_text_style('MAP@10 = ', font_size=32, tag='span') + '**' + \
                  set_text_style(f'{total_map10:.6f} ', font_size=32, tag='span') + \
                  set_text_style(f'▲{total_map10 - cart_map10:.6f}', font_size=24, color=InstacartColors.Lime,
                                 tag='span') + '**'
    c1.markdown(map10_value, unsafe_allow_html=True)

    col_title = set_text_style('Зависимость точности предсказаний '
                               'от коэффициента фильтрации',
                               font_size=24, text_align='center')
    c2.markdown(col_title, unsafe_allow_html=True)
    fig = plot_total(map10_total, total_map10, map10_total_pred, total_rate)
    c2.pyplot(fig)
    col_title = set_text_style('Распределение рейтингов '
                               'ранее купленных продуктов',
                               font_size=24, text_align='center')
    c2.markdown(col_title, unsafe_allow_html=True)
    fig = plot_total_hist(total_ratings, frequency_ratings)
    c2.pyplot(fig)


def filling(missed_last_products):
    st.markdown(
        '**' + set_text_style('Заполнение', font_size=48, color=InstacartColors.Carrot, text_align='center') +
        '**', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap='large')

    col_title = 'Ранг группы' + set_text_style('▲', tag='span', color=InstacartColors.Lime) + \
                '&nbsp;→&nbsp;Вероятность покупки' + set_text_style('▲', tag='span', color=InstacartColors.Lime)
    col_title = set_text_style(col_title, font_size=24, text_align='center')
    c1.markdown(col_title, unsafe_allow_html=True)
    c1.markdown('---')
    c1.latex('\large r_{u,a}=\sum_{i \in I_a}r_{u,i}')
    c1.markdown(
        '''
    | Обозначение | Описание                                                            |
    | ----------- | ------------------------------------------------------------------- |
    | $r_{u,a}$   | рейтинг группы продуктов с номером $a$ у пользователя с номером $u$ |
    | $r_{u,i}$   | рейтинг продукта с номером $i$ у пользователя с номером $u$         |
    | $I_a$       | номера продуктов в группе продуктов с номером $a$                   |
        ''', unsafe_allow_html=True)

    col_title = 'Ранг продукта' + set_text_style('▲', tag='span', color=InstacartColors.Lime) + \
                '&nbsp;→&nbsp;Вероятность покупки' + set_text_style('▲', tag='span', color=InstacartColors.Lime)
    col_title = set_text_style(col_title, font_size=24, text_align='center')
    c2.markdown(col_title, unsafe_allow_html=True)
    c2.markdown('---')
    c2.latex('\large r^g_i={\sum_{u \in U}r_{u,i} \over |U|}')
    c2.markdown(
        '''
    | Обозначение | Описание                                                    |
    | ----------- | ----------------------------------------------------------- |
    | $r^g_i$     | глобальный рейтинг продукта с номером $i$                   |
    | $r_{u,i}$   | рейтинг продукта с номером $i$ у пользователя с номером $u$ |
    | $U$         | множество номеров пользователей в транзакциях               |
        ''', unsafe_allow_html=True)

    # col_title = 'Количество' + set_text_style('▲', tag='span', color=InstacartColors.Lime) + \
    #             '&nbsp;→&nbsp;Рейтинг' + set_text_style('▲', tag='span', color=InstacartColors.Lime)
    # col_title = set_text_style(col_title, font_size=24, text_align='center')

    c1, c2 = st.columns(2, gap='large')
    c1.markdown('---')
    col_title = set_text_style('Распределение ранга группы продуктов, '
                               'не попавших в рекомендации',
                               font_size=24, text_align='center')
    c1.markdown(col_title, unsafe_allow_html=True)
    fig = plot_aisle_rank_hist(missed_last_products)
    c1.pyplot(fig)
    c2.markdown('---')
    col_title = set_text_style('Распределение ранга внутри группы продуктов, '
                               'не попавших в рекомендации',
                               font_size=24, text_align='center')
    c2.markdown(col_title, unsafe_allow_html=True)
    fig = plot_in_aisle_rank_hist(missed_last_products)
    c2.pyplot(fig)

    st.markdown('---')
    # map10_value = set_text_style('MAP@10 = ', font_size=32, tag='span') + '**' + \
    #               set_text_style(f'{filled_up_map10:.6f} ', font_size=32, tag='span') + \
    #               set_text_style(f'▲{filled_up_map10 - total_map10:.6f}', font_size=24, color=InstacartColors.Lime,
    #                              tag='span') + '**'
    # st.markdown(map10_value, unsafe_allow_html=True)


def test(test_results):
    st.markdown('**' + set_text_style('Результаты проверки на платформе Kaggle', font_size=48,
                                      color=InstacartColors.Carrot, text_align='center') + '**',
                unsafe_allow_html=True)
    table = '''
| Тип обработки | publicScore | privateScore | meanScore |
|---------------|-------------|--------------|-----------|
'''
    for _, (description, publicScore, privateScore, meanScore) \
            in test_results[['description', 'publicScore', 'privateScore', 'meanScore']].iloc[:-1].iterrows():
        table += f'|{description}|{publicScore:.5f}|{privateScore:.5f}|{meanScore:.5f}|\n'
    description, publicScore, privateScore, meanScore = \
        test_results[['description', 'publicScore', 'privateScore', 'meanScore']].iloc[-1]
    table += f'|**:orange[{description}]**|**:orange[{publicScore:.5f}]**' \
             f'|**:orange[{privateScore:.5f}]**|**:orange[{meanScore:.5f}]**|'
    st.markdown(table)

    st.markdown('---')

    test_results['color'] = InstacartColors.IllustrationBlue
    test_results.at[test_results['meanScore'].idxmax(), 'color'] = InstacartColors.Carrot
    fig, ax = plt.subplots(facecolor=InstacartColors.Cashew, figsize=(8, 3))
    test_results.plot(
        ax=ax,
        kind='barh', x='description', y='meanScore', color=test_results['color'],
        title={}, xlabel='', ylabel='',
        grid=True, fontsize=10, legend=False)
    ax.set_xlabel('$MAP@10$')
    _ = ax.set_xlim(0.27, 0.33)
    st.pyplot(fig)


st.set_page_config(page_title='Рекомендательная система для онлайн-гипермаркета Instacart',
                   page_icon=':carrot:', layout='wide')

# products_reordering, products_reordering_percentages, \
#     days_bins, days_total_counts, days_reordered_counts, \
#     cart_bins, cart_total_counts, cart_reordered_counts, \
#     frequency_ratings, frequency_map_10, \
#     days_rate, days_ratings, days_map10, map10_days, map10_days_pred, \
#     cart_rate, cart_ratings, cart_map10, map10_cart, map10_cart_pred, \
#     total_rate, total_ratings, total_map10, map10_total, map10_total_pred, \
#     missed_last_products, test_results = load_data()

prepare_data()

with st.sidebar:
    choice = option_menu(
        '',
        options=[
            "Вступление",
            "Цели и задачи",
            "Особенности",
            "Фильтрация",
            "Заполнение",
            "---",
            "Тестирование",
            # "Прототип"
        ],
        icons=[
            "",
            "map",
            "cart4",
            "filter",
            "droplet",
            "",
            "check-square",
            # "people",
        ],
        orientation='vertical',
        # styles={"container": {"padding": "5!important", "background-color": "#fafafa"}},
        key='main_menu'
    )

match choice:
    case "Вступление":
        intro()
    case "Цели и задачи":
        goals()
    case "Особенности":
        features()
    # case "Фильтрация":
    #     filtering(frequency_ratings, frequency_map_10,
    #               days_rate, days_ratings, days_map10, map10_days, map10_days_pred,
    #               cart_rate, cart_ratings, cart_map10, map10_cart, map10_cart_pred,
    #               total_rate, total_ratings, total_map10, map10_total, map10_total_pred,
    #               missed_last_products)
    # case "Заполнение":
    #     filling(missed_last_products)
    # case "Тестирование":
    #     test(test_results)
