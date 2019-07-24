import os

from nltk import word_tokenize
from nltk.corpus import stopwords

from analyzing.recipe_ingredient import RecipeIngredient
from analyzing.base_ingredients import Ingredients


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
        #self.set_data()
        return self.data


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


def line_features(word):
    """
    '10% Arrowhead Mills Wholemeal Wheat\n'
    :param word:
    :return:
    """
    tokens = word_tokenize(word)
    if len(tokens) >= 2:
        return {'last_letter': tokens[1]}
    return ''


def main():
    f = './recipes/baguettes/tartine_baguette3.txt'
    reader = TextReader(f)
    data = reader.read()
    print(data)
    for line in data:
        res = line_features(line)
        print('GOt {}'.format(res))



if __name__ == '__main__':
    main()