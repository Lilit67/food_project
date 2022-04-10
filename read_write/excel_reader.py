
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
    def __init__(self, workbook_path, sheet=None):
        self.filepath = workbook_path
        self.sheet = sheet
        self.name = sheet
        self.book = None

    def read_xl(self):
        """
        Assume an excel file with
        single spreadsheet

        Read to a dataframe
        :return:
        """
        if not os.path.exists(self.filepath):
            raise Exception("File path does not exist {}".format(self.filepath))
        if not os.path.splitext(self.filepath)[1] == '.xlsx':
            raise Exception("File should be Excel workbook")
        xl = pd.ExcelFile(self.filepath)
        self.recipe = pd.read_excel(xl, self.sheet)
        return self.recipe

    def read(self):
        self.read_xl()

    def all_sheet_names(self):
        """
        All sheets names in workbook
        :return:
        """
        xl = pd.ExcelFile(self.filepath)
        self.xl = xl
        print(dir(xl.book))
        self.book = xl.book
        names = xl.sheet_names
        for name in names:
            print(dir(xl.book.sheet_by_name(name)))
        return names

    def get_sheet_data(self, name):
        return self.xl.sheet_by_name(name)

    def write_xl(self, fpath, datafr, datafr2):
        """
        Write to excel file 2 sheets
        original and recalculated.
        :param fpath:
        :param datafr:
        :param datafr2:
        :return:
        """
        writer = pd.ExcelWriter(fpath)
        datafr.to_excel(writer, 'original recipe')
        datafr2.to_excel(writer, 'recalculated recipe')
        writer.save()

def parse_options():
    parser = argparse.ArgumentParser(description='Calculate recipe')
    parser.add_argument('-f', "--filepath",
                        metavar='filepath',
                        type=str,
                        help='file path',
                        required=True)

    args = parser.parse_args()
    return args

def main():
    args = parse_options()

    reader = ExcelReader(args.filepath)
    data = reader.read()
    print(reader.all_sheet_names())
    #print(dir(reader))



if __name__ == '__main__':
    main()
