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
import shutil

from statement import StatementFactory
from utils import get_input


def main(args=None):

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

                    for tbl in locked_tables:
                        os.remove(tbl)
                        os.rename(tbl + '_lock', tbl)
                        stmnt.commits += 1

                    locked_tables = []
                    is_transaction = False

                if is_transaction:
                
                    tbl_name = stmnt.get_table_name()

                    if tbl_name:
                        tbl_lock = tbl_name + '_lock'

                        if os.path.exists(tbl_lock):

                            if tbl_name in locked_tables:
                                stmnt.set_table_name(tbl_lock)
                                stmnt.execute()
                            else:
                                raise Exception("Error: Table " + tbl_name + " is locked!")
                        else:
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
