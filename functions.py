from typing import Union
import numpy as np
from numpy.polynomial.polynomial import polyfit, polyval, polyder, polyroots
import pandas as pd
from average_precision import apk, mapk


def approximate_precision_by_rate(rates: np.array, precisions: np.array, deg=3):
    """
    Approximates the dependence of the accuracy of predictions on the value of the filter coefficient
    and finds the position of the maximum of this function on the segment between the extreme points.
    
    :param rates: 1D array of values of the filter coefficient.
    :param precisions: values of the accuracy metric of predictions.
    :param deg: the highest degree of the polynomial.
    :return: values of the approximation function and the position of its maximum.
    """

    coefs = polyfit(rates, precisions, deg)
    approx_precisions = polyval(rates, coefs)
    derivative_coefs = polyder(coefs)
    derivative_roots = polyroots(derivative_coefs)
    best_rate_candidates = derivative_roots[
        (derivative_roots.real >= rates.min()) &
        (derivative_roots.real <= rates.max()) &
        (derivative_roots.imag == 0.0)
        ].real

    best_rate_candidate_values = polyval(best_rate_candidates, coefs)
    best_rate = best_rate_candidates[best_rate_candidate_values.argmax()]

    return approx_precisions, best_rate


def preprocess_transactions(transactions: pd.DataFrame) -> [pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Adds to transaction log orders flag ``days_before_last_order`` - the number of days
    before the last transaction by this user.
    Additionally, it divides the transaction log into two parts: the last user transactions and previous
    user transactions.
    
    :param transactions: the transaction log of product purchases.
    :return: the transaction log of product purchases (except for the last transactions) and the last
    user transactions.
    """

    transactions.sort_values(['user_id', 'order_number', 'add_to_cart_order'], inplace=True)

    # From the transactions we get a list of orders with the flag
    # of days since the previous order (days_since_prior_order)
    orders = transactions[['user_id', 'order_number', 'days_since_prior_order']] \
        .groupby(['user_id', 'order_number']).head(1).fillna(0).astype(int)

    # For each order we get information about the number of days until the next order (days_before_next_order),
    # shifting the flag values ​​of the number of days since the previous order (days_since_prior_order) up
    orders['days_before_next_order'] = orders.groupby('user_id')['days_since_prior_order'] \
        .shift(-1).fillna(0).astype(int)

    # By cumulative summation we get the time until the penultimate order
    orders['days_before_last_order'] = orders \
        .sort_values(['user_id', 'order_number'], ascending=[True, False]) \
        .groupby('user_id')['days_before_next_order'] \
        .cumsum()

    transactions = transactions.merge(
        orders[['user_id', 'order_number', 'days_before_last_order']],
        on=['user_id', 'order_number'], how='right').fillna(0).astype(int)

    transactions.sort_values(['user_id', 'order_number', 'add_to_cart_order'], inplace=True)

    transactions.drop(columns='order_number').drop_duplicates(['user_id', 'days_before_last_order', 'product_id'])

    transactions['add_to_cart_order'] = transactions.groupby(['user_id', 'days_before_last_order']).cumcount() + 1

    # Select previous transactions and add information about the time until the penultimate order
    prior_transactions = transactions.loc[transactions['days_before_last_order'] > 0].copy()

    # Select last transactions
    last_transactions = transactions.loc[transactions['days_before_last_order'] == 0].copy()

    # Add information about the number of days from the penultimate to previous transactions until the last transaction
    prior_transactions = prior_transactions.merge(
        last_transactions.groupby('user_id')[['user_id', 'days_before_last_order']]
        .head(1).rename(columns={'days_before_last_order': 'days_before_last_order_shift'}),
        on='user_id', how='left')
    prior_transactions['days_before_last_order'] -= prior_transactions['days_before_last_order_shift']

    # Compile a list of product lists in recent transactions
    last_products = last_transactions[['user_id', 'product_id']] \
        .groupby('user_id')['product_id'].apply(lambda x: list(x.values)).to_list()

    return prior_transactions, last_transactions, last_products


def get_weights(transactions: pd.DataFrame,
                days_rate: float = 0.0, cart_rate: float = 0.0):
    weights = transactions[['user_id', 'product_id']].copy()
    weights['weight'] = 1

    if days_rate > 0.:
        weights['weight'] *= np.exp(-transactions['days_before_last_order'] * days_rate)

    if cart_rate > 0.:
        weights['weight'] *= np.exp(-transactions['add_to_cart_order'] * cart_rate)

    return weights


def get_ratings(weights: pd.DataFrame, total_rate: float = 0.):
    """
    Generates a table of product ratings among all customers based on their purchase transactions.
    Ratings are calculated based on frequency, transaction time, and product add-to-cart numbers.
    
    :param weights: product weights in transactions.
    :param total_rate: popularity filtering rate.
    :return: product ratings table, which contains the following columns:
    
    * ``user_id`` - unique user identifier (if ``total`` is True).
    * ``product_id`` - unique product identifier.
    * ``rating`` - product rating.
    """

    ratings = weights.groupby(['user_id', 'product_id'])['weight'].sum().rename('rating').reset_index()
    if total_rate > 0.:
        total_ratings = get_total_ratings(weights).rename(columns={'rating': 'total_rating'})
        ratings = ratings.merge(total_ratings, on='product_id', how='left')
        ratings['rating'] *= np.exp(ratings['total_rating'] * total_rate)
        ratings.drop(columns='total_rating', inplace=True)

    return ratings


def get_total_ratings(weights: pd.DataFrame):
    """
    Generates a table of product ratings among all customers based on their purchase transactions.
    Ratings are calculated based on frequency, transaction time, and product add-to-cart numbers.
    
    :param weights: product weights in transactions.
    :return: product ratings table, which contains the following columns:
    
    * ``product_id`` - unique product identifier.
    * ``rating`` - product rating.
    """

    ratings = weights.groupby('product_id')['weight'].sum().rename('rating').reset_index()
    ratings['rating'] /= weights['user_id'].nunique()

    return ratings


def get_prediction(ratings: pd.DataFrame,
                   k: int = 10):
    """
    Generates a prediction of products in the next purchase with the given number of elements.
    :param ratings: product ratings among users with columns ``user_id``, ``product_id``, ``rating``.
    :param k: maximum number of elements in the prediction.
    :return: dataframe with columns ``user_id``, ``product_id``.
    """

    prediction = ratings.sort_values(['user_id', 'rating'], ascending=[True, False])
    prediction = prediction.groupby('user_id').head(k)

    return prediction


def get_aisle_ranks(ratings: pd.DataFrame, products: pd.DataFrame):
    extended_ratings = ratings.merge(products[['aisle_id', 'product_id']], on='product_id', how='left')
    aisle_ratings = extended_ratings.groupby(['user_id', 'aisle_id'])['rating'].sum()
    aisle_ranks = aisle_ratings \
        .groupby('user_id').rank(ascending=False).rename('aisle_rank').astype(int) \
        .reset_index().sort_values(['user_id', 'aisle_rank'])
    return aisle_ranks


def get_inside_aisle_ranks(ratings: pd.DataFrame, products: pd.DataFrame):
    extended_ratings = ratings.merge(products[['aisle_id', 'product_id']], on='product_id', how='left')
    inside_aisle_ratings = extended_ratings.groupby(['aisle_id', 'product_id'])['rating'].sum()
    inside_aisle_ranks = inside_aisle_ratings \
        .groupby('aisle_id').rank(ascending=False).rename('inside_aisle_rank').astype(int) \
        .reset_index().sort_values(['aisle_id', 'inside_aisle_rank'])
    return inside_aisle_ranks


def fill_up_prediction(prediction: pd.DataFrame, aisle_ranks: pd.DataFrame, inside_aisle_ranks: pd.DataFrame,
                       k: int = 10):
    sizes = prediction.groupby('user_id').size()
    small_sizes = sizes.loc[sizes < k].copy()
    appendix = []
    for user, small_size in small_sizes.items():
        appendix_size = k - small_size
        predicted_products = prediction.loc[prediction['user_id'] == user, 'product_id'].to_list()
        popular_aisles = aisle_ranks.loc[aisle_ranks['user_id'] == user, 'aisle_id'].head(k).to_list()
        appendix_size_per_aisle = [appendix_size // len(popular_aisles)] * len(popular_aisles)
        for index in range(appendix_size - sum(appendix_size_per_aisle)):
            appendix_size_per_aisle[index] += 1
        for aisle, size in zip(popular_aisles, appendix_size_per_aisle):
            if size == 0:
                break
            popular_aisle_products = inside_aisle_ranks.loc[inside_aisle_ranks['aisle_id'] == aisle, 'product_id'] \
                .head(k).to_list()
            for product in popular_aisle_products:
                if product not in predicted_products:
                    appendix.append((user, product))
                    size -= 1
                    if size == 0:
                        break
    filled_prediction = pd.concat([prediction, pd.DataFrame(appendix, columns=['user_id', 'product_id'])]).fillna(0)
    return filled_prediction


def get_prediction_precision(
        true: Union[list[int], list[list[int]]],
        prediction: pd.DataFrame,
        k: int = 10
):
    """
    Calculates the prediction accuracy of popular products. If the predictions are for all products without grouping,
    then the accuracy is determined by the ``AP@K`` metric. Otherwise, the average prediction accuracy
    among all product groups is calculated using the ``MAP@K` metric.
    :param true: the actual list of products in the user's purchase, or the list of product lists
    in the user's purchases.
    :param prediction: the list of predicted products in the user's purchase, or the list of predicted products
    in the user's purchases.
    :param k: the number of elements on which the accuracy is calculated.
    :return: the value of the accuracy metric.
    """
    if isinstance(true[0], int):
        prediction = prediction['product_id'].to_list()
        precision = apk(true, prediction, k)
    else:
        prediction = [
            user_ratings.to_list()
            for _, user_ratings
            in prediction.groupby('user_id')['product_id']
        ]
        precision = mapk(true, prediction, k)
    return precision


def get_prediction_table(
        prediction: pd.DataFrame,
):
    """
    Converts a prediction dataframe with columns: ``user_id``, ``product_id`` into a tabular
    dataframe with index from column 'user_id' and columns: 1,2,...,[number of elements in prediction] with values from
    column `product_id`.
    :param prediction: prediction dataframe.
    :return: prediction dataframe in tabular form.
    """
    prediction['rank'] = prediction.groupby('user_id')['product_id'].cumcount() + 1
    prediction_table = prediction \
        .pivot(index='user_id', columns='rank', values='product_id') \
        .fillna(0) \
        .astype(int)
    prediction.drop(columns='rank')
    return prediction_table


def save_kaggle_submission_csv(
        prediction: pd.DataFrame,
        file_path: str
):
    """
    Saves the prediction as a solution csv file for the `skillbox-recommender-system` competition on the Kaggle platform.
    
    :param prediction: prediction of products in the users' next purchase.
    :param file_path: path to the solution file.
    """
    prediction_table = get_prediction_table(prediction)
    prediction_csv = prediction_table \
        .map(str) \
        .apply(list, axis=1) \
        .str.join(' ') \
        .rename('product_id') \
        .to_frame()
    prediction_csv.to_csv(file_path)


def get_map10_by_days_rate(last_products: list[list[int]], prior_transactions: pd.DataFrame, days_rate: float):
    return get_prediction_precision(true=last_products,
                                    prediction=get_prediction(
                                        get_ratings(get_weights(prior_transactions, days_rate=days_rate))),
                                    k=10)


def get_map10_by_cart_rate(last_products: list[list[int]], prior_transactions: pd.DataFrame,
                           days_rate: float, cart_rate: float):
    return get_prediction_precision(true=last_products,
                                    prediction=get_prediction(
                                        get_ratings(get_weights(prior_transactions,
                                                                days_rate=days_rate, cart_rate=cart_rate))),
                                    k=10)


def get_map10_by_total_rate(last_products: list[list[int]], prior_transactions: pd.DataFrame,
                            days_rate: float, cart_rate: float, total_rate: float):
    return get_prediction_precision(true=last_products,
                                    prediction=get_prediction(
                                        get_ratings(get_weights(prior_transactions,
                                                                days_rate=days_rate,
                                                                cart_rate=cart_rate,
                                                                ), total_rate=total_rate)),
                                    k=10)
