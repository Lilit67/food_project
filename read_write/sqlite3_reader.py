import os
import sqlite3
import argparse

from excel_reader import ExcelReader
from csv_reader import CSVReader
from text_reader import TextReader


class Reader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.filetype = None
        self.data = None
        self.steps = None
        self.steps = None

    def read(self):
        if not os.path.exists(self.filepath):
            raise Exception("File not found {}".format(self.filepath))
        self.filetype = os.path.splitext(self.filepath)[1]
        if self.filetype == '.xls':
            # read excel sheets, these are expected to be there, TODO: error if not
            ingredient_reader = ExcelReader(self.filepath, 'ingredients')
            step_reader = ExcelReader(self.filepath, 'steps')
            data_reader = ExcelReader(self.filepath, 'data')
            # get as dataframes
            ingredients = ingredient_reader.read_xl()
            self.ingredients = ingredients.fillna(0)
            steps = step_reader.read_xl()
            self.steps = steps.fillna(0)
            self.data = data_reader.read_xl()
        elif self.filetype == '.txt':
            reader = TextReader(self.filepath)
            self.data = reader.read()
        elif self.filetype == '.csv':
            reader = CSVReader(self.filepath)
            self.data = reader.read()
        else:
            raise Exception("Incorrect file type {}".format(self.filetype))

        return self.data



