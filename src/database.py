'''
Name: database.py
Author: Michael Deckebach
Date: 2022-10-01
Description: Implementation of a Database class, which represents a traditional
relational database. Databases are implemented as directories.
'''

import os


class Database():
    def __init__(self, name):
        self.name = name

    def create(self):
        if os.path.exists(self.name):
            raise Exception("!Failed to create database " + self.name + " because it already exists.")
        
        os.makedirs(self.name)
        print("Database " + self.name + " created.")        

    def drop(self):
        if not os.path.exists(self.name):
            raise Exception("!Failed to delete " + self.name + " because it does not exist.")
        
        ################################### !! ###############
        os.rmdir(self.name) ## NEED TO MAKE THIS recursive so tables don't have to first be dropped
        ################################### !! ###############
        
        
        print("Database " + self.name + " deleted.")

    def use(self):
        # This file must be on the same level of __main__.py to ensure folder (database) integrity
        # as it relies on os.path.realpath to move between various database folders
        # os.chdir(os.path.dirname(os.path.realpath(__file__)) + '/' + self.name)
        os.chdir(os.path.dirname(__file__) + '/..')

        if not os.path.exists(self.name):
            raise Exception("!Failed to use " + self.name + " because it does not exist.")

        os.chdir(self.name)
        print('Using database ' + self.name)
