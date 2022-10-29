'''
Name: record.py
Author: Michael Deckebach
Date: 2022-10-29
Description: A class to represent a row of data in a Table
'''

from collections import OrderedDict

from utils import KEYWORD_COMPARISON_OPERATORS


class Record:

    def __init__(self, keys, values):
        self.data = OrderedDict(zip(keys, values))

    def get_values(self):
        return list(self.data.values())

    def set_value(self, key, value):
        self.data[key] = value

    def satisfies(self, condition):

        parsed = condition.split()

        if len(parsed) != 3:
            raise Exception("Invalid condition. Please check syntax")

        target_field = parsed[0]
        operator = parsed[1]
        value = parsed[2].replace("'", '')
        
        if target_field not in self.data.keys():
            raise Exception("!Failed - " + target_field + " is not a valid field name")

        return KEYWORD_COMPARISON_OPERATORS[operator](self.data[target_field], value)                                
