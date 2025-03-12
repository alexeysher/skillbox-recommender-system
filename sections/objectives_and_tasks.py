import streamlit as st

st.markdown(
    '''
    # Objective of the work
    
    ## What Instacart is?
    Instacart, a grocery ordering and delivery app, is designed to make it easier 
    to stock your fridge with your favorite items when you need them.
    After a customer selects items through the app, Instacart employees check the order, 
    make the purchases, and deliver them from the store to the customer's home.
    The list of products and items is huge and it can be difficult to find something. 
    That's why Instacart wants to help the customer and show them the products they are most likely to want to buy.
    
    ## What does Instacart want to get?
    The goal of the work is to develop a recommender system that will predict 
    which products your customers will order next. The system should use anonymized customer order history 
    (transaction log) to make predictions.
    
    ## How Instacart will assess the work
    The work will be evaluated base on the precision of predictions using MAP@10 metric. 
    The minimal acceptable value of this metric is 0.20954.
    '''
)