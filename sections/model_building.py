import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

from auxiliary import load_data_from_gcs, InstacartColors
from main import GC_BUCKET, GC_DATA_PATH

@st.cache_resource(show_spinner='Loading...')
def load_frequency_map10():
    data = load_data_from_gcs('frequency_map10.dmp', GC_BUCKET, GC_DATA_PATH)
    return data


@st.cache_resource(show_spinner='Plotting...')
def plot_ratings_hist():
    data = load_data_from_gcs('plot_ratings_hist_data.dmp', GC_BUCKET, GC_DATA_PATH)
    data = data.loc[data['rating'] <= 21]
    data['tooltip'] = data['range'].map(
        lambda interval: f'{int(np.ceil(interval.left))} - {int(np.floor(interval.right))}')
    step = data.at[1, 'range'].right - data.at[1, 'range'].left
    plot = alt.Chart(
        data
    ).mark_bar(
        color=InstacartColors.IllustrationBlue,
        binSpacing=1
    ).encode(
        alt.X(
            'rating',
            axis=alt.Axis(format='.0f'),
            # scale=alt.Scale(domain=(0, 11)),
            title='Rating',
            bin=alt.Bin(step=step)
        ),
        alt.Y(
            'max(number_of_products)',
            axis=alt.Axis(),
            # scale=alt.Scale(domain=(15, 29)),
            title='Number of products'
        ),
        tooltip=[
            alt.Tooltip('tooltip', title='Rating'),
            alt.Tooltip('number_of_products', title='Number of products')
        ]
    )
    return plot


@st.cache_resource(show_spinner='Loading...')
def load_days_rate():
    data = load_data_from_gcs('days_rate.dmp', GC_BUCKET, GC_DATA_PATH)
    return data


@st.cache_resource(show_spinner='Loading...')
def load_days_map10():
    data = load_data_from_gcs('days_map10.dmp', GC_BUCKET, GC_DATA_PATH)
    return data


@st.cache_resource(show_spinner='Plotting...')
def plot_days(best_rate: float, best_precision: float):
    data = load_data_from_gcs('plot_days_data.dmp', GC_BUCKET, GC_DATA_PATH)
    domain = ['actual', 'approximated']
    colors = [InstacartColors.IllustrationBlue, InstacartColors.IllustrationPink, InstacartColors.IllustrationRed]
    dashes = [[], [8, 4]]

    lines = alt.Chart(
        data
    ).mark_line(
        strokeWidth=4,
        interpolate='natural',
    ).encode(
        alt.X(
            'days_rate',
            axis=alt.Axis(),
            # scale=alt.Scale(domain=(1, 21)),
            title='Rate',
        ),
        alt.Y(
            'precision',
            axis=alt.Axis(),
            scale=alt.Scale(domain=(.275, .33)),
            title='MAP@10'
        ),
        color=alt.Color('type', title='', scale=alt.Scale(domain=domain, range=colors)),
        strokeDash=alt.StrokeDash('type', title='', scale=alt.Scale(domain=domain, range=dashes)),
    )

    best_data = pd.DataFrame.from_dict(
        {'x': [best_rate], 'y': [best_precision]}
    )
    x = alt.X('x', title='')
    x_tooltip = alt.Tooltip('x', title='Best rate', format='.4f')
    y = alt.Y('y', title='')
    y_tooltip = alt.Tooltip('y', title='Best MAP@10', format='.6f')

    circle = alt.Chart(
        best_data
    ).mark_circle(
        color=InstacartColors.IllustrationRed, size=80
    ).encode(
        x=x, y=y, tooltip = [x_tooltip, y_tooltip]
    )

    x_rule = alt.Chart(
        best_data
    ).mark_rule(
        color=InstacartColors.IllustrationRed, strokeWidth=2, strokeDash = [4, 4]
    ).encode(
        x=x, tooltip=[x_tooltip]
    )

    y_rule = alt.Chart(
        best_data
    ).mark_rule(
        color=InstacartColors.IllustrationRed, strokeWidth=2, strokeDash = [4, 4]
    ).encode(
        y=y, tooltip=[y_tooltip]
    )

    plot = lines + circle + x_rule + y_rule

    return plot


