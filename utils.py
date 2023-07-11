import os
import shutil
import random
import csv
import pandas as pd
from ctgan import CTGAN

from datetime import datetime, timedelta


def join_path(base_path, relative_path):
    return os.path.join(base_path, relative_path)

def format_folder(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)

def make_dirs_or_format_dir(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    else:
        format_folder(folder_path)

def my_load_data(csv_data_dir):
    return pd.read_csv(csv_data_dir)

def learning_data(data, discrete_columns, epochs=300):
    ctgan = CTGAN(verbose=True, cuda=True, epochs=epochs)
    ctgan.fit(data, discrete_columns)
    return ctgan

def read_bd_csv(bd_csv_dir):
    return csv.reader(open(bd_csv_dir, encoding='utf-8-sig'))

def rand_date():
    start_date = datetime.now() - timedelta(days=1825)
    end_date = datetime.now()

    random_date = start_date + (end_date - start_date) * random.random()
    return random_date.strftime("%d.%m.%Y")

def rand_sub_arr(input_arr, nums_elements_sub_arr):
    sub_arr = random.sample(input_arr, nums_elements_sub_arr)
    sub_arr.sort()
    return sub_arr

def rand_number(first_number):
    if first_number:
        return random.randint(1, 9)
    else:
        return random.randint(0, 9)

def rand_string_number(input_str):
    split_input_str = [element for element in input_str]
    output_str = ''
    if input_str != '':
        first_number = True
        for char in split_input_str:
            if char.isdigit():
                new_char = str(rand_number(first_number))
                first_number = False
            else:
                new_char = char
            output_str += new_char
    return output_str
