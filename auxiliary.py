import streamlit as st
from google.cloud import storage
from google.oauth2 import service_account
from pickle import load
from pathlib import Path


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


def connect_gcs(
        credential_info,
        bucket_id: str,
) -> storage.Bucket:
    """
    Establish connection to Bucket with given ID on Google Cloud Storage using given Credentials
    """
    credentials = service_account.Credentials.from_service_account_info(credential_info)
    storage_client = storage.Client(credential_info['project_id'], credentials=credentials)
    return storage_client.bucket(bucket_id)


def load_data_from_gcs(file_name: str, bucket: storage.Bucket, data_path: str):
    """
    Loads data from dump-file in given Bucket on Google Cloud Storage
    """
    file_path = f'{data_path}/{file_name}'
    blob = bucket.blob(file_path)
    blob.download_to_filename(file_name)
    with open(file_name, 'rb') as fp:
        data = load(fp)
    Path(file_name).unlink()
    return data


def css_styling():
    """
    Styles UI.
    """
    st.html(f"""
    <style>
        MainMenu {{visibility: hidden;}}
        # header {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        .st-emotion-cache-t1wise {{
            padding-top: 3.5rem;
        }}
        .st-emotion-cache-zxxjvx h1 {{
            color: {InstacartColors.Carrot};
            # font-size: 2.5rem;
            # font-weight: strong;
            # padding: 1.25rem 0px 1rem;
        }}
        .st-emotion-cache-zxxjvx h2 {{
            color: {InstacartColors.Carrot};
            # font-size: 2.0rem;
            # padding: 1rem 0px;
        }}
        .st-emotion-cache-zxxjvx h3 {{
            # font-size: 1.5rem;
            # padding: 0.5rem 0px 1rem;
        }}
        .st-emotion-cache-zxxjvx h4 {{
            font-size: 1.5rem;
            padding: 0.5rem 0px 1rem;
        }}
        # .st-emotion-cache-zxxjvx p {{
        #     word-break: break-word;
        #     margin-top: 0px;
        #     margin-left: 0px;
        #     margin-right: 0px;
        # }}
        .st-emotion-cache-zxxjvx {{
            font-size: 1.0rem;
        }}
        # dataframe {{
        #     font-size: 16px;
        # }}
    </style>
    """)


def hide_menu_button():
    """
    Hides the menu button.
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
    Removes white space at the top of the page.
    """
    st.markdown(
        '''
        <style>
            .st-emotion-cache-t1wise {
                padding-top: 1.5rem;
            }
        </style>
        ''',
        unsafe_allow_html=True,
    )