@st.cache_resource(show_spinner='Plotting...')
def plot_days_hist():
    data = load_data_from_gcs('plot_days_hist_data.dmp', GC_BUCKET, GC_DATA_PATH)
    data = data.loc[data['rating'] <= 11]
    data['tooltip'] = data['range'].map(
        lambda interval: f'{int(np.ceil(interval.left))} - {int(np.floor(interval.right))}')
    step = data.at[1, 'range'].right - data.at[1, 'range'].left
    plot = alt.Chart(
        data
    ).mark_bar(
        color=InstacartColors.IllustrationBlue,
        binSpacing=1
    ).encode(
        alt.X(
            'rating',
            axis=alt.Axis(format='.0f'),
            # scale=alt.Scale(domain=(0, 11)),
            title='Rating',
            bin=alt.Bin(step=step)
        ),
        alt.Y(
            'max(number_of_products)',
            axis=alt.Axis(),
            # scale=alt.Scale(domain=(15, 29)),
            title='Number of products'
        ),
        tooltip=[
            alt.Tooltip('tooltip', title='Rating'),
            alt.Tooltip('number_of_products', title='Number of products')
        ]
    )
    return plot


@st.cache_resource(show_spinner='Loading...')
def load_cart_rate():
    data = load_data_from_gcs('cart_rate.dmp', GC_BUCKET, GC_DATA_PATH)
    return data


@st.cache_resource(show_spinner='Loading...')
def load_cart_map10():
    data = load_data_from_gcs('cart_map10.dmp', GC_BUCKET, GC_DATA_PATH)
    return data


@st.cache_resource(show_spinner='Plotting...')
def plot_cart(best_rate: float, best_precision: float):
    data = load_data_from_gcs('plot_cart_data.dmp', GC_BUCKET, GC_DATA_PATH)
    domain = ['actual', 'approximated']
    colors = [InstacartColors.IllustrationBlue, InstacartColors.IllustrationPink, InstacartColors.IllustrationRed]
    dashes = [[], [8, 4]]

    lines = alt.Chart(
        data
    ).mark_line(
        strokeWidth=4,
        interpolate='natural',
    ).encode(
        alt.X(
            'cart_rate',
            axis=alt.Axis(),
            # scale=alt.Scale(domain=(1, 21)),
            title='Rate',
        ),
        alt.Y(
            'precision',
            axis=alt.Axis(),
            scale=alt.Scale(domain=(.3248, .3268)),
            title='MAP@10'
        ),
        color=alt.Color('type', title='', scale=alt.Scale(domain=domain, range=colors)),
        strokeDash=alt.StrokeDash('type', title='', scale=alt.Scale(domain=domain, range=dashes)),
    )

    best_data = pd.DataFrame.from_dict(
        {'x': [best_rate], 'y': [best_precision]}
    )
    x = alt.X('x', title='')
    x_tooltip = alt.Tooltip('x', title='Best rate', format='.4f')
    y = alt.Y('y', title='')
    y_tooltip = alt.Tooltip('y', title='Best MAP@10', format='.6f')

    circle = alt.Chart(
        best_data
    ).mark_circle(
        color=InstacartColors.IllustrationRed, size=40
    ).encode(
        x=x, y=y, tooltip = [x_tooltip, y_tooltip]
    )

    x_rule = alt.Chart(
        best_data
    ).mark_rule(
        color=InstacartColors.IllustrationRed, strokeWidth=2, strokeDash = [4, 4]
    ).encode(
        x=x, tooltip=[x_tooltip]
    )

    y_rule = alt.Chart(
        best_data
    ).mark_rule(
        color=InstacartColors.IllustrationRed, strokeWidth=2, strokeDash = [4, 4]
    ).encode(
        y=y, tooltip=[y_tooltip]
    )

    plot = lines + circle + x_rule + y_rule

    return plot


@st.cache_resource(show_spinner='Plotting...')
def plot_cart_hist():
    data = load_data_from_gcs('plot_cart_hist_data.dmp', GC_BUCKET, GC_DATA_PATH)
    data = data.loc[data['rating'] <= 11]
    data['tooltip'] = data['range'].map(
        lambda interval: f'{int(np.ceil(interval.left))} - {int(np.floor(interval.right))}')
    step = data.at[1, 'range'].right - data.at[1, 'range'].left
    plot = alt.Chart(
        data
    ).mark_bar(
        color=InstacartColors.IllustrationBlue,
        binSpacing=1
    ).encode(
        alt.X(
            'rating',
            axis=alt.Axis(format='.0f'),
            # scale=alt.Scale(domain=(0, 11)),
            title='Rating',
            bin=alt.Bin(step=step)
        ),
        alt.Y(
            'max(number_of_products)',
            axis=alt.Axis(),
            # scale=alt.Scale(domain=(15, 29)),
            title='Number of products'
        ),
        tooltip=[
            alt.Tooltip('tooltip', title='Rating'),
            alt.Tooltip('number_of_products', title='Number of products')
        ]
    )
    return plot


