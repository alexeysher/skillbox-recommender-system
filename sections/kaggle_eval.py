import streamlit as st
from auxiliary import load_data_from_gcs, InstacartColors
from main import GC_BUCKET, GC_DATA_PATH
import pandas as pd


@st.cache_resource(show_spinner='Loading...')
def load_test_results():
    data = load_data_from_gcs('test_results.dmp', GC_BUCKET, GC_DATA_PATH)
    return data


@st.cache_resource(show_spinner='Loading...')
def load_filled_up_map10():
    data = load_data_from_gcs('filled_up_map10.dmp', GC_BUCKET, GC_DATA_PATH)
    return data


test_results = load_test_results()
filled_up_map10 = load_filled_up_map10()

st.title('Results of evaluation on the Kaggle platform')
table = test_results.loc[:, ['description', 'publicScore', 'privateScore', 'meanScore']]
table['previous_meanScore'] = [None, *table['meanScore'].iloc[:-1].to_list()]
table['change'] = table['meanScore'] - table['previous_meanScore']
table.drop(columns=['previous_meanScore'], inplace=True)
column_config = {
    'description': st.column_config.TextColumn('Processing type'),
    'publicScore': st.column_config.NumberColumn('Public Score', format='%.6f'),
    'privateScore': st.column_config.NumberColumn('Private Score', format='%.6f'),
    'change': st.column_config.NumberColumn('Change', format='%+.6f'),
    'meanScore': st.column_config.ProgressColumn(
        'Mean Score',
        width='large',
        format='%.6f',
        min_value=0.275, max_value=0.33
    ),
}

table = table.style.set_properties(
    **{'background-color': InstacartColors.Carrot}, subset=pd.IndexSlice[4])
st.dataframe(table, column_config=column_config, hide_index=True)

st.markdown(
    f'''
    1. Simple filtering by purchase frequency already provides the required prediction accuracy 
       ({test_results.at[0, "meanScore"]:.6f} > 0.25).
    2. Other types of filtering significantly improve the result (up to {test_results.at[4, "meanScore"]:.6f}). 
       The main increase in accuracy was provided by filtering by purchase time 
       (+{(test_results.at[1, "meanScore"] - test_results.at[0, "meanScore"]):.6f}).
       A little filtering is added by the adding to the cart order of the product and its popularity 
       (+{(test_results.at[2, "meanScore"] - test_results.at[1, "meanScore"]):.6f} and 
       +{(test_results.at[3, "meanScore"] - test_results.at[2, "meanScore"]):.6f} respectively).
    3. Filling in missing products made an insignificant contribution 
       (+{(test_results.at[4, "meanScore"] - test_results.at[3, "meanScore"]):.6f}).
    4. The accuracy of the model\'s predictions on test data ({test_results.at[4, "meanScore"]:.6f}) 
       is comparable to the accuracy shown during validation on training data ({filled_up_map10:.6f}).
       This means that the algorithm of the model is quite functional, and the model itself is well trained.
    '''
)
