'''
Name: table.py
Author: Michael Deckebach
Date: 2022-10-01
Description: Implementation of a Table class, which represents two dimensional
data (rows & columns) in a database. Records (tuples) are stored as 
comma-separated values in a CSV file. Each CSV file can be thought of as 
a single table. Field names and types are stored in the first row of the file.
Currently supports ALTER TABLE, CREATE TABLE, DROP TABLE, and SELECT * FROM <table>.
'''

import csv, os
from typing import OrderedDict

from condition import Condition
from utils import KEYWORD_COMPARISON_OPERATORS

class Table():
    def __init__(self, name):
        self.name = name

    def alter(self, new_field):
        if not os.path.exists(self.name):
            raise Exception("!Failed to alter " + self.name + " because it does not exist.")
    
        altered = []
        with open(self.name) as csvfile:
            reader = csv.reader(csvfile)

            # Alter the first row (headers)
            headers = next(reader)
            headers.append(new_field)
            altered.append(headers)

            # Default value of None for existing records for the new field
            for row in reader:
                row.append(None)
                altered.append(row)
        
        with open(self.name, 'w') as csvfile:
            writer = csv.writer(csvfile, lineterminator='\n')
            writer.writerows(altered)
            print("Table " + self.name + " modified.")

    def create(self, fields):
        if os.path.exists(self.name):
            raise Exception("!Failed to create table " + self.name + " because it already exists.")
        
        with open(self.name, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, lineterminator='\n', fieldnames=fields)
            writer.writeheader()
            print("Table " + self.name + " created.")   


    def drop(self):
        if not os.path.exists(self.name):
            raise Exception("!Failed to delete " + self.name + " because it does not exist.")
        
        os.remove(self.name)
        print("Table " + self.name + " deleted.")

    def select(self, select_clause):
        if not os.path.exists(self.name):
            raise Exception("!Failed to query " + self.name + " because it does not exist.")
        
        with open(self.name, newline='\n') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if select_clause == ['*']:
                    print('|'.join(row))
                else:
                    #todo: this is a placeholder to implement more advanced SELECT syntax
                    pass

    def insert(self, values):
        if not os.path.exists(self.name):
            raise Exception("!Failed to insert into " + self.name + " because it does not exist.")
        
        fields = self._get_field_names()
        if len(fields) != len(values):
            raise Exception("!Failed to insert into " + self.name + " because field counts do not match.")

        with open(self.name, 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(values)
            print("1 new record inserted.")   

    def update(self, target_field, new_value, condition):
        if not os.path.exists(self.name):
            raise Exception("!Failed to update " + self.name + " because it does not exist.")
        
        field_names = self._get_field_names()
        if target_field not in field_names:
            raise Exception("!Failed to update " + self.name + " because " + target_field + " not in table.")

        target_column = field_names.index(target_field)

        count_modified = 0
        updated = []

        with open(self.name) as csvfile:
            reader = csv.reader(csvfile)
            updated.append(next(reader))

            for row in reader:

                row_dict = OrderedDict(zip(field_names, row))

                c = Condition(condition)

                if c.field_name not in row_dict.keys():
                    raise Exception("!Failed to update " + self.name + " because " + c.field_name + " is not a valid field name")

                value_to_test = row_dict[c.field_name]
                value_to_test_to = c.value

                condition_met = KEYWORD_COMPARISON_OPERATORS[c.operator](value_to_test, value_to_test_to)
                                
                if condition_met:
                    row_dict[target_field] = new_value
                    updated.append(list(row_dict.values()))
                    count_modified += 1
                else:
                    updated.append(row)

        with open(self.name, 'w') as csvfile:
            writer = csv.writer(csvfile, lineterminator='\n')
            writer.writerows(updated)
        
        if count_modified == 1:
            print(str(count_modified) + " record modified.")
        else:
            print(str(count_modified) + " records modified.")


    def _get_field_names(self):
        if not os.path.exists(self.name):
            raise Exception("!Error - attempted to retrieve field names for a table that does not exist: " + self.name)
        
        field_names = []

        with open(self.name) as csvfile:
            reader = csv.reader(csvfile)
            field_names = next(reader)

        field_names = [field.split()[0] for field in field_names]
        
        return field_names



        # Table(self.table_name).update(self.target_field, self.target_value, self.conditions)
