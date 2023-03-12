from pathlib import Path
import streamlit as st

from auxilary import set_text_style, InstacartColors

DATA_PATH = Path('D:/skillbox-recommender-system/data')  # Путь к папке данных


@st.cache_data
def load_data():
    global DATA_PATH
    from pickle import load

    data = []
    for file_name in [
        'missed_last_products.dmp',
        # 'filled_up_map10.dmp',
        # 'total_map10.dmp',
    ]:
        file_path = DATA_PATH / file_name
        with open(file_path, 'rb') as fp:
            data.append(load(fp))
    return data


@st.cache_resource
def plot_aisle_rank_hist(missed_last_products):
    import matplotlib.pyplot as plt
    from auxilary import InstacartColors

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
    from auxilary import InstacartColors

    fig, ax = plt.subplots(facecolor=InstacartColors.Cashew)
    bins = int(missed_last_products['inside_aisle_rank'].max())
    ax.hist(missed_last_products['inside_aisle_rank'], color=InstacartColors.IllustrationBlue, bins=bins)
    ax.set_xlabel('Ранг', fontfamily='sans serif', fontsize=14, color=InstacartColors.Kale)
    ax.set_xlim(1, 25)
    ax.set_ylabel('Количество продуктов', fontfamily='sans serif', fontsize=14, color=InstacartColors.Kale)
    ax.grid()
    return fig


def main():
    # missed_last_products, filled_up_map10, total_map10 = load_data()
    missed_last_products, = load_data()

    st.markdown('**' + set_text_style('Заполнение', size=48, color=InstacartColors.Carrot, align='center') +
                '**', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap='large')

    col_title = 'Ранг группы' + set_text_style('▲', tag='span', color=InstacartColors.Lime) + \
                '&nbsp;→&nbsp;Вероятность покупки' + set_text_style('▲', tag='span', color=InstacartColors.Lime)
    col_title = set_text_style(col_title, size=24, align='center')
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
    col_title = set_text_style(col_title, size=24, align='center')
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
    # col_title = set_text_style(col_title, size=24, align='center')

    c1, c2 = st.columns(2, gap='large')
    c1.markdown('---')
    col_title = set_text_style('Распределение ранга группы продуктов, '
                               'не попавших в рекомендации',
                               size=24, align='center')
    c1.markdown(col_title, unsafe_allow_html=True)
    fig = plot_aisle_rank_hist(missed_last_products)
    c1.pyplot(fig)
    c2.markdown('---')
    col_title = set_text_style('Распределение ранга внутри группы продуктов, '
                               'не попавших в рекомендации',
                               size=24, align='center')
    c2.markdown(col_title, unsafe_allow_html=True)
    fig = plot_in_aisle_rank_hist(missed_last_products)
    c2.pyplot(fig)

    st.markdown('---')
    # map10_value = set_text_style('MAP@10 = ', size=32, tag='span') + '**' + \
    #               set_text_style(f'{filled_up_map10:.6f} ', size=32, tag='span') + \
    #               set_text_style(f'▲{filled_up_map10 - total_map10:.6f}', size=24, color=InstacartColors.Lime,
    #                              tag='span') + '**'
    # st.markdown(map10_value, unsafe_allow_html=True)
