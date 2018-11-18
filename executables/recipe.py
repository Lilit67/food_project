
import pandas as pd
import requests
import json
import argparse
import logging
import os
import xlsxwriter
from management.chain_manager import RecipeTree
from constants.column_names import ColumnNames as cn


class Recipe(object):
    def __init__(self, options):
        self.reader = ExcelReader(options)
        self.sheet = options.sheet
        self.workbook = options.workbook
        self.recipe = self.reader.read_xl()

        self.df_manager = RecipeTree()
        # set the root as original recipe
        self.df_manager.add_node(self.recipe)
        self._logger = logging.getLogger(__class__.__name__)


    class Decorators:

        @classmethod
        def recorder(cls, func):
            def function_wrapper(*args, **kwargs):
                print("Before calling " + func.__name__)
                res = func(*args, **kwargs)
                res1 = copy.copy(res)
                print(kwargs)
                Recipe.history.append(res1)
                print("After calling " + func.__name__)

            return function_wrapper


    def clean_data(self, df):
        """ Override """
        raise Exception('This function should be overriden')


    def reindex1(self, df):
        df.set_index([cn.step_no, cn.ingredient], inplace=True)
        df.sort_index(inplace=True)
        return df1

    def reindex(self, df):
        """
        Reindex dataframe to stepNo/indredient MultiIndex
        :param df:
        :return:
        """
        df1 = df.set_index(['stepNo', cn.ingredient])
        df1.sort_index(inplace=True)
        print('Reindexed: {}'.format(df1))

        return df1


    def reorder_columns(self, df):
        """ Reorders columns to standard predefine order """
        cn_inst = cn()
        columns = cn_inst.get_ordered()

        df = df[columns]
        return df

    def get_ingredients(self, df):
        """
        return list of ingredients
        assume a dataframe object
        :return:
        """
        ingredients = df[cn.ingredient]
        return ingredients

    def columns(self, df):
        return df.columns.tolist()

    def ingredient_names(self, df):

        dfs = df.reset_index()
        return dfs.ingredient.values

    def step_numbers(self, df):
        dfs = df.reset_index()
        return dfs.stepNo.values

    def get_size(self, df):
        """ what is this for? """
        dfs = df.groupby(['stepNo', 'ingredient']).size()

    def ingredient_names_no_reindexed(self, df):
        """
        Return the "ingredient" column values
        as a list
        :return: list of ingredient names
        """
        dfList = df.ingredient.values
        dfList = [x for x in dfList if x]
        return dfList

    def total_time(self, df):
        """ Return sum of the column time """
        # TODO: what if user do not put any time?
        # smart calculation? Think about it
        pass

    def scale_ingredients_df(times):
        """
        Scale ingredients,
        simple scaling

        :param ingredients:
        :param times:
        :return:
        """
        df = pd.dataframe(self.recipe)
        ingredients = self.get_ingredients(df)
        scaled = ingredients['amount'] * times

        return scaled

    def set_at(self, df, col, index, val):
        """
        Set value at specific location,
        operation is done on same dataframe
        index can be multiindex
        Faster alternative: df.set_value('C', 'x', 10) - deprecated?
        :param df:
        :param col:
        :param row:
        :param val:
        :return:
        """
        print(row, col, val, df)
        if not isinstance(df, pd.DataFrame):
           raise Exception("First paramemter should be of type dataframe")
        #df.loc['[21-23)', 'M', '[10000-20000)'] = 2
        df.loc[index, col] = val
        return df

    def get_at(self, df, row, col):
        """
        Return value at row, column

        :param col:
        :param row:
        :param val:
        :return:
        """
        return df.loc[row, col]

    def _get_matching_records(self, df, ingredients):
        """
        Common call
        :param ingredients:
        :return: dataframe object
        """

        df1 = df.loc[df[cn.ingredient].isin(ingredients)]
        return df1

    def set_matching_records(self, df, row, col, values):
        pass

    # FORMATING and OUTPUT
    def df_to_json(self, df):
        json_obj = df.to_json(orient='records')
        return json_obj

    def to_xl(self, df, fpath=None, name=None):
        """
        Save to excel file
        :param fpath:
        :return:
        """
        original_file_name = os.path.split(self.workbook)[-1]
        writer = pd.ExcelWriter('./output/' + original_file_name + '_2.xlsx')
        df.to_excel(writer, self.sheet + '_original')
        self.recalculated = df
        self.recalculated.to_excel(writer, self.sheet + '_rec')
        writer.save()


    def save_xl(self):
        original_file_name = os.path.split(self.workbook)[-1]
        new_file = './output/' + original_file_name + '_2.xlsx'
        if os.path.exists(new_file):
            os.remove(new_file)
        writer = pd.ExcelWriter(new_file, engine='xlsxwriter')

        print("writing to {}".format(new_file))
        workbook = writer.book

        cell_format = workbook.add_format({'font_size': 22})
        cell_format.set_font_size(22)
        # Add some cell recipes2.
        format1 = workbook.add_format({'num_format': '#,##0.00'})
        format2 = workbook.add_format({'num_format': '0%'})

        for index, df in enumerate(self.history):
            sheetname = self.sheet + '_' + str(index)
            df.to_excel(writer, index=False, sheet_name=sheetname)
            # df.to_excel(writer_orig, index=False, sheet_name='report')
            worksheet = writer.sheets[sheetname]
            worksheet.set_column('A:Z', None, cell_format)
            worksheet.set_row(1, None, cell_format)
            # Set the column width and format.
            worksheet.set_column('B:B', 18, format1)
        writer.save()

    def df_to_csv(self, file_name):
        """ To csv plus header info in one sheet """
        print('Writing to {}'.format(file_name))
        accumulator = ''
        for index, df in enumerate(self.history):
            df[['amount']] = df[['amount']].astype('int64')
            #df['hydration'] = '<span style="color: #00CD00">Active</span>'
            data = df.to_csv(path_or_buf=None, sep='\t', encoding='utf-8')
            accumulator += data + '\n'
            accumulator += 'Total dough weight\n'.format(self.total_dough_weight(df))

        with open(file_name, 'w') as f:
            f.write(accumulator)

        return True


    def df_to_matrix(self, df):
        matix_type = df.as_matrix()
        self._logger.info(matix_type)
        return matix_type


    def recorder(self, func):
        def function_wrapper(df):
            print("Before calling " + func.__name__)
            res = func(x)
            res1 = copy(res)
            self.history.append(res1)
            print("After calling " + func.__name__)
        return function_wrapper


class CSVReader:
    def __init__(self, options):
        self.file = options.csv
        self.df = CSVReader.read_csv(self.file)

    @classmethod
    def read_csv(cls, input_path):
        df = pd.read_csv(input_path)

        return df

    def write_csv(self, df):
        return NotImplemented

class ExcelReader:
    """
    Can read all the different
    types of recipes and craeae a data
    frame format from them
    """
    def __init__(self, options):
        self.file = options.workbook
        self.sheet = options.sheet
        self.name = options.sheet

    def read_xl(self):
        """
        Assume an excel file with
        single spreadsheet

        Read to a dataframe
        :return:
        """
        xl = pd.ExcelFile(self.file)
        names = xl.sheet_names
        name = names[0]
        #self.recipe = xl.parse(name)
        self.recipe = pd.read_excel(xl, self.sheet)

        return self.recipe

    def write_xl(self, fpath, datafr1, datafr2):
        writer = pd.ExcelWriter(fpath)
        datafr.to_excel(writer, 'original recipe')

        datafr2.to_excel(writer, 'recalculated recipe')
        writer.save()