class DBManager(object):
    """ Manages the database info """

    def __init__(self, dbpath='recipe67.db'):
        self.dbpath = dbpath
        self.connection = sqlite3.connect(dbpath)

    # TABLE CREATION
    def create_table(self, table_name, entries=None, prim_key=None):
        cursor = self.connection.cursor()
        tables = self.list_tables()

        if table_name not in tables:
            command = "CREATE TABLE {} (id INT AUTO_INCREMENT PRIMARY KEY, " \
                      "recipe_name VARCHAR(255), category VARCHAR(255), " \
                      "tags VARCHAR(255))".format(table_name)
            cursor.execute(command)
            cursor.commit()

    def create_recipes_table(self):
        """
        index	recipe_id	ingredient_name	amount	unit	recipe_step_id
        :return:
        """
        cursor = self.connection.cursor()

        command = "CREATE TABLE if not exists recipes (id INT PRIMARY KEY, " \
                  "recipe_name VARCHAR(255), " \
                  "source_file_path VARCHAR(255), " \
                  "source_file_type VARCHAR(255))"

        cursor.execute(command)

    def create_ingredients_table(self):
        """
        index	recipe_id	recipe_step_id	ingredient_name	amount	unit
        :return:
        """
        cursor = self.connection.cursor()

        command = "CREATE TABLE if not exists ingredients " \
                  "(id INTEGER PRIMARY KEY, " \
                  "recipe_id VARCHAR(255), " \
                  "recipe_step_id INTEGER, " \
                  "ingredient_name VARCHAR(255), " \
                  "ingredient_amount INTEGER, " \
                  "measurement_unit VARCHAR(255))"
        cursor.execute(command)
        self.connection.commit()

    def create_steps_table(self):
        """
        index	recipe_id	recipe_step_id step_name	step_description	notes	time	time_unit	temperature temperature unit

        :return:
        """
        cursor = self.connection.cursor()

        command = "CREATE TABLE if not exists steps (id INT PRIMARY KEY, " \
                  "recipe_id VARCHAR(255), recipe_step_id INT, step_name VARCHAR(255), " \
                  "step_description VARCHAR(255), notes VARCHAR(255), time int, time_unit VARCHAR(255), " \
                  "temperature VARCHAR(255), temperature_unit VARCHAR(255))"
        cursor.execute(command)


    def create_data_table(self):
        """
        recipe_id
        date_of_bake
        variation from recipe
        dough_appearance
        baked result
        sergei
        toma
        christina
        recipe source
        flour used
        Notes at dough handling
        cause of success or failure (outcome cause)
        notes on bake process
        bake time
        portion %
        autolyze
        stretch an d fold
        bulk fermentation
        :return:
        """
        cursor = self.connection.cursor()

        command = "CREATE TABLE if not exists data (id INT AUTO_INCREMENT PRIMARY KEY, " \
                  "recipe_id VARCHAR(255), step_name VARCHAR(255), recipe_step_id VARCHAR(255), " \
                  "step_description VARCHAR(255))"
        cursor.execute(command)

    # DATA INSERTION

    def insert_recipe(self, recipe_id, recipe_name,
                      source_file_path, source_file_type):
        """
        id	recipe_name	source_file_path	source_file_type
        :param conn:
        :param project:
        :return: project id
        """
        recipe = (recipe_name, source_file_path, source_file_type)
        sql = ''' INSERT INTO recipes(recipe_name,source_file_path, source_file_type)
                  VALUES(?,?,?) '''
        cur = self.connection.cursor()
        try:
            cur.execute(sql, recipe)
            return cur.lastrowid
        except sqlite3.IntegrityError as e:
            print(e)
            print('Record with id {} already in table "recipes"'.format(recipe_id))

    def insert_ingredient(self, recipe_id,
                          ingredient_name, amount,
                          unit, recipe_step_id):
        """
        index	recipe_id	ingredient_name	amount	unit	recipe_step_id
        Create a new task
        :param conn:
        :param task:
        :return:
        """
        cur = self.connection.cursor()

        ingredient = (str(recipe_id), str(recipe_step_id),
                          ingredient_name, int(amount),
                          unit)

        sql = ''' INSERT INTO ingredients(recipe_id, recipe_step_id, ingredient_name,ingredient_amount,measurement_unit)
                  VALUES(?,?,?,?,?) '''

        cur.execute(sql, ingredient)
        return cur.lastrowid

    def insert_step(self,
                    recipe_id,
                    recipe_step_id,
                    step_name,
                    step_description,
                    notes,
                    time,
                    time_unit,
                    temperature,
                    temperature_unit):
        """
        index	recipe_id	recipe_step_id step_name	step_description	notes	time	time_unit	temperature temperature unit
        :param conn:
        :param task:
        :return:
        """
        cur = self.connection.cursor()

        step = (str(recipe_id),
                int(recipe_step_id),
                step_name,
                step_description, notes,
                int(time), time_unit, int(temperature),
                temperature_unit)


        sql = ''' INSERT INTO steps(recipe_id, 
                recipe_step_id,
                step_name, 
                step_description, 
                notes,
                time, 
                time_unit, 
                temperature, 
                temperature_unit)
                VALUES(?,?,?,?,?,?,?,?,?) '''

        cur.execute(sql, step)
        return cur.lastrowid

    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Exception as e:
            print(e)

        return None

    def add_column(self, table, colname, type, primary=False):
        cursor = self.connection.cursor()
        cursor.execute("ALTER TABLE recipes ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")

    def show_tables(self):
        """
        SELECT sql FROM sqlite_master
        WHERE tbl_name = 'table_name' AND type = 'table'
        :return:
        """
        tablist  = []
        cursor = self.connection.cursor()
        tables = cursor.execute("select name from sqlite_master where type = 'table';")
        tables = tables.fetchall()
        for entry in tables:
            for t in entry:
                tablist.append(t)
        return tablist

    def show_table_colnames(self, name):
        cursor = self.connection.cursor()
        cmd = 'PRAGMA table_info({})'.format(name)
        records = cursor.execute(cmd)
        return records.fetchall()

    def query(self, qstr):
        cursor = self.connection.cursor()
        records = cursor.execute(qstr)
        return records.fetchall()

    def list_table(self, name):
        cmd = "select * from {}".format(name)
        cursor = self.connection.cursor()
        records = cursor.execute(cmd)
        return records.fetchall()

def record_ingredients_pandas(picker, ingredients, recipe_id):
    """
    dataframe to db
    :param ingredients:
    :return:
    """
    columns = list(ingredients.columns.values)


    if not columns == ['index', 'recipe_id', 'recipe_step_id', 'ingredient_name', 'amount', 'unit']:
        raise Exception('Incorrect recipe entries given: {}'.format(columns))

    for i in range(ingredients.shape[0]):
        record = ingredients.iloc[i]
        record = record.tolist()
        picker.insert_ingredient(recipe_id=record[1], recipe_step_id=record[2],
                                 ingredient_name=record[3], amount=record[4], unit=record[5])

