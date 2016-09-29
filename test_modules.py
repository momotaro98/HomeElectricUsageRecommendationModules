# coding: utf-8

import unittest
import csv
from datetime import datetime as dt

from home_electric_usage_recommendation_modules.modules import SettingTemp


class RowData:
    '''
    想定しているデータカラム
    --------------------------------------------------------------------------------------------
    timestamp,on_off,operating,set_temperature,wind,temperature,pressure,humidity,IP_Address
    ============================================================================================
    2016-08-22 07:53:16,on,cool,25,auto,28.6441845969,998.101116478,64.0657707517,192.168.11.15
    --------------------------------------------------------------------------------------------
    2016-08-22 08:44:08,off,cool,25,auto,27.9784137312,997.686977325,55.3711607947,192.168.11.15
    --------------------------------------------------------------------------------------------
    ...
    '''
    def __init__(self, timestamp, on_off=None, operating=None,
                 set_temperature=None, wind=None,
                 temperature=None, pressure=None, humidity=None,
                 IP_Address=None):
        self.timestamp = dt.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        self.on_off = str(on_off) if on_off else on_off
        self.operating = str(operating) if operating else operating
        self.set_temperature = int(set_temperature)\
            if set_temperature else set_temperature
        self.wind = str(wind) if wind else wind
        self.temperature = float(temperature) if temperature else wind
        self.pressure = float(pressure) if pressure else pressure
        self.humidity = float(humidity) if humidity else humidity
        self.IP_Address = str(IP_Address) if IP_Address else IP_Address


class SettingTempModuleTestCase(unittest.TestCase):
    def setUp(self):
        # prepare TestCase
        with open('test.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            self.input_rows = []
            for row in reader:
                self.input_rows.append(\
                    RowData(timestamp=row['timestamp'],
                            set_temperature=row['set_temperature']))

    def test_find_frequest_set_temperature(self):
        '''
        _find_frequent_set_temperature()メソッドをテスト
        '''
        st = SettingTemp(self.input_rows)
        frequent_set_temp = st._find_frequent_set_temperature()
        self.assertEqual(frequent_set_temp, 25)

    def test_show_recommend_set_temperature(self):
        '''
        _show_recommend_set_temperature()メソッドをテスト
        '''
        st = SettingTemp(self.input_rows)
        recommend_set_temp = st._show_recommend_set_temperature()
        self.assertEqual(recommend_set_temp, 27)


class ReduceUsageModuleTestCase(unittest.TestCase):
    def setUp(self):
        # prepare TestCase
        with open('test.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            self.input_rows = []
            for row in reader:
                self.input_rows.append(\
                    RowData(timestamp=row['timestamp'],
                            on_off=row['on_off']))


class ChangeUsageModuleTestCase(unittest.TestCase):
    def setUp(self):
        # prepare TestCase
        with open('test.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            self.input_rows = []
            for row in reader:
                self.input_rows.append(\
                    RowData(timestamp=row['timestamp'],
                            on_off=row['on_off']))


if __name__ == "__main__":
    '''
    with open('test.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        input_rows = []
        for row in reader:
            input_rows.append(\
                RowData(timestamp=row['timestamp'],
                        set_temperature=row['set_temperature']))

    for row in input_rows:
        print("row.set_temperature: ", row.set_temperature)
    '''
    pass
