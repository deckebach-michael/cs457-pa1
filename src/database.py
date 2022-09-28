import os

class Database():
    def __init__(self, name):
        self.name = name

        if os.path.exists(name):
            raise Exception("!Failed to create database " + name + " because it already exists.")
        
        os.makedirs(name)        

    def load(self, name):
        os.chdir(name)

    def delete(self):
        os.rmdir(self.name)