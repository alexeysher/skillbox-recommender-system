import streamlit as st
import pandas as pd

st.title('Provided data description')
st.header('Product registry')
st.markdown('File: **products.csv**')
st.markdown('Fields:')
df = pd.DataFrame(
    {
        'name': ['product_id', 'product_name', 'aisle_id', 'department_id', 'aisle', 'department'],
        'description': [
            'product unique identifier',
            'product name',
            'aisle unique identifier',
            'department unique identifier',
            'aisle name',
            'department name'
        ]
    }
)
st.dataframe(df, hide_index=True)
st.markdown(
    '''
    Total numbers:
    - products: **49,688**
    - aisles: **134**
    - departments: **21**
    '''
)

st.header('Transaction log')
st.markdown('File name: **transactions.csv**')
st.markdown('Fields:')
df = pd.DataFrame(
    {
        'name': ['order_id', 'user_id', 'order_number', 'order_dow', 'order_hour_of_day', 'days_since_prior_order',
                 'product_id', 'add_to_cart_order', 'reordered'],
        'description': [
            'transaction unique identifier',
            'customer unique identifier',
            'customer''s order number',
            'day of week of order',
            'hour of order',
            'number of days since the previous order by the customer',
            'product identifier',
            'the order under which the product was added to the cart',
            'whether the product was in previous order'
        ]
    }
)
st.dataframe(df, hide_index=True)
st.markdown(
    '''
    Total numbers:
    - transactions: **26,408,073**
    - customers: **100,000**
    - purchased unique products: **49,465**
    '''
)

st.header('Remarks')
st.markdown(
    '''
    1. The dataset does not provide any useful information about the customers 
    such as gender, age, marital status, etc.
    2. Since the date and time of the next orders are unknown, information such as (`order_dow field`) 
    and order time (`order_hour_of_day`) are useless.
    3. Also useless is the information about the transaction ID (`order_id`) 
    and the reorder of the product (`reordered`).
    '''
)