@st.cache_resource(show_spinner='Loading...')
def load_total_rate():
    data = load_data_from_gcs('total_rate.dmp', GC_BUCKET, GC_DATA_PATH)
    return data


@st.cache_resource(show_spinner='Loading...')
def load_total_map10():
    data = load_data_from_gcs('total_map10.dmp', GC_BUCKET, GC_DATA_PATH)
    return data


@st.cache_resource(show_spinner='Plotting...')
def plot_total(best_rate: float, best_precision: float):
    data = load_data_from_gcs('plot_total_data.dmp', GC_BUCKET, GC_DATA_PATH)
    domain = ['actual', 'approximated']
    colors = [InstacartColors.IllustrationBlue, InstacartColors.IllustrationPink, InstacartColors.IllustrationRed]
    dashes = [[], [8, 4]]

    lines = alt.Chart(
        data
    ).mark_line(
        strokeWidth=4,
        interpolate='natural',
    ).encode(
        alt.X(
            'total_rate',
            axis=alt.Axis(titleFontSize=20, labelFontSize=16),
            # scale=alt.Scale(domain=(1, 21)),
            title='Rate',
        ),
        alt.Y(
            'precision',
            axis=alt.Axis(titleFontSize=20, labelFontSize=16),
            scale=alt.Scale(domain=(.3252, .3277)),
            title='MAP@10'
        ),
        color=alt.Color('type', title='', scale=alt.Scale(domain=domain, range=colors)),
        strokeDash=alt.StrokeDash('type', title='', scale=alt.Scale(domain=domain, range=dashes)),
    )

    best_data = pd.DataFrame.from_dict(
        {'x': [best_rate], 'y': [best_precision]}
    )
    x = alt.X('x', title='')
    x_tooltip = alt.Tooltip('x', title='Best rate', format='.4f')
    y = alt.Y('y', title='')
    y_tooltip = alt.Tooltip('y', title='Best MAP@10', format='.6f')

    circle = alt.Chart(
        best_data
    ).mark_circle(
        color=InstacartColors.IllustrationRed, size=80
    ).encode(
        x=x, y=y, tooltip = [x_tooltip, y_tooltip]
    )

    x_rule = alt.Chart(
        best_data
    ).mark_rule(
        color=InstacartColors.IllustrationRed, strokeWidth=2, strokeDash = [4, 4]
    ).encode(
        x=x, tooltip=[x_tooltip]
    )

    y_rule = alt.Chart(
        best_data
    ).mark_rule(
        color=InstacartColors.IllustrationRed, strokeWidth=2, strokeDash = [4, 4]
    ).encode(
        y=y, tooltip=[y_tooltip]
    )

    plot = lines + circle + x_rule + y_rule

    return plot


@st.cache_resource(show_spinner='Plotting...')
def plot_total_hist():
    data = load_data_from_gcs('plot_total_hist_data.dmp', GC_BUCKET, GC_DATA_PATH)
    data = data.loc[data['rating'] <= 11]
    data['tooltip'] = data['range'].map(
        lambda interval: f'{int(np.ceil(interval.left))} - {int(np.floor(interval.right))}')
    step = data.at[1, 'range'].right - data.at[1, 'range'].left
    plot = alt.Chart(
        data
    ).mark_bar(
        color=InstacartColors.IllustrationBlue,
        binSpacing=1
    ).encode(
        alt.X(
            'rating',
            axis=alt.Axis(titleFontSize=20, labelFontSize=16, labelAngle=0, format='.0f'),
            # scale=alt.Scale(domain=(0, 11)),
            title='Rating',
            bin=alt.Bin(step=step)
        ),
        alt.Y(
            'max(number_of_products)',
            axis=alt.Axis(titleFontSize=20, labelFontSize=16),
            # scale=alt.Scale(domain=(15, 29)),
            title='Number of products'
        ),
        tooltip=[
            alt.Tooltip('tooltip', title='Rating'),
            alt.Tooltip('number_of_products', title='Number of products')
        ]
    )
    return plot


