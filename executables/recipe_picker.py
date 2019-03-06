import os
import sqlite3



class RecipePicker:
    """ Connects to db to pick recipe """

    def __init__(self):
        self.client = DbManager()


class DbManagerOld(object):
    """ Manages the database info """

    def __init__(self, dbname='example.db', user='admin', passwd='admin'):
        self.connection = sqlite3.connect(dbname)

    def create(self, tablename='bread'):
        # Create table
        #if self.connection.execute('''table bread exists'''):
        #    return
        self.connection.execute('''CREATE TABLE if not exists bread
                     (id text, name text, ingredient text, qty real, unit text)''')

    def insert(self, tablename='bread', columns=(), values=()):
        if not columns or not values:
            raise Exception('columns and values should be valid entries')
        if not len(columns) == len(values):
            raise Exception('columns and values are not equal lists')
        c = self.connection.cursor()
        # Insert a row of data
        sql_comm = 'INSERT INTO bread {} VALUES {}'.format(columns, values)
        c.execute(sql_comm)

        # Save (commit) the changes
        self.connection.commit()

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        self.connection.close()

    def query(self, query):
        pass

    def retreive(self, keyword):
        return ''

def main():
    picker = DbManager()
    picker.create('bread')
    recipe = ''


if __name__ == '__main__':
    main()