import pandas as pd
import os


class CSVReader:
    def __init__(self, filepath):
        self.filepath = filepath


    def read(self):
        self.data = pd.read_csv(self.filepath)
        return self.data

def main():
    f = './recipes/baguettes/tartine_baguette3.txt'
    reader = CSVReader(f)
    data = reader.read()
    print(dir(data))


if __name__ == '__main__':
    main()
