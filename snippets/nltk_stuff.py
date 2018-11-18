import nltk
import random
from nutrient.ingredients import flours



def flour_features():
    words = nltk.words()
    return {'contains': 'flour'}


labeled_names = flours
random.shuffle(labeled_names)

labeled_names = ([(name, 'male') for name in
                  names.words('male.txt')] +
                 [(name, 'female') for name in
                  names.words('female.txt')])