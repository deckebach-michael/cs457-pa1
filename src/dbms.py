from operator import contains
import re, os

import globals, statement


def main(args=None):

    while True:

        try:
            statements = get_input()
            factory = statement.StatementFactory()

            for s in statements:
                if s == 'EXIT':
                    quit()

                stmnt = factory.make_statement(s)
                stmnt.execute()

        except Exception as exc:
            print(exc)



def get_input():

    user_input = input()

    if ends_with_semicolon(user_input) or is_exit(user_input):
        return split_statements(user_input)

    else:
        raise Exception("Command does not end with a semicolon. Please try again.")

def ends_with_semicolon(str):
    if str.endswith(';'):
        return True
    return False

def is_exit(str):
    if str.endswith('EXIT'):
        return True
    return False


def split_statements(str):
    
    split = str.split(';')[0:-1]

    if str.endswith('EXIT'):
        split.append('EXIT')

    return split










# 
    # raise Exception("could not get input")

    # user_input = parse_statements(input())

    # for statement in user_input:
    #     # print(is_create_db(statement))
    #     # clausified = clausify(statement)
    #     # print(clausified)
    #     # # print(is_command(clausified))
    #     # print()
    
    #     create_db(statement)





# def clausify(statement):
#     return statement.split()

# def normalize(word):
#     return word.strip().upper()

# def is_command(clausified):
#     first_clause = normalize(clausified[0])
#     return first_clause in globals.KEYWORDS_COMMANDS




# def is_create_db(statement):
#     return bool(re.search(r'(?i)(CREATE DATABASE )\w+', statement))

# def create_db(statement):
#     if is_create_db(statement):
#         clausified = clausify(statement)
#         os.mkdir(clausified[2])