@st.cache_resource(show_spinner='Plotting...')
def plot_missed_hist():
    data = load_data_from_gcs('plot_missed_hist_data.dmp', GC_BUCKET, GC_DATA_PATH)
    data = data.loc[data['total_rank'] <= 1001]
    data['tooltip'] = data['range'].map(
        lambda interval: f'{int(np.ceil(interval.left))} - {int(np.floor(interval.right))}')
    step = data.at[1, 'range'].right - data.at[1, 'range'].left
    plot = alt.Chart(
        data
    ).mark_bar(
        color=InstacartColors.IllustrationBlue,
        binSpacing=1
    ).encode(
        alt.X(
            'total_rank',
            axis=alt.Axis(format='.0f'),
            # scale=alt.Scale(domain=(0, 11)),
            title='Rank',
            bin=alt.Bin(step=step)
        ),
        alt.Y(
            'max(number_of_products)',
            axis=alt.Axis(),
            # scale=alt.Scale(domain=(15, 29)),
            title='Number of products'
        ),
        tooltip=[
            alt.Tooltip('tooltip', title='Rank'),
            alt.Tooltip('number_of_products', title='Number of products')
        ]
    )
    return plot


@st.cache_resource(show_spinner='Loading...')
def load_filled_up_map10():
    data = load_data_from_gcs('filled_up_map10.dmp', GC_BUCKET, GC_DATA_PATH)
    return data


@st.cache_resource
def plot_aisle_rank_hist():
    data = load_data_from_gcs('plot_aisle_rank_hist_data.dmp', GC_BUCKET, GC_DATA_PATH)
    data = data.loc[data['aisle_rank'] <= 25]
    data['tooltip'] = data['range'].map(
        lambda interval: f'{int(np.ceil(interval.left))} - {int(np.floor(interval.right))}')
    step = data.at[1, 'range'].right - data.at[1, 'range'].left
    plot = alt.Chart(
        data
    ).mark_bar(
        color=InstacartColors.IllustrationBlue,
        binSpacing=1
    ).encode(
        alt.X(
            'aisle_rank',
            axis=alt.Axis(format='.0f'),
            # scale=alt.Scale(domain=(0, 11)),
            title='Rank of group',
            bin=alt.Bin(step=step)
        ),
        alt.Y(
            'max(number_of_products)',
            axis=alt.Axis(),
            # scale=alt.Scale(domain=(15, 29)),
            title='Number of products'
        ),
        tooltip=[
            alt.Tooltip('tooltip', title='Rank of group'),
            alt.Tooltip('number_of_products', title='Number of products')
        ]
    )
    return plot


@st.cache_resource
def plot_in_aisle_rank_hist():
    data = load_data_from_gcs('plot_in_aisle_rank_hist_data.dmp', GC_BUCKET, GC_DATA_PATH)
    data = data.loc[data['inside_aisle_rank'] <= 25]
    data['tooltip'] = data['range'].map(
        lambda interval: f'{int(np.ceil(interval.left))} - {int(np.floor(interval.right))}')
    step = data.at[1, 'range'].right - data.at[1, 'range'].left
    plot = alt.Chart(
        data
    ).mark_bar(
        color=InstacartColors.IllustrationPink,
        binSpacing=1
    ).encode(
        alt.X(
            'inside_aisle_rank',
            axis=alt.Axis(format='.0f'),
            # scale=alt.Scale(domain=(0, 11)),
            title='Rank of product inside group',
            bin=alt.Bin(step=step)
        ),
        alt.Y(
            'max(number_of_products)',
            axis=alt.Axis(),
            # scale=alt.Scale(domain=(15, 29)),
            title='Number of products'
        ),
        tooltip=[
            alt.Tooltip('tooltip', title='Rank of product inside group'),
            alt.Tooltip('number_of_products', title='Number of products')
        ]
    )
    return plot


st.markdown(
    '''
    # Building a recommendation model
    
    ## Filtering by frequency of product purchases
    
    
    '''
)
st.markdown(
    '''
    In accordance with the chosen concept of the prediction model, 
    the rating of products for each customer should be primarily assessed 
    by the frequency of purchases by this customer. 
    In this case, products that the customer has never purchased will have a zero rating. 
    And for products that the customer has purchased, the rating 
    will be equal to the number of purchases of this product.
    
    This type of filtering can be described by the following formula:
    '''
)

