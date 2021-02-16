import pandas as pd

data = pd.read_csv('../datasets/kc_house_data.csv')
print(data.columns)
# ===================================================================================================================
# 1. Crie uma nova coluna chamada: "house_age" ==
#  - Se o valor da coluna "date" for maior que 2015-01-01 => 'new_house
#  - Se o valor da coluna "date" for menor que 2015-01-01 => 'old_house
data['house_age'] = 'house'
data['date'] = pd.to_datetime(data['date'])
#print(data.dtypes)
data.loc[data['date'] > '2015-01-01', 'house_age'] = 'new_house'
data.loc[data['date'] < '2015-01-01', 'house_age'] = 'old_house'
print( data.sample(5) )
#print( data[['id', 'date']] .sort_values('date') )
# ===================================================================================================================

# ===================================================================================================================
#  2. Crie uma nova coluna chamada: "dormitory_type"
#  - Se o valor da coluna "bedrooms" for igual à 1 => 'studio'
#  - Se o valor da coluna "bedrooms" for igual à 2 => 'apartament'
data['dormitory_type']


# ===================================================================================================================








