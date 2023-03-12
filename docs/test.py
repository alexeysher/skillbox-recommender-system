from pathlib import Path
import matplotlib.pyplot as plt
import streamlit as st
from auxilary import InstacartColors, set_text_style

DATA_PATH = Path('D:/skillbox-recommender-system/data')  # Путь к папке данных


@st.cache_data
def load_data():
    global DATA_PATH
    from pickle import load

    data = []
    for file_name in [
        'test_results.dmp',
    ]:
        file_path = DATA_PATH / file_name
        with open(file_path, 'rb') as fp:
            data.append(load(fp))
    return data


def main():
    st.markdown('**' + set_text_style('Результаты проверки на платформе Kaggle', size=48, color=InstacartColors.Carrot,
                                      align='center') + '**', unsafe_allow_html=True)
    test_result, = load_data()
    # test_result_styler = test_result.set_index('description')[['publicScore', 'privateScore', 'meanScore']]\
    #     .style.highlight_max(color=InstacartColors.Carrot)
    # st.table(test_result_styler, use_container_width=True)
    table = '''
| Тип обработки | publicScore | privateScore | meanScore |
|---------------|-------------|--------------|-----------|
'''
    for _, (description, publicScore, privateScore, meanScore) \
            in test_result[['description', 'publicScore', 'privateScore', 'meanScore']].iloc[:-1].iterrows():
        table += f'|{description}|{publicScore:.5f}|{privateScore:.5f}|{meanScore:.5f}|\n'
    description, publicScore, privateScore, meanScore = \
        test_result[['description', 'publicScore', 'privateScore', 'meanScore']].iloc[-1]
    table += f'|**:orange[{description}]**|**:orange[{publicScore:.5f}]**' \
             f'|**:orange[{privateScore:.5f}]**|**:orange[{meanScore:.5f}]**|'
    st.markdown(table)

    st.markdown('---')

    test_result['color'] = InstacartColors.IllustrationBlue
    test_result.at[test_result['meanScore'].idxmax(), 'color'] = InstacartColors.Carrot
    fig, ax = plt.subplots(facecolor=InstacartColors.Cashew, figsize=(8, 3))
    test_result.plot(
        ax=ax,
        kind='barh', x='description', y='meanScore', color=test_result['color'],
        title={}, xlabel='', ylabel='',
        grid=True, fontsize=10, legend=False)
    ax.set_xlabel('$MAP@10$')
    _ = ax.set_xlim(0.27, 0.33)
    st.pyplot(fig)
