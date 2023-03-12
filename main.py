import streamlit as st
from streamlit_option_menu import option_menu
from auxilary import hide_menu_button, remove_blank_space, set_text_style, InstacartColors


# from docs import intro, goals, features, filtering, filling, test,

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


st.set_page_config(layout='wide')
hide_menu_button()
remove_blank_space()

with st.sidebar:
    choice = option_menu(
        '',
        options=[
            "Вступление",
            "Цели и задачи",
            "Особенности",
            "Фильтрация",
            "Заполнение",
            "Тестирование",
            "---",
            "Прототип"
        ],
        icons=[
            "",
            "map",
            "cart4",
            "filter",
            "droplet",
            "check-square",
            "",
            "people",
        ],
        orientation='vertical',
        # styles={"container": {"padding": "5!important", "background-color": "#fafafa"}},
        key='main_menu'
    )

match choice:
    case "Вступление":
        intro()
    # case "Цели и задачи":
    #     goals.main()
    # case "Особенности":
    #     features.main()
    # case "Фильтрация":
    #     filtering.main()
    # case "Заполнение":
    #     filling.main()
    # case "Тестирование":
    #     test.main()
    # case "Прототип":
    #     proto.main()
