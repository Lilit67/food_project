from nltk import word_tokenize

class YeastToSourdough:
    def __init__(self):
        pass


    @classmethod
    def yeast_to_sourdough(df):

        ingredients = df['ingredient']
        if not ingredients:
            raise Exception('Dataframe need to have ingredients column')

        if not find_ingredient(df, 'yeast'):
            raise Exception('The recipe has no yeast as ingredient, cannot convert to sourdough')

        flours = []



    def find_ingredient(self, i_list, word):
        for ing in i_list:
            toks = word_tokenize(ing)
            if word in toks:
                return ing
        return None
