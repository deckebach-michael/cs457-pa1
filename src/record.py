'''
Name: record.py
Author: Michael Deckebach
Date: 2022-10-29
Description: A class to represent a row of data in a Table
'''

from collections import OrderedDict

from utils import KEYWORD_COMPARISON_OPERATORS, KEYWORD_DATA_TYPES


class Record:

    def __init__(self, fields, types, values):
        
        typed_values = []
        for type, value in zip(types, values):
            if type in KEYWORD_DATA_TYPES:
                typed_values.append(KEYWORD_DATA_TYPES[type](value))
            else:
                typed_values.append(value)

        self.data = OrderedDict(zip(fields, typed_values))

    def get_values(self, fields=None):
        if fields == None or fields == ['*']:
            return [str(value) for value in self.data.values()]
        else:
            return [str(self.data[field]) for field in fields]

    def set_value(self, key, value):
        self.data[key] = value

    def satisfies(self, condition):

        if condition == None:
            return True

        else:
            parsed = condition.split()

            if len(parsed) != 3:
                raise Exception("Invalid condition. Please check syntax")

            target_field = parsed[0]
            operator = parsed[1]
            value = parsed[2].replace("'", '')
            
            if target_field not in self.data.keys():
                raise Exception("!Failed - " + target_field + " is not a valid field name")

            target_value = self.data[target_field]
            typed_value = type(target_value)(value)

            return KEYWORD_COMPARISON_OPERATORS[operator](target_value, typed_value)                                
