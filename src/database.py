'''
Name: database.py
Author: Michael Deckebach
Date: 2022-10-01
Description: Implementation of a Database class, which represents a traditional
relational database. Databases are implemented as directories. Implements 
functionality for CREATE DATABASE, DROP DATABASE, and USE DATABASE commands.
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
        
        # Remove all tables (files) inside the database folder, then remove the folder
        for file in os.listdir(self.name):
            os.remove(self.name + '/' + file)
        os.rmdir(self.name)
        
        print("Database " + self.name + " deleted.")

    def use(self):
        # BUG: This file must be on the same level of dbms.py to ensure folder 
        # (database) integrity as it relies on os.path.realpath to move between 
        # various database folders:
        # os.chdir(os.path.dirname(os.path.realpath(__file__)) + '/' + self.name)
        # Consider improving with more absolute & less relative approach in future.
        os.chdir(os.path.dirname(__file__) + '/..')

        if not os.path.exists(self.name):
            raise Exception("!Failed to use " + self.name + " because it does not exist.")

        os.chdir(self.name)
        print('Using database ' + self.name)
