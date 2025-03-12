import streamlit as st

st.markdown(
    '''
    # Data preprocessing
    
    According to the proposed hypnosis to predict purchases you need to take into account 
    the history of purchases of products. This requires a time stamp of shopping. 
    However, in the original dataset there is only information about the number of days between purchases 
    (`days_since_prior_oder`). 
    Therefore, an absolute time scale of orders cannot be retrieved, 
    but only a relative one. 
    Because, according to the concept, 
    it is important to know how long ago the other purchases were made relative to the planned, 
    then the timeline should be counted from the last known purchase. 
    To do this, add a feature to the transaction log, 
    which will show the number of days from each purchase of the customer to his last purchase 
    (`days_before_last_order`). And further by ***order time*** we mean just ***value of this feature***.
    
    Additionally, will consider orders made on the same day as one order. 
    Will combine the products present in them, and make the order of adding to the cart continuous. 
    Will assume that the customer first added orders from the first order to the cart, then from the second, etc.
    
    After processing, the **transaction log** will have the following fields:
    - `user_id` - unique buyer identifier
    - `days_before_last_order` - number of days since the previous transaction was made by this customer
    - `product_id` - unique product identifier
    - `add_to_cart_order` - number under which this product was added to the cart

    Will train the model on all customer transactions except the latest ones. 
    And will check the quality of its work on the latest transactions. Therefore, 
    will immediately divide the transaction log into two parts:
    - the latest transactions, on which we will evaluate the quality of predictions (`last_transactions`)
    - previous transactions, on the basis of which we will form the model's predictions (`prior_transactions`).
    
    In addition, to evaluate the accuracy of the model's predictions during validation, 
    a list of products in the latest purchases (`last_products`) will be required.
    '''
)