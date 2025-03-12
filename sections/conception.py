import streamlit as st
import altair as alt
import numpy as np
from main import GC_BUCKET, GC_DATA_PATH
from auxiliary import load_data_from_gcs, InstacartColors


@st.cache_resource(show_spinner='Plotting...')
def plot_reordering_prop():
    data = load_data_from_gcs('plot_reordering_prop_data.dmp', GC_BUCKET, GC_DATA_PATH)
    data['c'] = [InstacartColors.IllustrationBlue, InstacartColors.IllustrationPink]
    plot = alt.Chart(
        data
    ).mark_bar(
    ).encode(
        alt.X(
            'x',
            axis=alt.Axis(labelAngle=0),
            title='Category',
            sort=None
        ),
        alt.Y(
            'y',
            axis=alt.Axis(),
            title='Percentage'
        ),
        color=alt.Color(
            'c',
            scale=None
        ),
        tooltip=[
            alt.Tooltip('x', title='Category'),
            alt.Tooltip('y', title='Percentage', format='.2f')
        ]
    )
    return plot


@st.cache_resource(show_spinner='Plotting...')
def plot_reordering_hist():
    data = load_data_from_gcs('plot_reordering_percentages_data.dmp', GC_BUCKET, GC_DATA_PATH)
    data['tooltip'] = data['range'].map(
        lambda interval: f'{int(np.ceil(interval.left))} - {int(np.floor(interval.right))}')
    step = data.at[0, 'range'].right - data.at[0, 'range'].left
    plot = alt.Chart(
        data
    ).mark_bar(
        color=InstacartColors.IllustrationBlue,
        binSpacing=1
        # size=alt.Size()
    ).encode(
        alt.X(
            'reordered_percentage',
            axis=alt.Axis(labelAngle=0),
            title='Percentage',
            bin=alt.Bin(step=step)
        ),
        alt.Y(
            'max(number_of_customers)',
            axis=alt.Axis(),
            # scale=alt.Scale(domain=(15, 29)),
            title='Number of customers'
        ),
        tooltip=[
            alt.Tooltip('tooltip', title='Percentage'),
            alt.Tooltip('number_of_customers', title='Number of customers')
        ]
    )
    return plot


@st.cache_resource(show_spinner='Plotting...')
def plot_days_reordering():
    data = load_data_from_gcs('plot_days_reordering_data.dmp', GC_BUCKET, GC_DATA_PATH)
    data['tooltip'] = data['range'].map(
        lambda interval: f'{int(np.ceil(interval.left))} - {int(np.floor(interval.right))}')
    step = data.at[1, 'range'].right - data.at[1, 'range'].left
    base = alt.Chart(
        data,
    ).encode(
        x = alt.X(
            'order_time',
            axis=alt.Axis(format='.0f'),
            scale=alt.Scale(domain=(0, 360)),
            title='Time of order (in days before the last order)',
        ),
        y = alt.Y(
            'reordered_percentage',
            axis=alt.Axis(),
            # scale=alt.Scale(domain=(15, 30)),
            title='Percentage'
        ),
        tooltip = [
            alt.Tooltip('tooltip', title='Time of order'),
            alt.Tooltip('reordered_percentage', title='Percentage', format='.2f')
        ]
    )
    bar = base.mark_bar(
        color=InstacartColors.IllustrationBlue,
        opacity=0.25,
        filled=False,
        binSpacing=1
        # width = 20
    ).encode(
        x = alt.X('order_time', bin=alt.Bin(step=step))
    )
    line = base.mark_line(
        color=InstacartColors.IllustrationBlue,
        strokeWidth=4
    )
    plot = bar + line
    return plot


@st.cache_resource(show_spinner='Plotting...')
def plot_cart_reordering():
    data = load_data_from_gcs('plot_cart_reordering_data.dmp', GC_BUCKET, GC_DATA_PATH)
    data['tooltip'] = data['range'].map(
        lambda interval: f'{int(np.ceil(interval.left))} - {int(np.floor(interval.right))}')
    step = data.at[1, 'range'].right - data.at[1, 'range'].left
    base = alt.Chart(data).encode(
        alt.X(
            'add_to_cart_order',
            axis=alt.Axis(format='.0f'),
            scale=alt.Scale(domain=(1, 21)),
            title='Product add to cart order',
        ),
        alt.Y(
            'reordered_percentage',
            axis=alt.Axis(),
            # scale=alt.Scale(domain=(15, 29)),
            title='Percentage'
        ),
        tooltip = [
            alt.Tooltip('tooltip', title='Add to cart order'),
            alt.Tooltip('reordered_percentage', title='Percentage', format='.2f')
        ]
    )
    bar = base.mark_bar(
        color=InstacartColors.IllustrationPink,
        opacity=0.25,
        filled=False,
        binSpacing=1
        # width = 20
    ).encode(
        x = alt.X('add_to_cart_order', bin=alt.Bin(step=step))
    )
    line = base.mark_line(
        color=InstacartColors.IllustrationPink,
        strokeWidth=4
    )
    plot = bar + line
    return plot