def record_ingredients(picker, ingredients, recipe_id):
    for i in ingredients:
        picker.insert_ingredient(recipe_id=recipe_id, recipe_step_id=1,
                                 ingredient_name=i.name, amount=i.amount,
                                 unit=i.unit)

def record_steps(picker, steps, recipe_id):
    """
    dataframe to db
    :param ingredients:
    :return:
    """
    columns = list(steps.columns.values)
    expected = ['index',
                'recipe_id',
                'recipe_step_id',
                'step_name',
                'step_description', 'notes',
                'time', 'time_unit', 'temperature',
                'temperature_unit']
    if not columns == expected:
        raise Exception('Incorrect step entries given: {}:{}'.format(columns, expected))

    for i in range(steps.shape[0]):
        record = steps.iloc[i]
        record = record.tolist()
        picker.insert_step(recipe_id=record[1],
                           recipe_step_id=record[2],
                           step_name=record[3],
                           step_description=record[4],
                           notes=record[5],
                           time=record[6],
                           time_unit=record[7],
                           temperature=record[8],
                           temperature_unit=record[9])

def record_data(picker, data, recipe_id):
    """
    dataframe to db
    :param ingredients:
    :return:
    """
    columns = list(data.columns.values)
    expected = ['index',
                'recipe_id',
                'recipe_step_id',
                'step_name',
                'step_description', 'notes',
                'time', 'time_unit', 'temperature',
                'temperature_unit']
    if not columns == expected:
        raise Exception('Incorrect step entries given: {}:{}'.format(columns, expected))

    for i in range(data.shape[0]):
        record = steps.iloc[i]
        record = record.tolist()
        picker.insert_data(recipe_id=record[1],
                           recipe_step_id=record[2],
                           step_name=record[3],
                           step_description=record[4],
                           notes=record[5],
                           time=record[6],
                           time_unit=record[7],
                           temperature=record[8],
                           temperature_unit=record[9])



def parse_options():
    example = '''python3 read_write/sqlite3_reader.py'''
    parser = argparse.ArgumentParser(description='Reads and writes to sqlite3',
                                     epilog=example)
    parser.add_argument('--db',
                        default='bread_db',
                        required=False,
                        help='endtime string, example: Nov 22 2018 2:30PM')
    parser.add_argument('--recipe-path', required=True,
                        default='recipes/napoleon/my_napoleon.xlsx',
                        help='Path to Excel file with recipe')
    parser.add_argument('--sheet-name', required=False,
                        help='Worksheet name inside Excel recipe file')
    parser.add_argument('--worksheet', required=False,
                        help="ingredients")
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                        const=sum, default=max,
                        help='sum the integers (default: find the max)')

    args = parser.parse_args()
    return args


def main():
    args = parse_options()

    # Database init, empty tables, only once needed
    picker = DBManager(args.db)
    picker.create_recipes_table()
    picker.create_ingredients_table()
    picker.create_steps_table()
    picker.create_data_table()


    recipe_file = args.recipe_path
    try:
        reader = Reader(recipe_file)
        data = reader.read()
        print(data)

        # insert recipe record first
        recipe_path = os.path.abspath(args.recipe_path)
        recipe_dir, extension = os.path.splitext(recipe_path)
        recipe_name = os.path.split(recipe_dir)[1]
        recipe_id = recipe_name
        print('Recipe name is {}'.format(recipe_name))
        picker.insert_recipe(recipe_id, recipe_name, recipe_path, extension)

        # Add ingredients
        record_ingredients(picker, data.ingredients, recipe_id)
        # Add steps
        if False:
            record_steps(picker, steps, recipe_id)

            # Add data
            record_data(picker, data, recipe_id)


        print(picker.list_table('recipes'))
        print('Tables in db {}'.format(picker.show_tables()))
        print('Showing records in table "ingredients" {}'.format(picker.list_table('ingredients')))

        print('Showing records in table "steps" {}'.format(picker.list_table('steps')))
    except Exception:
        import traceback
        traceback.print_exc()



if __name__ == '__main__':
    main()