with st.columns([30, 40, 30])[1]:
    st.latex('r_{u,i}=\sum_{t \in T_u}s_{u,i,t}')
    st.markdown(
        '''
        | Symbol      | Description                                                                                                      |
        | ----------- | ---------------------------------------------------------------------------------------------------------------- |
        | $r_{u,i}$   | Rating of product with number $i$ for user with number $u$                                                       |
        | $T_u$       | Transaction numbers made by user with number $u$                                                                 |
        | $s_{u,i,t}$ | Presence of product with number $i$ in transaction with number $t$ made by user with number $u$: $0$-no, $1$-yes |
        ''',
        unsafe_allow_html=True
    )

st.subheader('Rating distribution (through all products)')
with st.columns([20, 60, 20])[1]:
    with st.container(border=True):
        st.markdown('Distribution of previously purchased products by rating')
        chart = plot_ratings_hist()
        st.altair_chart(chart)

st.subheader('Result')
frequency_map_10 = load_frequency_map10()
st.markdown(
    f'''
    The value of the $MAP@10$ metric in this case is **{frequency_map_10:.6f}**.
    This is already an acceptable result. We will try to improve it with additional filtering.
    '''
)

st.markdown(
    '''
    ## Appending filtering by order time
    
    As a result of the exploratory analysis, it was confirmed that the existence 
    of a dependence of the share of purchased products included in the next order on the time of the order. 
    In this regard, the importance of orders should be reduced as they move away in time from the last order. 
    To do this, will introduce the concept of "weight" of a transaction, 
    which will depend on the time of its execution. 
    Rely on the appearance of the graph of the above dependence, it can be assumed that it is exponential in nature. 
    Therefore, we will reduce the transaction weights exponentially, i.e. will apply 
    the so-called exponential filtering, in which the transaction weights are determined by the formula:
    '''
)

with st.columns([29, 42, 29])[1]:
    st.latex('\large w_{u,t}=e^{-d_{u,t}·a_d}')
    st.markdown(
        '''
        | Symbol      | Description                                                                                                 |
        | ----------- | ----------------------------------------------------------------------------------------------------------- |
        | $w_{u,t}$   | Weight of transaction with number $t$ made by user with number $u$                                          |
        | $d_{u,t}$   | Order time of transaction with number $t$ made by user with number $u$                                       |
        | $a_d$       | Filtering rate (positive number)                                                                            |
        '''
    )

st.markdown(
    '''        
    In this case, the formula for calculating product ratings will take the following form:
    '''
)

with st.columns([22, 56, 22])[1]:
    x = st.latex('r_{u,i}=\sum_{t \in T_u}s_{u,i,t}·w_{u,t}=\sum_{t \in T_u}s_{u,i,t}·e^{-d_{u,t}·a_d}.')
    st.markdown(
        '''
        | Symbol      | Description                                                                                                 |
        | ----------- | ----------------------------------------------------------------------------------------------------------- |
        | $r_{u,i}$   | Rating of product with number $i$ for user with number $u$                                                  |
        | $T_u$       | Transaction numbers made by user with number $u$                                                            |
        | $s_{u,i,t}$ | Presence of product with number $i$ in transaction with number $t$ of user with number $u$: $0$-no, $1$-yes |
        | $w_{u,t}$   | Weight of transaction with number $t$ made by user with number $u$                                          |
        | $d_{u,t}$   | Time of transaction with number $t$ made by user with number $u$                                            |
        | $a_d$       | Filtering rate (positive number)                                                                            |
        '''
    )

st.markdown(
    '''
    To check the effect of filtering by purchase time and the influence of the value of the rate $a_d$ 
    on the accuracy of predictions using it, will plot a chart of the dependence 
    of the value of the metric $MAP@10$ on the value of this rate.
    '''
)

with st.columns([20, 60, 20])[1]:
    with st.container(border=True):
        st.markdown('Dependence of prediction accuracy on filtering rate')
        days_map10 = load_days_map10()
        days_rate = load_days_rate()
        chart = plot_days(days_rate, days_map10)
        st.altair_chart(chart)

