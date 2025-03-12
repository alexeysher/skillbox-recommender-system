import streamlit as st
from auxiliary import InstacartColors

st.markdown(
    f'''<p style="font-size: 5rem;"><br><b>Recommendation system for online hypermarket Instacart</b></p>
        <p style="font-size: 4rem;">
            <span style="color: {InstacartColors.Kale}">Author: </span>
            <span style="color: {InstacartColors.Carrot}"><b>Alexey Sherstobitov</b></span>
        </p>
    ''',
unsafe_allow_html=True)
