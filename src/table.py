import csv, os

class Table():
    def __init__(self, name):
        self.name = name

    def alter(self):
        #TODO
        pass

    def create(self, fields):
        if os.path.exists(self.name):
            raise Exception("!Failed to create table " + self.name + " because it already exists.")
        
        with open(self.name, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, lineterminator='\n', fieldnames=fields)
            writer.writeheader()
        print("Table " + self.name + " created.")   


    def drop(self):
        if not os.path.exists(self.name):
            raise Exception("!Failed to delete " + self.name + " because it does not exist.")
        
        os.remove(self.name)
        print("Table " + self.name + " deleted.")

    def select(self, select_clause):
        if not os.path.exists(self.name):
            raise Exception("!Failed to query " + self.name + " because it does not exist.")
        
        with open(self.name, newline='\n') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if select_clause == ['*']:
                    print(' |'.join(row))
                else:
                    #todo - placeholder to implement more advanced select syntax
                    pass

