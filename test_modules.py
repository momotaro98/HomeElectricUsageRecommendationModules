# coding: utf-8

import unittest
import csv

from home_electric_usage_recommendation_modules.modules import SettingTemp


class RowData:
    '''
    入力データの型
    ------------------------------------
    timestamp | set_temperature | on_off
    ====================================
    2016-08-01 11:20:35 | 25 | on
    ------------------------------------
    2016-08-01 17:43:26 | 25 | off
    ------------------------------------
    ...
    '''
    def __init__(self, timestamp, set_temperature=25, on_off='on'):
        self.timestamp = timestamp
        self.set_temperature = set_temperature
        self.on_off = on_off


def make_input_list():
    ret_list = []
    with open('test.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ret_list.append(RowData(row['timestamp'],
                                      set_temperature=row['set_temperature'],
                                      on_off=row['on_off'],
                                      ))
    return ret_list


class SettingTempModuleTestCase(unittest.TestCase):
    def setUp(self):
        # prepare TestCase
        input_list = make_input_list()


class ReduceUsageModuleTestCase(unittest.TestCase):
    def setUp(self):
        # prepare TestCase
        pass


class ChangeUsageModuleTestCase(unittest.TestCase):
    def setUp(self):
        # prepare TestCase
        pass


if __name__ == "__main__":
    input_list = make_input_list()
    for row in input_list:
        print(row.timestamp, row.on_off, row.set_temperature)
