import pandas as pd

dataframe = pd.read_csv('./lstm/test.csv', usecols=[1], engine='python')
dataset = dataframe.values
print(type(dataset))
print(dataset)
# dataset = dataset.astype('float32')
# print(dataset)