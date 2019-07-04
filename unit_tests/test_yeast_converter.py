import pytest
import logging
import os
import copy

from analyzing.yeast_to_sourdough import RecipeIngredient, Ingredients

@pytest.fixture(scope='module')
def recipe1():
    flour1 = RecipeIngredient(name='bread flour', amount=300, unit='gram')
    flour2 = RecipeIngredient(name='AP flour', amount=50, unit='gram')
    water = RecipeIngredient(name='water', amount=250, unit='gram')
    salt = RecipeIngredient(name='salt', amount=10, unit='gram')
    yeast = RecipeIngredient(name='yeast', amount=9, unit='gram')

    ings = Ingredients()

    ings.add(flour1)
    ings.add(flour2)
    ings.add(water)
    ings.add(salt)
    ings.add(yeast)
    return ings




class TestYeastConverter:
    def test_yeast_to_sourdough(self, recipe1):
        #golden1 = copy.copy(ings)
        print()



    def test_smth(self):
        pass

