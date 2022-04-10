import pandas as pd
import numpy as np
import requests
import json
import argparse
import logging
import math
import copy

from recipe import Recipe
from constants.column_names import ColumnNames as cn
from constants.units import Units as unit
from constants.hydration import Hydration
from nutrient.foodinfo import Nutrient
from nutrient.usda_reader import UsdaReader
from nutrient.ingredients import flours, wet, starter
from management.chain_manager import RecipeTree


def parse_options():
    parser = argparse.ArgumentParser(description='Calculate recipe')
    parser.add_argument("--fpath",
                        type=str,
                        help='file path',
                        required=True)
    parser.add_argument('--sheet',  metavar='sheet',
                        type=str,
                        help='sheet name',
                        required=True)
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                        const=sum, default=max,
                        help='sum the integers (default: find the max)')

    args = parser.parse_args()
    return args

def main():

    options = parse_options()

    bread = Bread(options)

    bread.analyze_hydration(bread.recipe)
    bread.analyze_flours(bread.recipe)
    bread.analyze_cooking_conditions(bread.recipe)
    new_hydration_percent = 80
    bread.change_hydration(new_hydration_percent, bread.recipe)
    print('Changed hydration to {}'.format(new_hydration_percent))
    print(bread.reindexed_recipe)
    bread.save_xl()




if __name__ == "__main__":
    main()
