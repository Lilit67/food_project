import pandas as pd
import os

from analyzing.yeast_to_sourdough import Ingredients, RecipeIngredient

class CSVReader:
    def __init__(self, filepath):
        self.filepath = filepath


    def read(self):
        self.data = pd.read_csv(self.filepath)
        return self.data







def main():
    f = './recipes/baguettes/tartine_baguette.txt'
    data = []
    with open(f, 'r') as myfile:
        data = myfile.readlines()
    print(data)


if __name__ == '__main__':
    main()
