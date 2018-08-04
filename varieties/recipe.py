
import pandas as pd
import requests
import json
import argparse
import logging
import os
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

    def clean_data(self):
        """ Override """
        raise Exception('This function should be overriden')


    def reindex1(self, df):
        df.set_index([cn.step_no, cn.ingredient], inplace=True)
        df.sort_index(inplace=True)
        return df1

    def reindex(self, df):
        df1 = df.set_index(['stepNo', cn.ingredient])
        df1.sort_index(inplace=True)
        print('Reindexed: {}'.format(df1))

        return df1


    def reorder_columns(self, df):
        """ Call before reindexing"""
        cn_inst = cn()
        columns = cn_inst.get_ordered()

        df = df[columns]
        #print(df)
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

        Faster alternative: df.set_value('C', 'x', 10)
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
        #df = df.at[row, col] = val

        df.loc[index, col] = val
        return df

    # FORMATING and OUTPUT

    def df_to_json(self, df):
        json_obj = df.to_json(orient='records')
        return json_obj

    def to_xl(self, df, fpath=None):
        """
        Save to excel file
        :param fpath:
        :return:
        """
        original_file_name = os.path.split(self.workbook)[-1]
        writer = pd.ExcelWriter('./output/' + original_file_name + '_output.xlsx')
        df.to_excel(writer, self.sheet + '_original')
        self.recalculated = df
        self.recalculated.to_excel(writer, self.sheet + '_recalculated recipe')
        writer.save()

    def df_to_json_old(self, df):
        results = {}
        for key, df_gb in df.groupby('stepNo'):
            results[str(key)] = df_gb.to_dict('results')

        self._logger.info(json.dumps(results, indent=4))
        return results

    def df_to_matrix(self, df):
        matix_type = df.as_matrix()
        self._logger.info(matix_type)
        return matix_type



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
