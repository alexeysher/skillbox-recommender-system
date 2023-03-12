import argparse
import streamlit.web.bootstrap as bootstrap

parser = argparse.ArgumentParser()
parser.add_argument("--data_path", help="Path to the data folder.")
parser.add_argument("--workers", help="Number of parallel workers.")
args = parser.parse_args()
real_script = 'main.py'

bootstrap.run(real_script, f'run.py {real_script}', args, {})
