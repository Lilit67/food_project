from nltk import word_tokenize
import logging
import copy
from nutrient.ingredients import flours as FLOURS
from nutrient.ingredients import waters as WATERS
from nutrient.ingredients import yeast as YEAST
from nutrient.ingredients import starter as STARTER
from nutrient.ingredients import fat as FAT
from nutrient.ingredients import milk as MILK
from nutrient.ingredients import salt as SALT



def percentage(number=100, perc=100):
    """
    number = 100
    new_number = perc
    new = number * perc / 100
    :param perc:
    :return:
    """
    return number * perc / 100


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


class Ingredients:
    def __init__(self):
        self.ingredients = []
        self.waters = []
        self.flours = []
        self.salts = []
        self.yeast = []
        self.milks = []
        self.fats = []
        self.sugars = []
        self.starters = []
        self._logger = logging.getLogger('Ingredients')


    def __str__(self):
        ings = '\nName\t\tAmount\t\tUnit\n'
        for i in self.ingredients:
            ings += str(i)
        return ings

    def pretty_print(self):
        print(self)
        print('Hydration: {}'.format(self.hydration()))

    def __eq__(self, other):
        for i in self.ingredients:
            i1 = other.find_ingredient(i.name)
            if not i1:
                return False
        if not self.hydration() == other.hydration():
            return False
        return True

    @property
    def waters_weight(self):
        weight = 0
        for i in self.waters:
            weight += i.amount

        for i in self.starters:
            self._logger.info('Adding starter water {}'.format(i.amount))
            weight += i.amount / 2
        return weight

    @property
    def flours_weight(self, with_starters=True):
        """
        If starter weight to be considered, add half of starter weight
        assume starter is 100% hydration, for now
        :param with_starter:
        :return:
        """
        weight = 0
        for i in self.flours:
            weight += i.amount
        for i in self.starters:
            weight += i.amount / 2
        return weight

    def add(self, i):
        self.ingredients.append(i)

        if i.is_water():
            self.waters.append(i)
        elif i.is_flour():
            self.flours.append(i)
        elif i.is_salt():
            self.salts.append(i)
        elif i.is_milk():
            self.milks.append(i)
        elif i.is_fat():
            self.fats.append(i)
        elif i.is_yeast():
            self.yeast.append(i)
        elif i.is_starter():
            self.starters.append(i)
        self._logger.info('Added ingredient {}'.format(i.name))

    def ingredient_names(self):
        names = []
        for i in self.ingredients:
            names.append(i.name)
        return names

    def find_ingredient(self, name):
        for i in self.ingredients:
            if i.name == name:
                return i
        return None

    def _merge_ingredient(self, ing):
        """
        Find if ingredient with same name
        exists and merge the new one with existing
        :param ing:
        :return:
        """
        self._logger.debug('**Merging {}'.format(ing.name))
        existing = self.find_ingredient(ing.name)
        print('Found {}'.format(existing))
        if existing:
            merged = RecipeIngredient(existing.name,
                                      existing.amount+ing.amount,
                                      existing.unit)
            self.remove_ingredient(existing)
            self.remove_ingredient(ing)
            self.add(merged)



    def find_yeast(self):
        for i in self.ingredients:
            if i.is_yeast():
                return i
        return None

    def find_starter(self):
        for i in self.ingredients:
            if i.is_starter():
                return i
        return None

    def find_flours(self):
        """
        list of flour ingredients
        :return:
        """
        return self.flours

    def water_from_starter(self, hydration=100):
        water = 0
        for i in self.ingredients:
            if i.name in STARTER:
                water += self.weight([i]) / 2
                print('Water weight in starter {}'.format(water))
        return water

    def weight(self, ingredients, unit='grams'):
        """
        weight of ingredients
        :param ingredients:
        :param unit:
        :return:
        """
        weight = 0
        for i in ingredients:
            weight += i.amount
        return weight

    def make_percent_flour(self, percent):
        flours = self.find_flours()
        for f in flours:
            f.make_percent(percent)

    def make_percent_water(self, percent):
        for i in self.waters:
            i.make_percent(percent)

    def adjust_water_weight(self, weight):
        """
        change water in place
        :param weight:
        :return:
        """
        self._logger.info('Water weight before adjustment: {}, '
              'weight change: {}'.
              format(self.waters[0].amount, weight))
        self.waters[0].amount -= weight
        self._logger.info('Water weight after adjustment: {}'.
              format(self.waters[0].amount))

    def adjust_flour_weight(self, weight):
        self._logger.info('Flour weight '
                          'before adjustment {}, weight '
                          'to be substracted {}'.
                          format(self.flours[0].amount, weight))
        self.flours[0].amount -= weight
        self._logger.info(self.flours[0].amount)

    def starter_flour_to_dough(self, weight):
        """
        TODO:
        Smart way to
        define the type of flour
        that will be added to the main
        flour
        :param weight:
        :return:
        """
        newflour = RecipeIngredient('bread flour', weight, 'grams')
        self.flours.append(newflour)
        self.ingredients.append(newflour)
        return newflour

    def remove_ingredient(self, ingredient):
        """
        Remove an ingredient
        :return:
        """
        for ing in self.ingredients:
            if ing == ingredient:
                self.ingredients.remove(ing)
        i = ingredient
        if i.is_water():
            self.waters.remove(i)
        elif i.is_flour():
            self.flours.remove(i)
        elif i.is_salt():
            self.salts.remove(i)
        elif i.is_milk():
            self.milks.remove(i)
        elif i.is_fat():
            self.fats.remove(i)
        elif i.is_yeast():
            self.yeast.remove(i)
        elif i.is_starter():
            for x in self.starters:
                self.starters.remove(x)
        self._logger.info('Removed ingredient {}'.format(i.name))

    def hydration(self):

        wet_wait = self.waters_weight
        flours_weight = self.flours_weight
        if not flours_weight:
            raise Exception('Flours weight is 0!')
        hydration_percent = wet_wait * 100 / flours_weight
        return hydration_percent


