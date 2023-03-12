import streamlit as st
from auxilary import set_text_style, InstacartColors


def main():
    # font_formatted_text = set_text_style('Цели и задачи', size=48, color=InstacartColors.Carrot)
    # st.markdown(font_formatted_text, unsafe_allow_html=True)

    font_formatted_text = set_text_style('Как работает', tag='span', color=InstacartColors.Carrot)
    font_formatted_text += ' Instacart?'
    font_formatted_text = '**' + set_text_style(font_formatted_text, size=48) + '**'
    st.markdown(font_formatted_text, unsafe_allow_html=True)

    font_formatted_text = 'Предоставляет услуги по '
    font_formatted_text += set_text_style("заказу", tag='span', color=InstacartColors.Carrot)
    font_formatted_text += ' и доставке '
    font_formatted_text += set_text_style("продуктов питания", tag='span', color=InstacartColors.Carrot)
    font_formatted_text += ' через мобильное приложение и веб-сайт.'
    font_formatted_text = set_text_style(font_formatted_text, size=32)
    st.markdown(font_formatted_text, unsafe_allow_html=True)

    st.markdown(set_text_style('&nbsp;', size=32), unsafe_allow_html=True)

    font_formatted_text = set_text_style('Что нужно', tag='span', color=InstacartColors.Carrot)
    font_formatted_text += ' Instacart?'
    font_formatted_text = '**' + set_text_style(font_formatted_text, size=48) + '**'
    st.markdown(font_formatted_text, unsafe_allow_html=True)

    font_formatted_text = set_text_style("Предложить", tag='span', color=InstacartColors.Carrot)
    font_formatted_text += ' пользователю те '
    font_formatted_text += set_text_style("продукты", tag='span', color=InstacartColors.Carrot)
    font_formatted_text += ', которые он, скорее всего, '
    font_formatted_text += set_text_style("захочет", tag='span', color=InstacartColors.Carrot)
    font_formatted_text += ' купить.'
    font_formatted_text = set_text_style(font_formatted_text, size=32)
    st.markdown(font_formatted_text, unsafe_allow_html=True)
