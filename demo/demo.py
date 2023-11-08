from pathlib import Path
from csv import QUOTE_NONE
from tqdm import tqdm
from src.csify import CSify
import requests
import tarfile
import pandas as pd
import google_translate_args


def generate_jesc_cs():
    # dev_data_path = Path('./data/split/dtsc2_train_data')
    dev_data_path = Path('./data/split/dtsc2_train_data')
    print("Checking if Test data exists...")
    get_data(dev_data_path)
    print("Converting Test data to dataframe")
    df = read_data(dev_data_path)
    result_dir_path = Path("./data/CSified")

    print("Generating EN_HI CS Output for test data")
    en_to_enhi_code_switcher = CSify(**google_translate_args.EN_TO_ENHI)
    csify_df(df, result_dir_path, "DSTC-CS",
             'EN-Sentence', en_to_enhi_code_switcher.generate)


def get_data(data_path):
    data_dir_path = data_path.parents[1]
    data_dir_path.mkdir(parents=True, exist_ok=True)
    if not data_path.exists():
        print("Downloading and Extracting data...")
        url = "https://nlp.stanford.edu/projects/jesc/data/split.tar.gz"
        response = requests.get(url, stream=True)
        file = tarfile.open(fileobj=response.raw, mode="r|gz")
        file.extractall(path=data_dir_path)
    print("OK")


def read_data(data_path):
    return pd.read_csv(data_path, quoting=QUOTE_NONE, delimiter="\t", header=None, names=["EN-Sentence", "JA-Sentence"])


def csify_df(df, dir_path, filename, base_column, func, chunksize=0):
    gen_input_func(df, dir_path, filename, base_column, func)


def gen_input_func(df, dir_path, filename, base_column, func):
    # if file_exist(dir_path, filename):
    #     return
    tqdm.pandas()
    df = df.copy()

    df[filename] = df[base_column].progress_map(func)
    df = df.loc[:, [base_column, filename]]
    make_csv(df, dir_path, filename)


def make_csv(df, dir_path, filename):
    dir_path.mkdir(parents=True, exist_ok=True)
    path_to_file = dir_path / filename
    print(f"Writing to {path_to_file}")

    df.to_csv(path_or_buf=path_to_file,
              index=False, quoting=QUOTE_NONE, sep='~')
    print("OK")


def file_exist(dir_path, filename):
    dir_path.mkdir(parents=True, exist_ok=True)
    path_to_file = dir_path / filename
    if path_to_file.exists():
        print(f"{dir_path / filename} already exist")
        return True
    return False