class YeastToSourdough:

    @staticmethod
    def yeast_to_poolish(ingredients):
        """
        Use half the flour weight for the poolish
        the poolish will be 100 % hydration
        :return: ingredients
        """

        yeast = ingredients.find_yeast()

        if yeast:
            # half of flours weight
            poolish_flour = ingredients.flours_weight / 2
            poolish_water = poolish_flour
            poolish = RecipeIngredient('poolish', poolish_flour*2, 'grams')

            ingredients.make_percent_flour(50)

            ingredients.adjust_water_weight(poolish_water)

            ingredients.add(poolish)
            ingredients.remove_ingredient(yeast)


    @staticmethod
    def yeast_to_sourdough_regular(ingredients, percent=20):
        yeast = ingredients.find_yeast()

        if yeast:
            # by default it is 20%, but there is a problem adding flour back...s
            starter_flour = ingredients.make_percent_flour(percent)

            starter_water = starter_flour
            starter = RecipeIngredient('starter', starter_flour, 'grams')

            ingredients.adjust_water_weight(starter_water)

            ingredients.add(starter)
            ingredients.remove_ingredient(yeast)

    @staticmethod
    def sourdough_to_yeast(ingredients):
        leavener = ingredients.find_starter()
        starter_hydration = 100
        if leavener:

            starter_flour = leavener.amount / 2
            starter_water = leavener.amount / 2

            ingredients.adjust_water_weight(-starter_water)
            #ingredients.adjust_flour_weight(starter_flour)
            new_ingredient = ingredients.starter_flour_to_dough(starter_flour)
            #print('Before merge {}'.format(ingredients))
            ingredients._merge_ingredient(new_ingredient)
            #print('After merge {}'.format(ingredients))
            ingredients.remove_ingredient(leavener)
            new_yeast = RecipeIngredient('yeast', 9, 'grams')
            ingredients.add(new_yeast)


if __name__ == "__main__":
    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(format=FORMAT)

    flour1 = RecipeIngredient(name='bread flour', amount=300, unit='gram')
    flour2 = RecipeIngredient(name='AP flour', amount=50, unit='gram')
    flour3 = RecipeIngredient(name='00 tipo', amount=50, unit='gram')
    water = RecipeIngredient(name='water', amount=250, unit='gram')
    salt = RecipeIngredient(name='salt', amount=10, unit='gram')
    yeast = RecipeIngredient(name='yeast', amount=9, unit='gram')

    ings = Ingredients()

    ings.add(flour1)
    ings.add(flour2)
    ings.add(water)
    ings.add(salt)
    ings.add(yeast)
    ings.add(flour3)

    ings_copy = copy.copy(ings)

    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(format=FORMAT)

    print('Original recipe:')
    ings.pretty_print()

    YeastToSourdough.yeast_to_poolish(ings)
    print('Poolish to sourdough:')
    ings.pretty_print()

    YeastToSourdough.sourdough_to_yeast(ings)

    print('Sourdough to yeast;')
    ings.pretty_print()

    assert ings == ings_copy
    assert ings.flours_weight == ings_copy.flours_weight
    assert ings == ings_copy
