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
                    print(' | '.join(row))
                else:
                    #todo: this is a placeholder to implement more advanced SELECT syntax
                    pass

