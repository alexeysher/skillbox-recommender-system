import streamlit as st
import pandas as pd
from pathlib import Path
import time

import recommender
from main import GC_BUCKET, GC_DATA_PATH


@st.cache_resource(show_spinner='Loading...')
def load_recommender(bucket=GC_BUCKET, data_path: str = GC_DATA_PATH) -> recommender.Recommender:
    file_names = (
        'days.pkl', 'cart.pkl', 'total.pkl',
        'weights.zip', 'ratings.zip', 'aisle_ranks.zip', 'inside_aisle_ranks.zip',
        'products.zip'
    )

    for file_name in file_names:
        file_path = f'{data_path}/model/{file_name}'
        blob = bucket.blob(file_path)
        blob.download_to_filename(file_name)

    model = recommender.Recommender()
    model.load('.')

    for file_name in file_names:
        Path(file_name).unlink()

    return model


@st.cache_data(show_spinner='Generating recommendations...')
def get_recommendation(_recommender: recommender.Recommender,
                       user_ids: int|list[int]|None=None, k: int=10) -> pd.DataFrame:
    return _recommender.recommend(user_ids, k)


def execute_recommendation():
    start_time = time.time()
    st.session_state.user_id = st.session_state.selected_user_id
    st.session_state.k = st.session_state.selected_k
    st.session_state.recommendation = get_recommendation(model, st.session_state.user_id, st.session_state.k)
    end_time = time.time()
    st.session_state.exec_time = end_time - start_time
    st.session_state.recommendation.index.name = 'ID'
    st.session_state.recommendation.columns = [f'#{i}' for i in range(1, st.session_state.k + 1)]
    return


st.title('Recommendation system demo')
model = load_recommender()
st.header('Settings')
c1, c2, c3 = st.columns([50, 15, 35])
with c1:
    if 'user_id_multiselect' not in st.session_state:
        if 'selected_user_id' not in st.session_state:
            st.session_state.default_user_id = []
        else:
            st.session_state.default_user_id = st.session_state.selected_user_id
    st.session_state.selected_user_id = st.multiselect(
        'Customer IDs', model.users,
        default=st.session_state.default_user_id,
        placeholder=f'All customers ({len(model.users)})',
        key='user_id_multiselect'
    )
with c2:
    if 'k_number_input' not in st.session_state:
        if 'selected_k' not in st.session_state:
            st.session_state.default_k = 10
        else:
            st.session_state.default_k = st.session_state.selected_k
    st.session_state.selected_k = st.number_input(
        'Size of recommendations', 1, 10, value=st.session_state.default_k, key='k_number_input'
    )

st.header('Recommendations')
c1, c2, _ = st.columns([15, 15, 70])
with c1:
    if 'user_id' not in st.session_state:
        st.session_state.user_id = [0]
    if 'k' not in st.session_state:
        st.session_state.k = 0
    disabled = (st.session_state.selected_user_id == st.session_state.user_id) \
               and (st.session_state.selected_k == st.session_state.k)
    st.button('Get recommendations...', on_click=execute_recommendation,
              disabled=disabled)
if 'recommendation' not in st.session_state:
    execute_recommendation()
with c2:
    st.markdown(f'Execution time: **{st.session_state.exec_time:.3f}** s')
st.subheader('List of recommended products')
st.dataframe(st.session_state.recommendation, use_container_width=True)
