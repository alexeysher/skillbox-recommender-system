import streamlit as st
from auxiliary import connect_gcs, css_styling

# Google Cloud
GC_CREDENTIAL_INFO = st.secrets['gc-service-account'] # Credential info
GC_BUCKET_ID = st.secrets['gc-storage']['bucket_id'] # Bucket id
GC_BUCKET = connect_gcs(GC_CREDENTIAL_INFO, GC_BUCKET_ID) # Bucket
GC_DATA_PATH = 'data' # Data folder path


if __name__ == '__main__':

    st.set_page_config(page_title='Recommendation system for online hypermarket Instacart',
                       page_icon=':carrot:', layout='wide')

    css_styling()

    pages = [
        st.Page('sections/title.py', title="Title", default=True),
        st.Page('sections/objectives_and_tasks.py', title="Objective of the work"),
        st.Page('sections/data_description.py', title="Provided data description"),
        st.Page('sections/conception.py', title="Conception of the building model"),
        st.Page('sections/data_preprocessing.py', title="Data preprocessing"),
        st.Page('sections/model_building.py', title="Building a recommendation model"),
        st.Page('sections/kaggle_eval.py', title="Evaluation on Kaggle"),
        st.Page('sections/demo.py', title="Demo"),
    ]

    pg = st.navigation(pages)
    pg.run()