st.markdown(
    f'''
    The chart shows that the value of the $a_d$ rate significantly affects the quality of filtration. 
    At values of this rate close to zero (i.e. at weak filtration), as it should be, 
    the value of the $MAP@10$ metric is close to the value obtained only on the basis of purchase frequency. 
    Then, as the rate grows, a rapid growth of the prediction quality is observed, 
    which reaches its peak at a value of the $a_d$ rate in the region of $0.015...0.02$. 
    As the rate value continues to grow, the quality of filtration** expectedly begins slowly decreasing 
    to the original value (the $MAP@10$ metric returns to the value obtained only on the basis of purchase frequency).
    
    Will try to determine the position and magnitude of the peak of this dependence more precisely. 
    To do this, we approximate the function on $[0, 0.1]$ of the $MAP@10(a_d)$ chart 
    using a 7th-order polynomial function. After that, will find a point on this segment where the derivative 
    of the polynomial function is zero. This will be the desired point of the refined position of the peak - 
    the optimal value of the $a_d$ rate. And then, at that point, will find the real value of the $MAP@10$ metric. 
    This value will characterize the accuracy of predictions when using time filtering.
    
    ### Result
    Filtering by purchase time gives a *significant increase in the accuracy* of predictions 
    (the $MAP@10$ metric increased by **{(days_map10 - frequency_map_10):.6f}** 
    from {frequency_map_10:.6f} to {days_map10:.6f}) 
    with the filter rate $a_d$ equal to **{days_rate:.6f}**.
    
    ### Note
    Of course, it would have been possible to further improve the accuracy of predictions 
    on training data by using time filtering for each customer separately and even for each product separately. 
    But in this case, our model would have a very low generalization ability, 
    i.e. the model would become heavily overfitted.
    
    ## Appending filtering by adding to cart order
    
    Using statistical analysis, it was confirmed the existence of a dependence of the share 
    of purchased products included in the next order, the share of purchased products included in the next order, 
    on the numbers of their addition to. 
    Will try to take this circumstance into account and reduce the weight of products with 
    an increase in the order of their addition to the basket. 
    Just as in the case of filtering by purchase time, will use exponential filtering. 
    And will also use a single rate for the products of all transactions of all customers. 
    As a result, each product of each transaction of each customer will have its own weight, 
    which is described by the following formula:
    '''
)

with st.columns([29, 42, 29])[1]:
    st.latex('w_{u,i,t} = e^{-d_{u,t} a_d} e^{-c_{u,i,t} a_c}')
    st.markdown(
        '''
        | Symbol      | Description                                                                                                 |
        | ----------- | ----------------------------------------------------------------------------------------------------------- |
        | $w_{u,t}$   | Weight of transaction with number $t$ made by user with number $u$                                          |
        | $d_{u,t}$   | Order time of transaction with number $t$ made by user with number $u$                                      |
        | $a_d$       | Filtering rate by transaction purchase time                                                                 |
        | $a_c$       | Filtering rate by order of adding to the cart                                                               |
        '''
    )

st.markdown(
    '''
    When adding this filtering, the formula for calculating ratings will take the following form:
    '''
)

with st.columns([22, 56, 22])[1]:
    st.latex('r_{u,i}=\sum_{t \in T_u}s_{u,i,t}·w_{u,i,t} = \sum_{t \in T_u}s_{u,i,t}·e^{-d_{u,t}·a_d}·e^{-c_{u,i,t}·a_c}')
    st.markdown(
        '''
        | Symbol      | Description                                                                                                 |
        | ----------- | ----------------------------------------------------------------------------------------------------------- |
        | $r_{u,i}$   | Rating of product with number $i$ for user with number $u$                                                  |
        | $T_u$       | Transaction numbers made by user with number $u$                                                            |
        | $s_{u,i,t}$ | Presence of product with number $i$ in transaction with number $t$ of user with number $u$: $0$-no, $1$-yes |
        | $w_{u,t}$   | Weight of transaction with number $t$ made by user with number $u$                                          |
        | $d_{u,t}$   | Time of transaction with number $t$ made by user with number $u$                                            |
        | $a_d$       | Filtering rate by transaction purchase time                                                                 |
        | $a_c$       | Filtering rate by order of adding to the cart                                                               |
        '''
    )

st.markdown(
    '''
    To check the effect of filtering by the adding to the cart order and the influence 
    of the value of the rate $a_c$ on the accuracy of predictions using it, 
    will plot a chart of the dependence of the value of the metric $MAP@10$ on the value of this rate.
    '''
)

with st.columns([20, 60, 20])[1]:
    with st.container(border=True):
        st.markdown('Dependence of prediction accuracy on filtering rate')
        cart_map10 = load_cart_map10()
        cart_rate = load_cart_rate()
        chart = plot_cart(cart_rate, cart_map10)
        st.altair_chart(chart)

