import re

from database import Database
from table import Table
import globals


class StatementFactory:

    def __init__(self):
        pass

    def make_statement(self, str):

        if self.is_create_statement(str):
            return CreateStatement(str)

        elif self.is_drop_statement(str):
            return DropStatement(str)

        elif self.is_use_statement(str):
            return UseStatement(str)

        elif self.is_select_statement(str):
            return SelectStatement(str)
            
            # TODO
            # case alter_regex_match:
            #     return Alter_statement(str)

        else:
            raise Exception("Command not supported: " + str)

    def is_create_statement(self, str):
        return bool(re.search(r'(?i)(CREATE )(.*)', str))

    def is_drop_statement(self, str):
        return bool(re.search(r'(?i)(DROP )\w{2}', str))

    def is_use_statement(self, str):
        return bool(re.search(r'(?i)(USE )\w{2}', str))

    def is_select_statement(self, str):
        return bool(re.search(r'(?i)(SELECT )(.*)', str))

class Statement:

    def __init__(self, str):
        self.str = str
        self.parsed = str.split()
        self.num_words = len(self.parsed)

    def execute(self):
        pass


class CreateStatement(Statement):

    def __init__(self, str):
        Statement.__init__(self, str)

        if not self.min_size():
            raise Exception("Invalid CREATE command. Please check syntax")

        self.type = self.parsed[1].upper()
        self.object_name = self.parsed[2]

        if not self.correct_size():
            raise Exception("Invalid CREATE command. Please check syntax")

        if not self.valid_type():
            raise Exception("Invalid CREATE command. Valid objects are CREATE DATABASE <name> or CREATE TABLE <name>")

    def min_size(self):
        return self.num_words >= 3

    def correct_size(self):
        if self.type == 'DATABASE':
            return self.num_words == 3
        elif self.type == 'TABLE':
            return self.num_words >= 3

    def valid_type(self):
        return self.type in globals.KEYWORDS_OBJECTS
 
    def execute(self):
        if self.type == 'DATABASE':
            Database(self.object_name).create()
        elif self.type == 'TABLE':

            # Generate a list of fields and types
            field_str = ' '.join(self.parsed[3:])
            fields = self.parse_fields(field_str)
            
            Table(self.object_name).create(fields)

    def parse_fields(self, str):
        fields = re.findall(r'(?![(].*)[^,]*(?=.*[)]$)', str)
        return [i for i in fields if i != '']



class DropStatement(Statement):

    def __init__(self, str):
        Statement.__init__(self, str)

        if not self.correct_size():
            raise Exception("Invalid DROP command. Please check syntax")

        self.type = self.parsed[1].upper()
        self.object_name = self.parsed[2]

        if not self.valid_type():
            raise Exception("Invalid DROP comman. Valid objects are DROP DATABASE <name> or DROP TABLE <name>")

    def correct_size(self):
        return self.num_words == 3

    def valid_type(self):
        return self.type in globals.KEYWORDS_OBJECTS

    def execute(self):
        if self.type == 'DATABASE':
            Database(self.object_name).drop()
            pass
        elif self.type == 'TABLE':
            Table(self.object_name).drop()
            pass

class UseStatement(Statement):

    def __init__(self, str):
        Statement.__init__(self, str)

        if not self.correct_size():
            raise Exception("Invalid USE command. Please check syntax")

        self.object_name = self.parsed[1]

    def correct_size(self):
        return self.num_words == 2

    def execute(self):
        Database(self.object_name).use()
        pass

class SelectStatement(Statement):

    def __init__(self, str):
        Statement.__init__(self, str)

        #######################################################################
        #todo: NEED TO ADD ERROR CHECKING
        #######################################################################        
        self.parse_clauses()

    def execute(self):
        Table(self.from_clause).select(self.select_clause)

    def parse_clauses(self):

        #######################################################################
        #todo: NEED TO MAKE below re.search CASE INSENSITIVE USING FLAG syntax!
        #######################################################################
        self.select_clause = re.search(r'(?<=SELECT\s)(.*)(?=\sFROM)', self.str).group()
        self.select_clause = self.select_clause.split(',')
        self.select_clause = [i.strip() for i in self.select_clause]
        
        self.from_clause = re.search(r'(?<=FROM\s)(.*)', self.str).group()
