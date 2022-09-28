import re

from database import Database
import globals


class StatementFactory:

    def __init__(self):
        pass

    def make_statement(self, str):

        if self.is_create_statement(str):
            return CreateStatement(str)
            
            # TODO
            # case drop_regex_match:
            #     return Drop_statement(str)

            # case use_regex_match:
            #     return Use_statement(str)

            # case alter_regex_match:
            #     return Alter_statement(str)

            # case select_regex_match:
            #     return Select_statement(str)

        else:
            raise Exception("Command not supported: " + str)

    def is_create_statement(self, str):
        return bool(re.search(r'(?i)(CREATE DATABASE )\w+', str))

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
        print("TODO: Inside CreateStatement.execute()")

        if self.type == 'DATABASE':
            Database(self.object_name)
        if self.type == 'TABLE':
            # TODO: write table
            pass
