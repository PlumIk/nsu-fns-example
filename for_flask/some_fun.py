import re
import logging
from datetime import datetime
import os

CHECK_PATTERN = r'20[0-9][0-9]-(?:0?[1-9]|1[0-2])-(?:0?[1-9]|[12][0-9]|3[01])T(?:00|1?[1-9]|2[0-4])-[0-5][0-9]-[0-5][' \
                r'0-9] '


def qr_true(qr_code):
    qr_template = r'^t=\d+T\d+&s=\d+.\d+&fn=\d+&i=\d+&fp=\d+&n=1$'
    qr_is_valid = re.match(qr_template, qr_code)
    if qr_is_valid:
        return True
    return False


def search_for_oldest_log(list_logs):
    i = 0
    list_with_data_and_time = list()
    for i in range(len(list_logs[0])):
        name_log_file = list_logs[0][i]
        date_str = name_log_file.replace(".log", "")
        if re.match(CHECK_PATTERN, date_str):
            name_file = datetime.strptime(date_str, '%Y-%m-%dT%H-%M-%S')
            list_with_data_and_time.append(name_file)
            list_with_data_and_time.sort()

    return list_with_data_and_time[0]


def create_log_file_name(date_time):
    date = date_time.strftime('%Y-%m-%dT%H-%M-%S')
    name_file = date + ".log"
    return name_file


def configuration_of_logger(path: str, max_number_of_files: int, level_log):
    fn = create_log_file_name(datetime.now())
    a = os.path.join(path, fn)
    print(a)
    logging.basicConfig(filename=a, level=level_log, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%dT%H:%M:%S')

    """ logging.basicConfig(filename=fn, level=level_log, encoding='utf-8', filemode='w',
                        format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%dT%H:%M:%S')  python 3.9 """
