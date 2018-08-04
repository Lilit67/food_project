import matplotlib.pyplot as plt
#%matplotlib inline


def plot(df, col):
    sns.set()
    sns.pairplot(tips, hue='day');