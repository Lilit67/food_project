import pandas as pd
import numpy as np
import requests
import json
import argparse
import logging
import math

from recipe import Recipe
from constants.column_names import ColumnNames as cn
from constants.units import Units as unit
from constants.hydration import Hydration
from nutrient.foodinfo import Nutrient
from nutrient.usda_reader import UsdaReader
from nutrient.ingredients import flours, wet, starter
from management.chain_manager import RecipeTree

class RecipeClassifier:
    sourdough = 'sourdough'
    croissant = 'croissant'


# TODO: move
def color_negative_red(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    color = 'red' if val < 0 else 'black'
    return 'color: %s' % color

class Bread(Recipe):
    def __init__(self, options):
        """
        Initialization is with first version
        After change the new version will be
        appended to recipe_variations
        :param options:
        """
        Recipe.__init__(self, options)
        self._logger = logging.getLogger(self.__class__.__name__)
        self.original = self.recipe
        if self.recipe.empty:
            raise Exception('Recipe is empty!')
        df = self.original
        df = self.remove_empty_rows_columns(df)
        min_cols = cn.min_columns()
        df = self.leave_these_columns(df, min_cols)
        print(df)

        #df = self.clean_data(df)
        self._hydration = self.hydration(df)

        self._water_weight = self.wet_weight(df)

        df = self.set_bakers_percents(df)
        print('Returned from setting bakers percents {}'.format(df))
        df2 = self.fill_usda(df)
        print('After filling usda {}'.format(self.df_to_matrix(df2)))

    def record(self, df):
        """
        At users request the recipe variant should
        be saved as a variation of original recipe
        :param df:
        :return:
        """
        self.df_manager.add_node(self.latest, df)

    def fill_usda(self, df):
        """
        Fills in the usda database
        query results
        :param df:
        :return:
        """
        usda = UsdaReader()
        for index, row in df.iterrows():
            ingredient = row[cn.ingredient]
            if self.cell_valid(ingredient, celltype=str):
                #print(row['ingredient'], row['amount'], index)
                found_info = usda.get_product_info(ingredient)
                if found_info:
                    found_code = found_info.get('ndbno')
                    found_name = found_info.get('name')
                    print(found_code, found_name)
                    df.loc[index, cn.code] = found_code
                    df.loc[index, cn.usda_name] = found_name
        #print(df)
        return df


    def set_ingredient_types(self, df):
        for name in self.ingredient_names(df):
            if name in flours:
                self.set_at(df, col='type 1', row=name, val='dry')
        return df

# DATA CLEANUP, MISSING DATA

    def add_missing_columns(self, df):
        """
        Add missing from the whole list.
        Do not use it until better
        cleanup and reading can be done
        """
        existing_cols = self.columns(df)
        ingredients = self.get_ingredients(df)
        i_len = len(ingredients)
        column_names = cn.column_names()
        #print(column_names)
        for c in column_names:
            if c not in existing_cols:
                df[c] = [0] * i_len
        self._logger.info('Added missing columns, {}'.format(df))
        return df

    def remove_empty_rows_columns(self, df):
        df1 = df.dropna(thresh=2)
        df2 = df1.dropna(axis=1, how='all')
        return df2

    def leave_these_columns(self, df, min_cols):
        """
        Remove all but the minimum columns
        with data: ingredient, step, amount, unit
        :param df:
        :return:
        """
        all_cols = self.columns(df)
        to_drop = []
        for col in all_cols:
            if col not in min_cols:
                to_drop.append(col)
        df1 = df.drop(to_drop, axis=1)
        return df1


    def clean_data(self, df):
        df = self.add_missing_columns(df)
        df[cn.weight].fillna(0, inplace=True)
        df[cn.step_no].fillna(method='ffill', inplace=True)
        df[cn.step_name].fillna(method='ffill', inplace=True)
        df[cn.unit].fillna('gr', inplace=True)
        df[cn.BP].fillna(0, inplace=True)
        df[cn.code].fillna(0, inplace=True)
        df[cn.time_in_minutes].fillna(0, inplace=True)
        df[cn.temperature].fillna(0, inplace=True)
        df[cn.brand].fillna('', inplace=True)
        df[cn.step_description].fillna('', inplace=True)
        df[cn.usda_name].fillna('', inplace=True)
        df[cn.ingredient].fillna('', inplace=True)
        df[cn.unit].fillna('', inplace=True)
        df[cn.manufacturer].fillna('', inplace=True)
        df = self.reorder_columns(df)
        #print("After cleaning data {}".format(df))
        return df

    def nan_to_zeros(self, nan_number):
        """ First reindex, then set to 0 every NaN"""
        return int(money_str.replace(math.nan, 0))

    def money_to_float(money_str):
        """ Example usage for change_values()"""
        return float(money_str.replace("$", "").replace(",", ""))

    def change_values(self, df):
        for name in df.columns:
            df[name].apply(nan_to_zeros)


#CALCULATION

    def is_bread(self, df):
        """ Very smart """
        ingredients = self.ingredient_names(df)
        return True

    def set_bakers_percents_orig(self, df):
        if not self.is_bread(df):
            return df

        for ingredient in self.ingredient_names(df):
            bakers_percents = self.bakers_percent(df, ingredient=ingredient)
            bp = int(bakers_percents)
            self.set_at(df, cn.BP, ingredient, bp)
        return df


    def set_bakers_percents(self, df):
        df1 = df #df.reset_index()
        for index, row in df1.iterrows():
            ingredient = row[cn.ingredient]

            if self.cell_valid(ingredient, celltype=str):
                bakers_percents = self.bakers_percent(df, ingredient)
                bp = int(bakers_percents)
                df1.loc[index, cn.BP] = bp
                # this sets all column
                #df.loc[df.ingredient != "", 'BP'] = bp
        print('After setting BP-s: {}'.format(df1))
        return df1

    def cell_valid(self, ingredient, celltype=str):
        return isinstance(ingredient, celltype)

    def bakers_percent(self, df, ingredient):
        """
        TODO: smart function for flours, or else?
        Bakers percent per ingredient
        Bakers percent is the percentage of
        the specific igredient against the
        total weight of flours.
        Flours weight sums to 100 percent

        :param total_weight:
        :param this_weight:
        :return: int
        """

        if not self.cell_valid(ingredient, celltype=str):
            return 0

        flours_weight = self.flours_ingredients_weight(df)
        #print('Flours weight {}'.format(flours_weight))
        weight = self.ingredient_weight(df=df, ingredient=ingredient)
        self._logger.info('Weight of: {} is: {}'.format(ingredient, weight))

        if flours_weight == 0:
            raise Exception("Could not find flours!")
        baker_percent = int(weight * 100 / flours_weight)
        print('{} weight: {}, hydration: '
                  '{}, BP: {}, all flours weight {}'.format(
                                     ingredient,
                                     weight,
                                     self._hydration,
                                     baker_percent,
                                     flours_weight))

        return baker_percent

    def weight_from_bakers_percent(self, df):
        flours = self.get_flours_weight(df)
        for ing in self.ingredient_names(df):
            #Ingredient Percentage=Ingredient Weight/Total Flour x 100%
            self.set_ingredient_percentage(df)
        return df

    def ingredient_weight(self, ingredient, df):
        dfs = df.groupby(cn.ingredient).sum()
        weight = self.get_at(dfs, ingredient, cn.weight)
        return weight

    def get_weight(self, df, ingredient, index):
        """ not used"""

        weight = df.loc[ingredient, cn.weight]
        return weight


    def weight_from_percent(percent, total_weight):
        """
        Calculate weight from baker's percent

        :param percent:
        :param total_weight:
        :return:
        """
        return total_weight * percent / 100

    def wet_weight(self, df):
        """
        Weight in grams
        of wet ingredients
        A somewhat intelligent helper
        :return:
        """
        wets = self._get_matching_records(df, wet)
        wet_wright = sum(wets.amount.values)
        self._logger.info('Wet ingredients weight: {} {}'.format(wet_wright, unit.gram))
        #print('In wet_weight, dataframe is: {}'.format(df))
        return wet_wright

    def total_weight(self, df):
        """
        Sum of all rows from column "amount"
        :return:
        """
        total = df[cn.weight].sum()
        self._logger.info('Total ingredients weight in this recipe is {}'.format(total))
        return total


    def flours_ingredients_weight(self, df):
        """ Flours weight in baked recipe """
        flour = self._get_matching_records(df, flours)
        #print('Flour ingredients found: {}'.format(flour))
        #print('Flour names found: '.format(flour.ingredient))
        if flour.empty:
            raise Exception("Flour not found for bread product, something is wrong!")
        flours_weight = sum(flour.amount.values)
        self._logger.info('Flours weight is '
                          '{} {}'.format(flours_weight, unit.gram))
        return flours_weight


    def starter_weights(self, df, hydration=100):
        """
        Assume starter is 100% hydrated,
        so dry/wet is 50/50, for now.
        :param hydration:
        :return:
        """
        new_df = self._get_matching_records(df, ['starter'])
        weight = sum(new_df.amount.values)
        return weight/2, weight/2

    def hydration(self, df):
        """
        Calculate hydration percent
        from recipe ingredients
        :param ingredients:
        :return: percent hydration
        """
        water_weight = self.wet_weight(df)
        starter_wet, starter_dry = self.starter_weights(df)
        flour_weight = self.flours_ingredients_weight(df)
        water_weight = water_weight + starter_wet
        flour_weight = flour_weight + starter_dry

        hydration = water_weight * 100 / flour_weight
        #print('Hydration percent: {}, dataframe {}'.format(hydration, df))
        return hydration


#HELPERS
    def _get_matching_records(self, df, ingredients):
        """
        Common call
        :param ingredients:
        :return: dataframe object
        """

        selected = df.loc[df[cn.ingredient].isin(ingredients)]
        return selected

    def set_matching_records(self, df, row, col, values):
        pass


#ANALYSIS

    def bread_type(self):
        """
        Analyze, possiblitites are chabatta type,
        country, levain, etc
        This should be a smart function
        Should I create a classification
        algo model here?
        :return:
        """

        return 'white'

    def analyze_hydration(self, df):
        """
        print hydration, BP
        :return:
        """
        flours = self.flours_ingredients_weight(df)
        waters = self.wet_weight(df)
        hydra = self.hydration(df)
        print('Your Total flours: {}, your '
              'total waters: {}, your '
              'hydration: {}'.format(flours, waters, hydra))
        if hydra <= Hydration.low_hydration:
            print('This is a very dry dough')
        elif hydra > Hydration.low_hydration and hydra <= Hydration.common_hydration:
            print('This is somewhat dry dough')
        elif  hydra > Hydration.common_hydration and hydra <= Hydration.high_hydration:
            print('Your dough is quite well hydrated')
        elif hydra > Hydration.high_hydration and hydra <= Hydration.very_high_hydration:
            print('Your dough is rather wet, watch out when shaping!')
        else:
            print('This hydration is too much, make sure you know what you are doing!')


# RECALCULATION

    def change_hydration_old(self, new_hydration_percent, df):
        """
        Recalculate recipe with changed hydration
        :param percent:
        :return:
        """
        #old_percent = old_weight
        #new_percent = new_weight
        #new_weight = new_percent * old_weight / old_percent
        #X=new_h * old_weight/new_h
        #new_recipe = self.recipe.set_index('ingredient')

        current_wet_weight = self.wet_weight(df)
        current_whole_weight = self.total_weight(df)
        new_weight = new_hydration_percent * current_wet_weight / self._hydration
        # Set new weight in recipe
        self._logger.info(current_wet_weight, new_weight)
        df.loc['water', 'amount'] = new_weight
        self._hydration = new_hydration_percent

        return new_weight

    def change_hydration(self, new_hydration_percent, df):
        """
        Recalculate recipe with changed hydration
        :param percent:
        :return:
        """
        #old_percent = old_weight
        #new_percent = new_weight
        #new_weight = new_percent * old_weight / old_percent
        #X=new_h * old_weight/new_h
        #new_recipe = self.recipe.set_index('ingredient')

        original_wet_weight = self.wet_weight(df)
        original_total_weight = self.total_weight(df)
        hydration = self.hydration(df)
        new_wet_weight = new_hydration_percent * original_wet_weight / hydration
        # Set new weight in recipe
        self._logger.info(original_wet_weight, new_wet_weight)
        df.loc['water', 'amount'] = new_wet_weight
        self._hydration = new_hydration_percent

        return df

    def analyze_flours(self, df):
        """
        Find the list of
        flours used in recipe,
        try to figure out type
        of bread. This is
        a subjective functionality
        that can be improved in future
        :return:
        """

        recipe_flours = self._get_matching_records(df, flours)
        self._logger.info('Analyzing flours...')
        self._logger.info("Flours: {}".format(recipe_flours))

    @classmethod
    def yeast_to_starter_in_recipe(cls, df):
        """
        Calculates the recipe with
        100% hydration starter
        :param df:
        :return:
        """
        yeast = 0
        starter = 0

        return NotImplemented

    @classmethod
    def yeast_to_starter_conversion(cls, yeast=0, starter=0):
        """ General formula between converson of yeast and starter """

        return yeast, starter

    def analyze_cooking_conditions(self, df):
        """
        :return:
        """
        return NotImplemented

    def bake_time(self):
        if self.bread_type == 'tartine_master':
            return {'covered': 20, 'covered': 10, 'uncovered': 20}


    def autolyze_time(self, dough_info):
        """
        After analyzing recipe
        ingredients, this functinality
        can suggest a time
        for autolyze, depending
        on the informtion it gets.
        In addition to time, it should return
        explanation for his advice
        :return : json
        """
        tm = 60
        return tm

    def ideal_resting_temperature(self, water, flour, starter, scale='C'):
        """
        Ideal temperature for resting is 72
        since flours and starter temps are usually
        not controllable, the water should take over
        the lead
        :param scale:
        :return:
        """
        ideal_temp = 72
        water = 72 - flour - starter
        if scale == 'C':
            return 72


    def water_temp(flour_temp, room_temp, scale='F'):
        form = int(flour_temp) + int(room_temp) + 100
        return form

    def scale_recipe(self, df, times):
        """
        Scale all the ingredients,
        make another version,
        save to excel worksheet
        :param version:
        :return:
        """
        ingredients = self.ingredient_names(df)
        print(ingredients)
        for ingredient in ingredients:
            print(ingredient)
            if not ingredient:
                continue
            current_amount = self.ingredient_weight(ingredient=ingredient, df=df)
            self.set_at(df, cn.weight, ingredient, current_amount * times)
        self.versions.append(df)

    # DETECT IF BREAD
    #TODO this should be part of AI
    def _is_bread(self, df):
        """
        :param df:
        :return: True if bread
        """
        ingredients = self.ingredient_names(df)

        return True

    def convert_yeast_to_starter(self, df):
        """ Works for breads only"""
        if not self.is_bread(df):
            raise Exception("Cannot correctly calculate"
                            " yeast to starter convertion of "
                            "multi-ingredient recipe")
        yeast = self.get_yeast(df)
        if not yeast:
            raise Exception('This recipe does not contain yeast')
        water = self.get_waters(df)
        flour = self.get_flour(df)
        extras = self.get_others(df)
        if extras:
            raise Exception("Cannot correctly calculate"
                            " yeast to starter convertion of "
                            "multi-ingredient recipe "
                            "with extras {}".format(extras))
        total = water + flour
        starter = total / 6
        starter_flour = starter / 2
        starter_water = starter / 2
        new_flour = flour - starter_flour
        new_water = water - starter_water





def parse_options():
    parser = argparse.ArgumentParser(description='Calculate recipe')
    parser.add_argument('-w', "--workbook",  metavar='filepath', type=str,
                        help='file path')
    parser.add_argument('--sheet',  metavar='sheet', type=str,
                        help='sheet name')
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
    #bread.scale_recipe(bread.recipe, times=2)
    #print('Scaled recipe:')
    #print(bread.reindexed_recipe)
    bread.to_xl()




if __name__ == "__main__":
    main()    
