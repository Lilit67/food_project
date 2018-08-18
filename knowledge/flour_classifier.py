import sklearn
from sklearn import tree
from nutrient.ingredients import flours, condiments, wet

floursold = ['wheat flour', 'rye flour', 'rye', 'wheat',
       'oat flour', 'oats', 'flour',
       'all purpose flour, white',
       'white flour', 'whole wheat flour',
       'white wheat flour', 'whole rye flour']

'''

features = ['name', 'type', 'label']
flour = 1
condiment = 2
wet = 3

food_features = []
food_labels = []
for f in flours:
    new_feature = [f]
    food_features.append(new_feature)
    food_labels.append(flour)

for c in condiments:
    new_feature = [c]
    food_features.append(new_feature)
    food_labels.append(condiment)

newt = 'white wheat flour (bread flour)'
clf = tree.DecisionTreeClassifier()
cls = clf.fit(food_features, food_labels)

print(clf.predict([[newt]]))

fruit_features = [[130, 0],[140, 0],[170, 1],[180, 1]]
fruit_labels = [1,1,0,0]

clf = tree.DecisionTreeClassifier()
cls = clf.fit(fruit_features, fruit_labels)

print(clf.predict([[130, 1]]))

if __name__ == '__main1__':
    try:
        while false:
            print('please input ingredient')
            input = ''

    except KeyboardInterrupt:
        exit(0)
'''

from sklearn.datasets import fetch_20newsgroups
twenty_train = fetch_20newsgroups(subset='train', shuffle=True)

twenty_train.target_names #prints all the categories
print("\n".join(twenty_train.data[0].split("\n")[:3])) #prints first line of the first data file