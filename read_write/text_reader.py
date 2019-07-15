import os
from analyzing.yeast_to_sourdough import Ingredients, RecipeIngredient
from nltk import word_tokenize
from nltk.corpus import stopwords

class TextReader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = None
        self.ingredients = Ingredients()

    def read(self):
        if not os.path.exists(self.filepath):
            raise Exception("File path does not exist {}".format(self.filepath))

        with open(self.filepath, 'r') as myfile:
            self.data = myfile.readlines()
        self.set_data()
        return self.ingredients


    def set_data(self):
        for d in self.data:
            print(word_tokenize(d))

    def set_dataold(self):
        for d in self.data:
            d = d.strip()
            d = d.rstrip('\n')
            if not d:
                continue
            d = d.split(',')
            if not len(d) == 3:
                print("Wrong line found in ingredients file, passing")
                continue
            else:
                ingredient = RecipeIngredient(d[0], d[1], d[2])
                self.ingredients.add(ingredient)
        print(self.ingredients)


