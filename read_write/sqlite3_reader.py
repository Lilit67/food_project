import os
import sqlite3

from excel_reader import ExcelReader


class Sqlite3Reader(object):
    """ Manages the database info """

    def __init__(self, dbname='recipe.db', user='admin', passwd='admin'):
        self.connection = sqlite3.connect(dbname)

    def create_db(self, tablename='bread'):
        # Create table
        self.connection.execute('''CREATE TABLE if not exists bread
                     (id text, name text, ingredient text, qty real, unit text)''')


    def create_table(self, table_name, entries=None, prim_key=None):
        cursor = self.connection.cursor()
        tables = self.list_tables()

        if table_name not in tables:
            command = "CREATE TABLE {} (id INT AUTO_INCREMENT PRIMARY KEY, " \
                      "recipe_name VARCHAR(255), category VARCHAR(255), " \
                      "tags VARCHAR(255))".format(table_name)
            cursor.execute(command)

    def create_recipe(self, recipe):
        """
        Create a new project into the projects table
        :param conn:
        :param project:
        :return: project id
        """
        sql = ''' INSERT INTO recipes(recipe_name,category,tags)
                  VALUES(?,?,?) '''
        cur = self.connection.cursor()
        cur.execute(sql, recipe)
        return cur.lastrowid

    def add_column(self, table, colname, type, primary=False):
        cursor = self.connection.cursor()
        cursor.execute("ALTER TABLE recipes ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")

    def list_tables(self):
        tablist  = []
        cursor = self.connection.cursor()
        tables = cursor.execute("select name from sqlite_master where type = 'table';")
        tables = tables.fetchall()
        for entry in tables:
            for t in entry:
                tablist.append(t)
        return tablist

    def list_recipes(self):
        cmd = 'SELECT * from recipes'
        cursor = self.connection.cursor()
        records = cursor.execute(cmd)
        return records.fetchall()


def main():
    picker = Sqlite3Reader()
    picker.create_db('bread_db')
    reader = ExcelReader('recipes/napoleon/my_napoleon.xlsx', "ingredient")
    print(reader)
    recipe = reader.read_xl()
    print(recipe)
    print('Tables in db {}'.format(picker.list_tables()))
    picker.create_table(table_name='recipes')
    recp = ('croissant', 'savory', 'sourdough, baked')
    r_id = picker.create_recipe(recp)
    print(r_id)
    print(picker.list_recipes())




if __name__ == '__main__':
    main()