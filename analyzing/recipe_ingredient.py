import logging
import copy
from nutrient.ingredients import flours as FLOURS
from nutrient.ingredients import waters as WATERS
from nutrient.ingredients import yeast as YEAST
from nutrient.ingredients import starter as STARTER
from nutrient.ingredients import fat as FAT
from nutrient.ingredients import milk as MILK
from nutrient.ingredients import salt as SALT
from utilities.helpers import percentage


class RecipeIngredient(object):
    """ TODO: metaclass"""
    def __init__(self, name, amount, unit):
        self.name = name
        self.amount = amount
        self.unit = unit
        self._logger = logging.getLogger(self.__class__.__name__)

    def __str__(self):
        stringp = ''
        stringp += ' {} '.format(self.name) + '\t'
        stringp += ' {}'.format(self.amount) + '\t'
        stringp += ' {}'.format(self.unit) + '\n'
        return stringp

    def __eq__(self, other):
        if self.name != other.name:
            return False
        if self.amount != other.amount:
            return False
        if self.unit != other.unit:
            return False
        return True

    def make_percent(self, percent):
        self.amount = percentage(self.amount, percent)


    def isit(self, ingredient_type):
        if ingredient_type in FLOURS:
            return True
        elif ingredient_type in WATERS:
            return True
        return False

    def is_water(self):
        if self.name in WATERS:
            return True
        return False

    def is_flour(self):
        if self.name in FLOURS:
            return True
        return False

    def is_starter(self):
        if self.name in STARTER:
            return True
        return False

    def is_yeast(self):
        if self.name in YEAST:
            return True
        return False

    def is_salt(self):
        if self.name in SALT:
            return True
        return False

    def is_milk(self):
        if self.name in MILK:
            return True
        return False

    def is_fat(self):
        if self.name in FAT:
            return True
        return False
