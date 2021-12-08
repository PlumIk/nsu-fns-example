import re
import logging
from datetime import datetime
import os


def qr_true(qr_code):
    qr_template = r'^t=\d+T\d+&s=\d+.\d+&fn=\d+&i=\d+&fp=\d+&n=1$'
    qr_is_valid = re.match(qr_template, qr_code)
    if qr_is_valid:
        return True
    return False


def search_for_oldest_log(list_logs):
    i = 0
    list_with_data_and_time = list()
    for i in range(10):
        name_log_file = list_logs[0][i]
        date_str = name_log_file.replace(".log", "")
        name_file = datetime.strptime(date_str, '%Y-%m-%dT%H-%M-%S')
        list_with_data_and_time.append(name_file)

    list_with_data_and_time.sort()
    return list_with_data_and_time[0]


def create_log_file_name(date_time):
    date = date_time.strftime('%Y-%m-%dT%H-%M-%S')
    name_file = date + ".log"
    return name_file


def configuration_of_logger(path: str, max_number_of_files: int, level_log):
    filetype = ['log']
    list_logs = [[f for f in os.listdir(path) if f.endswith(type_)] for type_ in filetype]
    number_of_files_to_log = len(list_logs[0])

    if number_of_files_to_log >= max_number_of_files:
        old_log_file = create_log_file_name(search_for_oldest_log(list_logs))
        os.remove(old_log_file)

    fn = create_log_file_name(datetime.now())

    logging.basicConfig(filename=fn, level=level_log, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%dT%H:%M:%S')

    """ logging.basicConfig(filename=fn, level=level_log, encoding='utf-8', filemode='w',
                        format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%dT%H:%M:%S')  python 3.9 """