st.subheader('Rating distribution (through all products)')
st.markdown('!!!')
with st.columns([20, 60, 20])[1]:
    with st.container(border=True):
        st.markdown('Distribution of previously purchased products by rating')
        chart = plot_days_hist()
        st.altair_chart(chart)

st.markdown(
    f'''
    The chart shows that the value of the rate $a_c$ affects the quality of filtration. 
    Thus, at values of this rate close to zero (i.e. at weak filtration), as it should be, 
    the value of the $MAP@10$ metric is close to the value obtained after applying frequency and time filtration. 
    Then, as the rates grow, a slight increase in the quality of filtration is observed, 
    which reaches its peak at a rate value in the region of 0.016...0.02. 
    As the value of the rate continues to grow, the quality of filtration begins to rapidly decrease. 
    And at rate values greater than 0.045, the effect of filtration becomes negative 
    (the $MAP@10$ metric falls below the value obtained by filtering by frequency and time).
    
    Will try to determine the position and value of the peak of this dependence more precisely. 
    To do this, on the segment $[0, 0.05]$ we approximate the function $MAP@10(a_d)$ 
    using a 3rd order polynomial function. After that, we find a point on this segment 
    at which the derivative of the polynomial function is zero. 
    This will be the desired point of the refined position of the peak - the optimal value of the rate $a_c$. 
    And then at that point we will find the real value of the metric $MAP@10$. 
    This value will characterize the accuracy of predictions when using filtering 
    by the adding a product to the cart order.
    
    #### Result
    Filtering by the product addition number to the cart gave a *small increase in the accuracy* of predictions
    (the $MAP@10$ metric increased by only {(cart_map10 - days_map10):.6f} 
    from {days_map10:.6f} to {cart_map10:.6f}) '
    with the filtering rate $a_c$ equal to {cart_rate:.6f}.
    
    ## Appending filtering by popularity
    
    For each product, in addition to the rating for a specific customer, you can determine its global rating, 
    which is the average rating of this product among all customers. This rating is calculated using the formula:
    '''
)

with st.columns([32, 36, 32])[1]:
    st.latex('r^g_i={\sum_{u \in U}r_{u,i} \over |U|}')
    st.markdown(
        '''
        | Symbol     | Description                                                |
        | ---------- | ---------------------------------------------------------- |
        | $r^g_i$    | Global rating of product with number $i$                   |
        | $r_{u,i}$  | Rating of product with number $i$ for user with number $u$ |
        | $U$        | Set of user numbers in transactions                        |
        '''
    )

st.markdown(
    '''
    Will try to analyze products with which global rating were mistakenly 
    not included in the recommendations based on the above filters:
    - First, we find global product ratings based on previous transactions.
    - Then we find a list of the most recently purchased products by customers 
      that were not included in the recommendations.
    - Next, will display the distribution of global rank among the most recently 
      purchased products by customers that were not included in the recommendations.
    '''
)

with st.columns([20, 60, 20])[1]:
    with st.container(border=True):
        st.markdown('Global rank distribution among products not included in the recommendations')
        chart = plot_missed_hist()
        st.altair_chart(chart)

st.markdown(
    '''
    The histogram shows that products with a high global rating are most often mistakenly 
    not included in the recommendations. Will try to take this circumstance into account 
    and adjust the model's operation. To do this, we will increase the ratings of popular products 
    (with high global ratings). Will call this rating adjustment "popularity filtering". 
    As before, we will build it on the basis of exponential filtering. 
    As a result, the product rating will be calculated using the following formula:
    '''
)

with st.columns([32, 36, 32])[1]:
    st.latex('r^*_{u,i}=r_{u,i}·e^{r^g_i·a_p}')
    st.markdown(
        '''
        | Symbol     | Description                                                |
        | ---------- | ---------------------------------------------------------- |
        | $r^g_i$    | Global rating of product with number $i$                   |
        | $r_{u,i}$  | Rating of product with number $i$ for user with number $u$ |
        | $a_p$      | Filtering rate of products by popularity                   |
        '''
    )

st.markdown(
    '''
    To check the effect of filtering by popularity and the impact of the value of the rate $a_p$ 
    on the accuracy of predictions, will plot a graph of the dependence of the value 
    of the metric $MAP@10$ on the value of this rate.
    '''
)

