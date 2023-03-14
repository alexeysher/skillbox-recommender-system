import streamlit as st


class InstacartColors:
    Cashew = '#FAF1E5'
    Carrot = '#FF7009'
    Kale = '#003D29'
    Lime = '#0AAD0A'
    Pomegranate = '#BA0239'
    Guava = '#FF7A9B'
    Cinnamon = '#C22F00'
    Turmeric = '#ECAA01'
    PlusPlum = '#750046'
    PlusBerry = '#B9017A'
    IllustrationRed = '#F6443A'
    IllustrationBlue = '#5D5FEF'
    IllustrationBlush = '#FFC6D0'
    IllustrationYellow = '#FDE801'
    IllustrationPink = '#FF90F7'


def set_text_style(text: str, tag: str = 'p', font_family: str = None, font_size: int = None,
                   color: str = None, background_color: str = None, text_align: str = None):
    variables = []
    if font_family is not None:
        variables.append(f'font-family: {font_family}')
    if font_size is not None:
        variables.append(f'font-size: {font_size}px')
    if color is not None:
        variables.append(f'color: {color}')
    if background_color is not None:
        variables.append(f'background-color: {background_color}')
    if text_align is not None:
        variables.append(f'text-align: {text_align}')
    variables.append('')
    style = '; '.join(variables)
    return f'<{tag} style="{style}">{text}</{tag}>'


def hide_menu_button():
    """
    Скрывает кнопку вызова меню.
    """
    st.markdown(
        """
        <style>
            MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True
    )


def remove_blank_space():
    """
    Удаляет пустое пространство вверху страницы.
    """
    st.markdown(f'''
                <style>
                    .css-k1ih3n {{
                        padding-top: 1.5rem;
                    }}
                </style>
                <style>
                    .css-1vq4p4l {{
                        padding-top: 4.0rem;
                    }}
                </style>
                ''', unsafe_allow_html=True,
                )
