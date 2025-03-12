"""
Parallel data processing module.
"""

import argparse
from multiprocessing import Pool
from pathlib import Path
import numpy as np
import pandas as pd
import functions as f
import pickle


def load_data(file_path):
    """
    Loads a data object from a binary file.
    :param file_path: path to the file.
    :return: the loaded data object.
    """
    with open(file_path, 'rb') as fp:
        # noinspection PyTypeChecker
        data = pickle.load(fp)
    return data


def get_map10_by_days_rates(precisions: pd.Series, data_path: Path) -> pd.Series:
    """
    Calculates the accuracy of predictions for the MAP@10 metric obtained by filtering only by depth
    based on the number of days until the last transaction for different values of the coefficient filtering.
    :param precisions: Pandas Series whose index is a list of filter coefficient values,
    and np.nan values
    :param data_path: path to the data folder.
    :return: Pandas Series with ``MAP@10`` metric values
    """

    prior_transactions = load_data(data_path / 'prior_transactions.pkl')
    last_products = load_data(data_path / 'last_products.pkl')

    for days_rate in precisions.index:
        map10 = f.get_prediction_precision(
            true=last_products,
            prediction=f.get_prediction(
                f.get_ratings(
                    f.get_weights(prior_transactions, days_rate=days_rate))),
            k=10
        )
        precisions.at[days_rate] = map10

    return precisions


def get_map10_by_cart_rates(precisions: pd.DataFrame, data_path: Path, days_rate: float):
    """
    Calculates the accuracy of predictions for the MAP@10 metric obtained by filtering by depth
    based on the number of days until the last transaction and filtering by the product added to the cart number
    for different values of the filter coefficient.
    :param precisions: Pandas Series whose index is a list of filter coefficient values,
    and the values are np.nan
    :param data_path: path to the data folder.
    :param days_rate: filter coefficient by time.
    :return: Pandas Series with ``MAP@10`` metric values.
    """

    prior_transactions = load_data(data_path / 'prior_transactions.pkl')
    last_products = load_data(data_path / 'last_products.pkl')

    for cart_rate in precisions.index:
        map10 = f.get_prediction_precision(
            true=last_products,
            prediction=f.get_prediction(
                f.get_ratings(
                    f.get_weights(
                        prior_transactions, days_rate=days_rate, cart_rate=cart_rate))),
            k=10
        )
        precisions.at[cart_rate] = map10

    return precisions


def get_map10_by_total_rates(precisions: pd.DataFrame, data_path: Path,
                             days_rate: float, cart_rate: float):
    """
    Calculates the prediction accuracy of a metric MAP@10 obtained by filtering by depth
    based on information about the number of days before the last transaction and filtering by the product addition number to the cart
    with different values of the filtering coefficient by global rating.
    :param precisions: Pandas Series, the index of which is a list of values of the filtering coefficient,
    and the values of np.nan
    :param data_path: path to the folder with data.
    :param days_rate: filtering coefficient by time.
    :param cart_rate: filtering coefficient by the product addition number to the cart.
    :return: Pandas Series with metric values ``MAP@10``
    """

    prior_transactions = load_data(data_path / 'prior_transactions.pkl')
    last_products = load_data(data_path / 'last_products.pkl')

    weights = f.get_weights(prior_transactions, days_rate=days_rate, cart_rate=cart_rate)
    ratings = f.get_ratings(weights).rename(columns={'rating': 'user_rating'})
    total_ratings = f.get_total_ratings(weights).rename(columns={'rating': 'total_rating'})
    ratings = ratings.merge(total_ratings, on='product_id', how='left')

    for rate in precisions.index:
        ratings['rating'] = ratings['user_rating'] * np.exp(ratings['total_rating'] * rate)
        map10 = f.get_prediction_precision(
            true=last_products,
            prediction=f.get_prediction(ratings),
            k=10
        )
        precisions.at[rate] = map10

    return precisions


if __name__ == '__main__':

    __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"

    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", help="Number of parallel workers.")
    parser.add_argument("--data_path", help="Path to the data folder.")
    parser.add_argument("--start", help="Start value of var range.")
    parser.add_argument("--stop", help="Stop value of var range.")
    parser.add_argument("--num", help="Spacing between values in var range.")
    parser.add_argument("--func", help="Name of the calling function.")
    parser.add_argument("--days_rate", help="Rate of 'days_before_last_order' filtration.")
    parser.add_argument("--cart_rate", help="Rate of 'add_to_cart_order' filtration.")

    args = parser.parse_args()

    WORKERS = int(args.workers)
    DATA_PATH = Path(args.data_path)
    var_range = np.linspace(float(args.start), float(args.stop), int(args.num))
    func = locals()[args.func]

    precisions = pd.DataFrame(
        columns=['var', 'precision', 'worker'],
        dtype=int
    )

    precisions['var'] = var_range
    precisions['worker'] = precisions.index % WORKERS
    precisions.set_index('var', inplace=True)

    with Pool(WORKERS) as pool:
        if func == get_map10_by_days_rates:
            precisions.index.name = 'days_rate'
            process_results = [pool.apply_async(func, (data, DATA_PATH))
                               for _, data in precisions.groupby('worker')['precision']]
        elif func == get_map10_by_cart_rates:
            days_rate = float(args.days_rate)
            precisions.index.name = 'cart_rate'
            process_results = [pool.apply_async(func, (data, DATA_PATH, days_rate))
                               for _, data in precisions.groupby('worker')['precision']]
        elif func == get_map10_by_total_rates:
            days_rate = float(args.days_rate)
            cart_rate = float(args.cart_rate)
            precisions.index.name = 'total_rate'
            process_results = [pool.apply_async(func, (data, DATA_PATH, days_rate, cart_rate))
                               for _, data in precisions.groupby('worker')['precision']]

        result = pd.concat([process_result.get() for process_result in process_results]).sort_index()

    with open(DATA_PATH / 'precisions.pkl', 'wb') as fp:
        # noinspection PyTypeChecker
        pickle.dump(result, fp)
