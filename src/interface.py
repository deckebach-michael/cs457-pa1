'''
Name: interface.py
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

import os

from statement import StatementFactory
from utils import get_input


def main(args=None):

    while True:

        is_transaction = False
        locked_tables = []

        try:
            statements = get_input()
            factory = StatementFactory()

            for stmt_str in statements:
                if stmt_str == 'EXIT':
                    print('All done.')
                    quit()

                stmnt = factory.make_statement(stmt_str)

                if stmnt.start_transaction:
                    is_transaction = True

                if stmnt.end_transaction:

                    for tbl in locked_tables:
                        os.remove(tbl)
                        os.rename(tbl + '_lock', t)

                    locked_tables = []
                    is_transaction = False
                    
                stmnt.execute()

        except Exception as exc:
            print(exc)