st.markdown(
    '''
    # Design a conception of recommendation model
    
    ## Hypothesis for model design
    
    The store sells food. 
    An important feature of food sales is that people tend to buy about the same products. 
    Of course, sometimes customers' preferences change, they try new products. 
    But changes in product preferences occur systematically. 
    I.e. the basic set of products is quite stable. 
    Of course, in the lives of people periodically occur various events (birthdays, visitors, travel, etc.), 
    which affect the grocery pack they buy. But for most people, these events don’t happen very often. 
    So suppose that by detecting the set of products that the customer has most often ordered, especially recently, 
    we can understand what products should be offered to him to buy.
    Attention should also be paid to the order in which products are added to the basket. 
    This feature may indirectly indicate the importance of a product to the customer. 
    We usually put the most important products in the basket first.
    
    ## Statistical analysis of data
    
    ### Repeatability of purchased products
    
    To confirm the hypothesis, will perform a statistical analysis of the data. 
    First, will find out what part of the products from the customers' last order were purchased by them earlier.
    To do this, for each product of the last order of each customer, 
    will find the orders of this customer in which it was previously encountered.
    
    Then, for each customer, will find the percentage of products from the last order 
    that he or she has already purchased before, and display the distribution of this value using a histogram.
    '''
)

c1, c2 = st.columns([40, 60], gap='medium')
with c1:
    with st.container(border=True):
        text = 'Percentage of products in recent order depending on presence in previous orders'
        st.markdown(text)
        chart = plot_reordering_prop()
        st.altair_chart(chart)
with c2:
    with st.container(border=True):
        text = 'Distribution of percentage of previously purchased products in recent order'
        st.markdown(text)
        chart = plot_reordering_hist()
        st.altair_chart(chart)

st.markdown(
    '''
    #### Conclusion
    
    The histograms clearly shows that the vast majority of products in the customers' latest order 
    had already been ordered by them before. That is, the assumption that customers mostly buy products 
    that they have bought before has been confirmed.
    
    ### Customer preferences are changing slowly
    
    Will test the assumption that customers' product preferences may change over time, 
    and that this factor should be taken into account. 
    To do this, will plot a graph of the share of products in customers' orders 
    that are present in their latest orders, depending on the order time, with an interval of 1 month.
    '''
)

with st.columns([20, 60, 20])[1]:
    with st.container(border=True):
        st.markdown('Dependence of percentage of products present in orders depending on the order time')
        chart = plot_days_reordering()
        st.altair_chart(chart)

st.markdown(
    '''
    #### Conclusion

    The chart clearly shows that there is indeed a tendency for customer preferences to change over time. 
    Thus, the percentage of products that were ordered month before the last order 
    and are present in the last order is **28%**. 
    But the percentage of presence in the last order of products purchased almost year ago 
    is almost two times less - about **15%**.

    ### Customers add regularly purchased products to their cart first

    Next, will test another assumption that the serial number of adding a product 
    to the cart reflects its importance to the customer, and that this feature can be used to form predictions. 
    To do this, we will plot a graph of the share of products in customer orders that are present in their last order, 
    depending on the serial number of products in the cart.    
    '''
)

with st.columns([20, 60, 20])[1]:
    with st.container(border=True):
        st.markdown('Dependence of percentage of products present in subsequent '
                    'orders depending on add to cart number')
        chart = plot_cart_reordering()
        st.altair_chart(chart)

st.markdown(
    '''
    #### Conclusion

    The chart clearly shows that products from the last order were often among the first 
    to be added to the cart in previous orders. Thus, the share of products that were added to the cart first 
    and are present in the last order is about **28.5%**. 
    But the share of products present in the last order and added to the cart **21** 
    is almost two times less - about **15.5%**. So **this feature** should be used while model building.
    '''
)
