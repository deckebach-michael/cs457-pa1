'''
Name: utils.py
Author: Michael Deckebach
Date: 2022-10-01
Description: A collection of global variables and utility functions 
used by the database management system
'''

###############################################################################
# GLOBAL VARIABLES
###############################################################################

KEYWORDS_COMMANDS = {
    'ALTER',
    'CREATE',
    'DROP',
    'SELECT',
    'USE',
}

KEYWORDS_OBJECTS = {
    'DATABASE',
    'TABLE'
}

###############################################################################
# UTILITY FUNCTIONS
###############################################################################

def get_input():

    user_input = input()

    if _ends_with_semicolon(user_input) or _is_exit(user_input):
        return _split_statements(user_input)

    else:
        raise Exception("Command does not end with a semicolon. Please try again.")

###############################################################################
# INTERNAL HELPER FUNCTIONS FOR UTILITY FUNCTIONS
# Not to be called directly
###############################################################################

def _ends_with_semicolon(str):
    if str.endswith(';'):
        return True
    return False

def _is_exit(str):
    if str.endswith('EXIT'):
        return True
    return False

def _split_statements(str):
    
    split = str.split(';')[0:-1]

    if str.endswith('EXIT'):
        split.append('EXIT')

    return split
