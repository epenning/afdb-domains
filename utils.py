import os
import requests
from datetime import datetime


def add_to_error_file(error, to_add):
    filename = datetime.now().strftime("{}-%Y_%m_%d-%I_%M_%S_%p.txt").format(error)
    with open(filename, 'a') as error_file:
        error_file.write(to_add + "\n")


def make_dir(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)


def download_to(url, target_path):
    response = requests.get(url)
    if response.ok:
        with open(target_path, "wb") as target_file:
            target_file.write(response.content)
    else:
        raise Exception(response.content)


def do_per_line(filename, function):
    with open(filename, 'r') as lines:
        for line in lines:
            function(line.strip())