with st.columns([20, 60, 20])[1]:
    with st.container(border=True):
        st.markdown('Dependence of prediction accuracy on filtering rate')
        total_map10 = load_total_map10()
        total_rate = load_total_rate()
        chart = plot_total(total_rate, total_map10)
        st.altair_chart(chart)

st.markdown(
    f'''
    The graph shows that the value of the rate $a_p$ affects the quality of filtration. 
    Thus, when the values of these rates are close to zero (i.e., with weak filtration), 
    as it should be, the value of the $MAP@10$ metric is close to the value obtained 
    by filtering by the time of purchase and the ordinal number of adding the product to the cart. 
    Then, as the rate grows, a slight increase in the quality of filtration is observed, 
    which reaches its peak at a rate value in the region of 0.3...0.4. 
    With continued growth of the rate value, the quality of filtration begins to **rapidly decrease. 
    And when the rate values are greater than 0.8, the influence of filtration becomes negative 
    (the $MAP@10$ metric falls below the value obtained by filtering 
    by the time and ordinal number of adding the product to the cart).
    
    Will try to determine the position and magnitude of the peak of this dependence more precisely. 
    To do this, we approximate the function $MAP@10(a_p)$ on the segment $[0, 1.0]$ 
    using a 3rd order polynomial function. 
    After that, we find a point on this segment at which the derivative of this function is equal to zero. 
    This will be the point of the approximate position of the peak. 
    And then at that point we find the real value of the metric $MAP@10$.
    
    #### Result
    Filtering by product popularity gave a **small increase in accuracy** of predictions 
    (the $MAP@10$ metric **increased** by only {(total_map10 - cart_map10):.6f} from 
    {cart_map10:.6f} to {total_map10:.6f}) 
    with the filtering rate $a_p$ equal to {total_rate:.6f}.
    
    ## Filling in missing products
    
    In the model, are rating only the customer's products that he or she had previously purchased. 
    But it's needed to offer the customer a certain number of products. 
    It is quite possible that he had previously purchased a smaller number of unique products. 
    In this case, it makes sense to offer him products that are in high demand among other customers 
    in addition to the products previously purchased by the customer. 
    It is logical to assume that the customer should be offered products 
    from those groups from which he had previously actively purchased products.
    
    Will check if our assumption is correct. To do this, we will determine the ranks of product groups 
    for each customer in accordance with the total rating of the products included in this group:
    '''
)

with st.columns([32, 36, 32])[1]:
    st.latex('\large r_{u,a}=\sum_{i \in I_a}r_{u,i}')
    st.markdown(
        '''
        | Symbol | Description                                                     |
        | ----------- | ---------------------------------------------------------- |
        | $r_{u,a}$   | Rating of group with number $a$ for user with number $u$   |
        | $r_{u,i}$   | Rating of product with number $i$ for user with number $u$ |
        | $I_a$       | Set of product numbers in group with number $a$            |
        '''
    )

st.markdown(
    '''
    In each group, will rank products based on their global ratings $r^g_i$. 
    Then will find a list of the latest products purchased by customers that were mistakenly 
    not included in the recommendations.
    Next, will look at the distribution of these obtained ranks among 
    the most recently purchased products by customers that were not included in the recommendations.
    '''
)

with st.columns([20, 60, 20])[1]:
    with st.container(border=True):
        st.markdown('Distribution of group rank among last purchased products that were '
                    'not included in recommendations')
        chart = plot_aisle_rank_hist()
        st.altair_chart(chart)

with st.columns([20, 60, 20])[1]:
    with st.container(border=True):
        st.markdown('Distribution of rank within the group among '
                    'last purchased products that were not included in the recommendations')
        chart = plot_in_aisle_rank_hist()
        st.altair_chart(chart)

filled_up_map10 = load_filled_up_map10()

st.markdown(
    f'''
    The histograms show that the assumption has a right to exist, since a significant portion 
    of the products that were mistakenly not included in the recommendations belong 
    to high-ranking groups and have a high rank in their groups.
    
    Will check what effect this filling has on training data.
    
    #### Result
    
    Adding popular products from popular groups to predictions gave a minor increase in the accuracy of predictions '
    (the $MAP@10$ metric **increased** by only {(filled_up_map10 - total_map10):.6f} 
    from {total_map10:.6f} to {filled_up_map10:.6f}).'
    '''
)