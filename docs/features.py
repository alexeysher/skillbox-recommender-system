from pathlib import Path
import streamlit as st
from auxiliary import set_text_style, InstacartColors

DATA_PATH = Path('D:/skillbox-recommender-system/data')  # Путь к папке данных


@st.cache_data
def load_data():
    global DATA_PATH
    from pickle import load

    data = []
    for file_name in [
        'prior_transactions.dmp',
        'products_reordering.dmp',
        'products_reordering_percentages.dmp',
    ]:
        file_path = DATA_PATH / file_name
        with open(file_path, 'rb') as fp:
            data.append(load(fp))
    return data


@st.cache_resource
def plot_reordering_prop(products_reordering):

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
    import matplotlib.pyplot as plt
    from auxilary import InstacartColors

    fig, ax = plt.subplots(facecolor=InstacartColors.Cashew)
    _, _, bars = ax.hist(products_reordering_percentages['reordered_percentage'], bins=20)
    # .plot(
    #     ax=ax,
    #     kind='hist', bins=20,
    #     legend=False)
    # ax.set_facecolor(InstacartColors.Cashew)
    # ax.set_title('Распределение долей\nпокупавшихся ранее продуктов',
    #              fontfamily='sans serif', fontsize=16, fontweight='bold', color=InstacartColors.Kale)
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
def plot_days_reordering(prior_transactions, products_reordering):
    import matplotlib.pyplot as plt
    import numpy as np
    from auxilary import InstacartColors

    fig, ax = plt.subplots(facecolor=InstacartColors.Cashew)
    x = prior_transactions['days_before_last_order'] + prior_transactions['days_before_last_order_shift']
    nbins = int(np.ceil((x.max() - x.min()) / 30))
    total_counts, bins, _ = ax.hist(x, bins=nbins)
    ax.clear()
    x = products_reordering['days_before_last_order']
    reordered_counts, _, _ = ax.hist(x, bins=nbins)
    ax.clear()
    x = [(x1 + x2) / 2 for x1, x2 in zip(bins[:-1], bins[1:])]
    y = [reordered_count / total_count * 100 for total_count, reordered_count in zip(total_counts, reordered_counts)]
    line, = ax.plot(x, y)
    line.set_linewidth(4)
    # line.set_alpha(0.75)
    line.set_color(InstacartColors.IllustrationBlue)
    ax.set_xlabel('Время заказа [дни]', fontfamily='sans serif', fontsize=14, color=InstacartColors.Kale)
    ax.set_ylabel('Доля продуктов [%]', fontfamily='sans serif', fontsize=14, color=InstacartColors.Kale)
    ax.grid()
    return fig


@st.cache_resource
def plot_cart_reordering(prior_transactions, products_reordering):
    import matplotlib.pyplot as plt
    from auxilary import InstacartColors

    fig, ax = plt.subplots(facecolor=InstacartColors.Cashew)
    x = prior_transactions['add_to_cart_order']
    nbins = int(x.max() - x.min())
    total_density, bins, _ = ax.hist(x, bins=nbins, density=True)
    add_to_cart_max = sum(total_density >= 0.01)
    bins = bins[:add_to_cart_max + 1]
    ax.clear()
    total_counts, _, _ = ax.hist(x, bins=nbins)
    total_counts = total_counts[:add_to_cart_max]
    ax.clear()
    x = products_reordering['add_to_cart_order']
    reordered_counts, _, _ = ax.hist(x, bins=nbins)
    reordered_counts = reordered_counts[:add_to_cart_max]
    ax.clear()
    x = [(x1 + x2) / 2 for x1, x2 in zip(bins[:-1], bins[1:])]
    y = [reordered_count / total_count * 100 for total_count, reordered_count in zip(total_counts, reordered_counts)]
    line, = ax.plot(x, y)
    line.set_color(InstacartColors.IllustrationPink)
    line.set_linewidth(4)
    # line.set_alpha(0.75)
    ax.set_xlabel('Номер', fontfamily='sans serif', fontsize=14, color=InstacartColors.Kale)
    ax.set_ylabel('Доля продуктов [%]', fontfamily='sans serif', fontsize=14, color=InstacartColors.Kale)
    ax.grid()
    return fig


def main():
    prior_transactions, products_reordering, products_reordering_percentages = load_data()

    # Повторяемость
    title = '**' + set_text_style('Повторяемость', size=48, color=InstacartColors.Carrot, align='center') + '**'
    st.markdown(title, unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap='large')
    col_title = set_text_style('Соотношение продуктов в зависимости от присутствия в предыдущих заказах',
                               size=24, align='center')
    c1.markdown(col_title, unsafe_allow_html=True)
    col_title = set_text_style('Распределение долей покупавшихся ранее продуктов в последних заказах',
                               size=24, align='center')
    c2.markdown(col_title, unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap='large')
    fig = plot_reordering_prop(products_reordering)
    c1.pyplot(fig)
    fig = plot_reordering_hist(products_reordering_percentages)
    c2.pyplot(fig)

    # Плавное изменение и Сначала важные
    c1, c2 = st.columns(2, gap='large')
    c1.markdown('---')
    c2.markdown('---')
    col_title = '**' + set_text_style('Плавное изменение', size=48, color=InstacartColors.Carrot, align='center') + '**'
    c1.markdown(col_title, unsafe_allow_html=True)
    col_title = '**' + set_text_style('Сначала важные', size=48, color=InstacartColors.Carrot, align='center') + '**'
    c2.markdown(col_title, unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap='large')
    col_title = set_text_style('Зависимость доли продуктов, присутствующих в последующих заказах, '
                               'в зависимости от времени заказа', size=24, align='center')
    c1.markdown(col_title, unsafe_allow_html=True)
    col_title = set_text_style('Зависимость доли продуктов, присутствующих в последующих заказах, '
                               'в зависимости от номера добавления продукта в корзину', size=24, align='center')
    c2.markdown(col_title, unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap='large')
    fig = plot_days_reordering(prior_transactions, products_reordering)
    c1.pyplot(fig)
    fig = plot_cart_reordering(prior_transactions, products_reordering)
    c2.pyplot(fig)
