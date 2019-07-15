from nltk import word_tokenize
import logging
import copy


from base_ingredients import Ingredients
from recipe_ingredient import RecipeIngredient

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
