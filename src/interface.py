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

    BEGIN TRANSACTION - starts a transaction
    COMMIT - commits transaction activity or rolls back, depending on locking
    EXIT - terminates the program

Semicolons (;) are strictly required to denote a SQL statement, but not required
for additional, non-SQL interface commands like EXIT.
'''

import os
import shutil

from statement import StatementFactory
from utils import get_input


def main(args=None):

    # transaction tracking variables
    is_transaction = False
    locked_tables = []

    while True:

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
                    # transactions work in separate "_lock.csv" version
                    # so to "commit" a transaction we actually just need
                    # to swap out <table>_lock.csv with <table>.csv
                    for tbl in locked_tables:
                        os.remove(tbl)
                        os.rename(tbl + '_lock', tbl)
                        stmnt.commits += 1

                    locked_tables = []
                    is_transaction = False

                if is_transaction:
                    tbl_name = stmnt.get_table_name()

                    # this condition is necessary for non-table commands like
                    # BEGIN TRANSACTION and USE DATABASE
                    if tbl_name:
                        tbl_lock = tbl_name + '_lock'

                        if os.path.exists(tbl_lock):
                            if tbl_name in locked_tables:
                                stmnt.set_table_name(tbl_lock)
                                stmnt.execute()

                            # if table is locked and not by you, then another user must
                            # be committing a transaction on it!
                            else:
                                raise Exception("Error: Table " + tbl_name + " is locked!")
                        
                        else:
                            # create the _lock version and perform activity on it
                            shutil.copy(tbl_name, tbl_lock)
                            locked_tables.append(tbl_name)
                            stmnt.set_table_name(tbl_lock)
                            stmnt.execute()

                    else:
                        stmnt.execute()
                
                else:
                    stmnt.execute()

        except Exception as exc:
            print(exc)
