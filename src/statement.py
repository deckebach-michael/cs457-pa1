import re

from database import Database
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
            
            # TODO

            # case use_regex_match:
            #     return Use_statement(str)

            # case alter_regex_match:
            #     return Alter_statement(str)

            # case select_regex_match:
            #     return Select_statement(str)

        else:
            raise Exception("Command not supported: " + str)

    def is_create_statement(self, str):
        return bool(re.search(r'(?i)(CREATE )\w{2}', str))

    def is_drop_statement(self, str):
        return bool(re.search(r'(?i)(DROP )\w{2}', str))

    def is_use_statement(self, str):
        return bool(re.search(r'(?i)(USE )\w{1}', str))

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

        if not self.correct_size():
            raise Exception("Invalid CREATE command. Please check syntax")

        self.type = self.parsed[1].upper()
        self.object_name = self.parsed[2]

        if not self.valid_type():
            raise Exception("Invalid CREATE command. Valid objects are CREATE DATABASE <name> or CREATE TABLE <name>")

    def correct_size(self):
        return self.num_words == 3

    def valid_type(self):
        return self.type in globals.KEYWORDS_OBJECTS
 
    def execute(self):
        if self.type == 'DATABASE':
            Database(self.object_name).create()
        elif self.type == 'TABLE':
            #TODO: write table
            pass

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
            #TODO: Write Table function
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