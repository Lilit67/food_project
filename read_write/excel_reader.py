
import pandas as pd
import requests
import json
import argparse
import logging
import os
import xlsxwriter
#from management.chain_manager import RecipeTree
#from constants.column_names import ColumnNames as cn


class ExcelReader:
    """
    Manipulates on excel files
    """
    def __init__(self, workbook_path, sheet):
        self.file = workbook_path
        self.sheet = sheet
        self.name = sheet

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
