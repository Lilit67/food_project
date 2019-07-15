""" GIven the data, convert to internal represenation format of recipe """
from yeast_to_sourdough import RecipeIngredient, Ingredients
from nltk.tokenize import sent_tokenize, word_tokenize

class InternalCanonizer:

    def __init__(self, data):
        self.raw_data = data
        self.ingredients = self.get_ingredients()



    def get_ingredients(self):
        if isinstance(self.raw_data, list):
            for i in self.raw_data:
                tokens = word_tokenize(i)
                print(tokens)

