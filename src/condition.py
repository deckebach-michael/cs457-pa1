'''
Name: condition.py
Author: Michael Deckebach
Date: 2022-10-25
Description: A class to represent SQL WHERE clauses with helper functionality
'''

class Condition:

    def __init__(self, str):
        self.str = str
        self.parsed = str.split()

        if len(self.parsed) != 3:
            raise Exception("Invalid condition. Please check syntax")

        self.field_name = self.parsed[0]
        self.operator = self.parsed[1]
        self.value = self.parsed[2].replace("'", '')





'''
JUST MESSING AROUND WITH A CONDITION CLASS

NEED TO FIGURE OUT FUNCTIONALITY FOR HOW TO TEST IF A CONDITION IS MET BY A RECORD!

TO BE CONTINUED. CAN ALWAYS DELETE THIS FILE AND BACK OUT AND COMMIT BASIC UPDATE 
FUNCTIONALITY (WITHOUT THE CONDITION CHECKING PART)
'''