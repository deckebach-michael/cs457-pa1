'''
Name: table.py
Author: Michael Deckebach
Date: 2022-10-30
Description: Implementation of a Table class, which represents two dimensional
data (rows & columns) in a database. Records (tuples) are stored as 
comma-separated values in a CSV file. Each CSV file can be thought of as 
a single table. Field names and types are stored in the first row of the file.
Currently supports ALTER, CREATE, DELETE, DROP, SELECT, and UPDATE commands.
'''

import csv, os

from record import Record

class Table():
    def __init__(self, name, alias=None):
        self.name = name
        self.alias = alias

    def alter(self, new_field):
        self._check_table_exists("alter")
    
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

    def delete(self, condition):
        
        field_names = self._get_field_names()
        field_types = self._get_field_types()
        count_deleted = 0
        updated = []

        self._check_table_exists("delete records from table")

        with open(self.name) as csvfile:
            reader = csv.reader(csvfile)
            updated.append(next(reader))

            for row in reader:

                record = Record(field_names, field_types, row)

                if record.satisfies(condition):
                    count_deleted += 1
                else:
                    updated.append(record.get_values())

        with open(self.name, 'w') as csvfile:
            writer = csv.writer(csvfile, lineterminator='\n')
            writer.writerows(updated)
        
        if count_deleted == 1:
            print(str(count_deleted) + " record deleted.")
        else:
            print(str(count_deleted) + " records deleted.")

    def drop(self):
        self._check_table_exists("delete")        
        os.remove(self.name)
        print("Table " + self.name + " deleted.")

    def select(self, select_clause, where_clause=None, join_type=None, right_table=None, right_table_alias=None):
        
        if join_type:
            self.join_select(select_clause, where_clause, join_type, right_table, right_table_alias)
        else:
            self.single_select(select_clause, where_clause)

    def join_select(self, select_clause, where_clause, join_type, right_table, right_table_alias):
        right = Table(right_table, right_table_alias)

        self._check_table_exists("query")
        right._check_table_exists("query")

        field_names = self._get_field_names() + right._get_field_names()
        field_types = self._get_field_types() + right._get_field_types()

        if self.alias:
            where_clause = where_clause.replace(self.alias + '.', '')
        if right.alias:
            where_clause = where_clause.replace(right_table_alias + '.', '')

        with (open(self.name, newline='\n') as l_csvfile,
              open(right.name, newline='\n') as r_csvfile
        ):
            l_reader = csv.reader(l_csvfile)
            r_reader = csv.reader(r_csvfile)

            header = next(l_reader) + next(r_reader)
            print('|'.join(header))

            for l_row in l_reader:
                is_printed = False

                for r_row in r_reader:
                    
                    combined_row = l_row + r_row
                    record = Record(field_names, field_types, combined_row)

                    if record.satisfies(where_clause):
                        results = record.get_values(select_clause)
                        print('|'.join(results))
                        is_printed = True
   
                if join_type == 'LEFT' and is_printed == False:
                    null_values = len(header) - len(l_row)                    
                    left_join_row = l_row + ['' for i in range(null_values)]
                    print(('|').join(left_join_row))

                r_csvfile.seek(0)
                next(r_reader)


    def single_select(self, select_clause, where_clause=None):
        self._check_table_exists("query")

        field_names = self._get_field_names()
        field_types = self._get_field_types()

        with open(self.name, newline='\n') as csvfile:
            reader = csv.reader(csvfile)

            # Special code to handle headers separately, because they do not adhere
            # to the same data type criteria as actual data rows do (e.g., a field
            # of int data type still as a string header)
            header = next(reader)
            results = [field for field in header if field.split()[0] in select_clause]
            if select_clause == ['*']:
                print('|'.join(header))
            else:
                print('|'.join(results))


            for row in reader:
                record = Record(field_names, field_types, row)

                if not record.satisfies(where_clause):
                    continue
                else:
                    results = record.get_values(select_clause)
                    print('|'.join(results))

    def insert(self, values):
        self._check_table_exists("insert into")
        
        fields = self._get_field_names()
        if len(fields) != len(values):
            raise Exception("!Failed to insert into " + self.name + " because field counts do not match.")

        with open(self.name, 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(values)
            print("1 new record inserted.")   

    def update(self, target_field, new_value, condition):
        self._check_table_exists("update")

        field_names = self._get_field_names()
        field_types = self._get_field_types()
        count_modified = 0
        updated = []
        
        if target_field not in field_names:
            raise Exception("!Failed to update " + self.name + " because " + target_field + " not in table.")

        with open(self.name) as csvfile:
            reader = csv.reader(csvfile)
            updated.append(next(reader))

            for row in reader:

                record = Record(field_names, field_types, row)

                if record.satisfies(condition):
                    record.set_value(target_field, new_value)
                    updated.append(record.get_values())
                    count_modified += 1
                else:
                    updated.append(record.get_values())

        with open(self.name, 'w') as csvfile:
            writer = csv.writer(csvfile, lineterminator='\n')
            writer.writerows(updated)
        
        if count_modified == 1:
            print(str(count_modified) + " record modified.")
        else:
            print(str(count_modified) + " records modified.")

    def _check_table_exists(self, action):
       if not os.path.exists(self.name):
            raise Exception("!Failed to " + action + " " + self.name + " because it does not exist.")
  
    def _get_field_names(self):
        self._check_table_exists("retrieve field names for table")
        
        field_names = []
        with open(self.name) as csvfile:
            reader = csv.reader(csvfile)
            field_names = next(reader)

        field_names = [field.split()[0] for field in field_names]
        
        return field_names

    def _get_field_types(self):
        self._check_table_exists("retrieve field types for table")
        
        header = []
        with open(self.name) as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)

        field_types = [field.split()[1] for field in header]
        
        return field_types


