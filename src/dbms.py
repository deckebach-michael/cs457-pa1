'''
Name: dbms.py
Author: Michael Deckebach
Date: 2022-10-01
Description: A simple database management system implemented in pure python.
Creates a command line environment for simple SQL statements.

Supported statements and syntax include:

    ALTER TABLE <table> ADD <field> <datatype>;
    CREATE DATABASE <database>;
    CREATE TABLE <table> (<field> <datatype>, <field> <datatype>, ...);
    DROP DATABASE <database>;
    DROP TABLE <table>;
    SELECT * FROM <table>;
    USE <database>;

Additionally, the following commands are supported:

    EXIT - terminates the program

Semicolons (;) are strictly required to denote a SQL statement, but not required
for additional, non-SQL interface commands like EXIT.
'''

from statement import StatementFactory
from utils import get_input


def main(args=None):

    while True:
        try:
            statements = get_input()
            factory = StatementFactory()

            for s in statements:
                if s == 'EXIT':
                    print('All done.')
                    quit()

                stmnt = factory.make_statement(s)
                stmnt.execute()

        except Exception as exc:
            print(exc)
