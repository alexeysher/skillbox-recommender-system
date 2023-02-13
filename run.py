import argparse

import streamlit.web.bootstrap as bootstrap

parser = argparse.ArgumentParser()
parser.add_argument("--data_path", help="Path to the data folder.")
parser.add_argument("--workers", help="Number of parallel workers.")
args = parser.parse_args()
data_path = args.data_path
workers = args.workers
real_script = 'main.py'

bootstrap.run(real_script, f'run.py {real_script}', [data_path, workers], {})
