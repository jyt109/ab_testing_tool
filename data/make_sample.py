import pandas as pd


def make_sample(filename):
    """INPUT:
    - filename(STR) [The filename to be read and sampled]

    OUTPUT:
    - Output to csv

    Sample the first 5000 rows
    """
    data = pd.read_csv(filename)
    data.sort('ts', inplace=True)
    data = data.iloc[:5000]
    data.to_csv('sample.csv')

def make_whole(filename):
    pass

if __name__ == '__main__':
    make_sample('experiment.csv')
