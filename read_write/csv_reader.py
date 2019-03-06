import pandas as pd
import requests
import json
import argparse
import logging
import os
import xlsxwriter
from management.chain_manager import RecipeTree
from constants.column_names import ColumnNames as cn

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