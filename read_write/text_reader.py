import os
import argparse
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
        print(os.path.splitext(self.filepath))
        if not os.path.splitext(self.filepath)[1] == '.txt':
            raise Exception("File should be plain text")
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

def categorize_recipe(data):

    """
    All should be percents to be a percent recipe
    :param lines:
    :return:
    """
    percent_lines = []
    for line in data:

        tipo = analyze_line(line)

def analyze_line(line):
    tokens = tokenize_line(line)
    percent_lines = []
    print(tokens)
    if '%' in tokens:
        percent_lines.append(tokens)


def tokenize_line(line):
    tokens = word_tokenize(line)
    return tokens

def line_features(word):
    """
    '10% Arrowhead Mills Wholemeal Wheat\n'
    :param word:
    :return:
    """
    tokens = word_tokenize(word)
    print(tokens)
    if len(tokens) >= 2:
        return {'last_letter': tokens[1]}
    return ''


def parse_options():
    parser = argparse.ArgumentParser(description='Calculate recipe')
    parser.add_argument('-f', "--filepath",
                        metavar='filepath',
                        type=str,
                        help='file path',
                        required=True)

    args = parser.parse_args()
    return args

def main():
    args = parse_options()
    f = args.filepath #'./recipes/baguettes/tartine_baguette3.txt'
    reader = TextReader(f)
    data = reader.read()
    categorize_recipe(data)




if __name__ == '__main__':
    main()