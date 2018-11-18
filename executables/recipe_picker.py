import os
import sqlite3



class RecipePicker:
    """ Connects to db to pick recipe """

    def __init__(self):
        self.client = DbManager()


    def pick_random(self, criteria=None):
        pass


class DbManager:
    """ Manages the database info """

    def __init__(self, dbname=None, user='admin', passwd='admin'):
        conn = sqlite3.connect('example.db')

    def create(self, tabename='bread'):
        # Create table
        c.execute('''CREATE TABLE bread
                     (id text, name text, ingredient text, qty real, unit text)''')

    def insert(self, table='bread'):
        c = conn.cursor()
        # Insert a row of data
        c.execute("INSERT INTO bread VALUES ('8i9uy65','white_sourdough','RHAT',100,35.14)")

        # Save (commit) the changes
        conn.commit()

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        conn.close()


    def retreive(self):
        return ''


