# coding: utf-8

import unittest
from home_electric_usage_recommendation_modules import (SettingTemp,
                                                        ReduceUsage,
                                                        ChangeUsage)


class RowTestDataSet:
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
    def __init__(self):
        pass


class SettingTempModuleTestCase(unittest.TestCase):
    def setUp(self):
        # prepare TestCase
        pass


class ReduceUsageModuleTestCase(unittest.TestCase):
    def setUp(self):
        # prepare TestCase
        pass


class ChangeUsageModuleTestCase(unittest.TestCase):
    def setUp(self):
        # prepare TestCase
        pass
