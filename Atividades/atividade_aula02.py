import pandas as pd

data = pd.read_csv('datasets/kc_house_data.csv')
print(data.columns)
# ===================================================================================================================
# 1. Crie uma nova coluna chamada: "house_age" ==
#  - Se o valor da coluna "date" for maior que 2015-01-01 => 'new_house
#  - Se o valor da coluna "date" for menor que 2015-01-01 => 'old_house
## Resposta:
data['house_age'] = 'house'
data['date'] = pd.to_datetime(data['date'])
# #print(data.dtypes)
data.loc[data['date'] > '2015-01-01', 'house_age'] = 'new_house'
data.loc[data['date'] < '2015-01-01', 'house_age'] = 'old_house'
print( data.sample(5) )
#print( data[['id', 'date']] .sort_values('date') )
# ===================================================================================================================

# ===================================================================================================================
#  2. Crie uma nova coluna chamada: "dormitory_type"
#  - Se o valor da coluna "bedrooms" for igual à 1 => 'studio'
#  - Se o valor da coluna "bedrooms" for igual à 2 => 'apartament'
#  - Se o valor da coluna "bedrooms" for maior q 2 => 'house'
## Resposta:
data['dormitory_type'] = 'undefined'
data.loc[ data['bedrooms'] == 1, 'dormitory_type'] = 'studio'
data.loc[ data['bedrooms'] == 2, 'dormitory_type'] = 'apartament'
data.loc[ data['bedrooms'] > 2, 'dormitory_type'] = 'house'
# print( data.sample(5) )
# dormitory_type_undefined = data.loc[data['dormitory_type'] == 'undefined']
# print(dormitory_type_undefined[['id', 'bedrooms', 'dormitory_type']])
# ===================================================================================================================

# ===================================================================================================================
#  3. Crie uma nova coluna chamada: "condition_type"
#  - Se o valor da coluna "condition" for menor ou igual à 2 => 'bad'
#  - Se o valor da coluna "condition" for igual à 3 ou 4 => 'regular'
#  - Se o valor da coluna "condition" for igual à 5 => 'good'
## Resposta:
data['condition_type'] = 'undefined'
data.loc[data['condition'] <= 2, 'condition_type'] = 'bad'
data.loc[(data['condition'] == 3) | (data['condition'] == 4), 'condition_type'] = 'regular'
data.loc[data['condition'] == 5, 'condition_type'] = 'good'
#print( data[['id', 'condition', 'condition_type']] )
# ===================================================================================================================

# ===================================================================================================================
# 4. Modifique o TIPO da coluna "condition" para STRING
# print(data.dtypes) #condition is int64
data['condition'] = data['condition'].astype(str)
# print('\n\ncondition column parsed from int to str:\n', data.dtypes)
# ===================================================================================================================

# ===================================================================================================================
# 5. Delete as colunas "sqft_living15" e "sqft_lot15"
cols = ['sqft_living15', 'sqft_lot15']
data = data.drop(cols, axis=1)
# print(data.columns)
# ===================================================================================================================

# ===================================================================================================================
# 6. Modifique o TIPO da coluna "yr_built" para DATE (ano da construção)
# print(data.dtypes)
data['yr_built'] = pd.to_datetime(data['yr_built'], format= '%Y', errors= 'coerce')
# print('\n\nyr_built column parsed from int to str:\n', data.dtypes)
# ===================================================================================================================

# ===================================================================================================================
#  7. Modifique o TIPO da coluna "yr_renovated" para DATE (ano da reforma)
# ===================================================================================================================
# print(data.dtypes)
data['yr_renovated'] = pd.to_datetime(data['yr_renovated'], format= '%Y', errors= 'coerce')
# print('\n\nyr_renovated column parsed from int to str:\n', data.dtypes)
# ===================================================================================================================

# ===================================================================================================================
# 8. Qual a data mais antiga de construção de um imóvel?
# print(data.columns)
# data['date'] = pd.to_datetime(data['date'])
# print( data[['id','yr_built']].sort_values('yr_built', ascending=True) ) #R: 1900
# ===================================================================================================================

# ===================================================================================================================
# 9. Qual a data mais antiga de renovação de um imóvel?
# ===================================================================================================================
#print(data.yr_renovated.min()) #R: 1934-01-01
# ===================================================================================================================

# ===================================================================================================================
#  10. Quantos imóveis tem 2 andares?
# print(data.loc[ data['floors'] == 2 ]) #R:8241
# ===================================================================================================================

# ===================================================================================================================
# 11. Quantos imóveis estão com a condição igual à "regular"?
#print(data.loc[data['condition_type'] == 'regular']) #R:19710
# ===================================================================================================================

# ===================================================================================================================
# 12. Quantos imóveis estão com a condição igual a "bad" e possuem "vista para água"?
#print(data.loc[(data['condition_type'] == 'bad') & (data['waterfront'] == True)]) #R: 2
# ===================================================================================================================

# ===================================================================================================================
# 13. Quantos imóveis estão com a condição igual a "good" e são "new_house"?condition_type
#print(data.loc[(data['condition_type'] == 'good') & (data['house_age'] == 'new_house') ]) #R:423 or 1701 (if it was 2014)
# ===================================================================================================================

# ===================================================================================================================
# 14. Qual o valor do imóvel mais caro do tipo "studio"?
#print( data.loc[ (data['dormitory_type'] == 'studio')].price.max() ) #R:1247000.0
# ===================================================================================================================

# ===================================================================================================================
#  15. Quantos imóveis do tipo "apartament" foram reformados em 2015?
#print(data.loc[(data['dormitory_type'] == 'apartament') & (data['yr_renovated'] == '2015-01-01')]) #R: 0
# ===================================================================================================================

# ===================================================================================================================
# 16. Qual o maior número de quartos que um imóvel do tipo "house" possui?
# print( data.loc[(data.dormitory_type == 'house')].bedrooms.max() )
# ===================================================================================================================

# ===================================================================================================================
#  17. Quandos imóveis "new_house" foram reformados no ano de 2014?
# print( data.loc[(data['house_age'] == 'new_house') & (data['yr_renovated'] == '2014')] ) #R: 15 or 91 (if it was 2014)
# ===================================================================================================================

# ===================================================================================================================
# 18. Selecione as colunas: "id", "date", "price", "floors", "zipcode" pelo método: [0, 1, 2, 7, 16]
#  a Direto pelo nome das colunas
col = ['id', 'date', 'price', 'floors', 'zipcode']
# print(data[col])

#  b Pelos índices
#print(data.iloc[:, [0, 1, 2, 7, 16]])

#  c Pelos índices das linhas e o nome das colunas
#print(data.loc[:, col])

#  d Índices booleanos
#d. Method 1
# listaBool = []
# for column in data.columns.tolist():
#     if column in col:
#         listaBool.append(True)
#     else:
#         listaBool.append(False)
# print(data.loc[:, listaBool])

#d. Method 2
# cols = [True, True, True, False, False, False, False,
#         True, False, False, False, False, False, False, False,
#         False, True, False, False, False, False, False, False, False]
# print( data.loc[ 0:10, cols ] )
# ===================================================================================================================

# ===================================================================================================================
#  19. Salve um arquivo .csv com somente as colunas do item 10
#somente_colunas_item10 = data.iloc[10, :]
# somente_colunas_item10 = data.loc[[10]]
# somente_colunas_item10.to_csv('datasets/aula02_atividade_somente_colunas_item10.csv', index=True)
# ===================================================================================================================


# ===================================================================================================================
#  20. Modifique a cor dos pontos no mapa de "pink" para "verde-escuro"
# ===================================================================================================================
# data_mapa = data[['id', 'lat', 'long', 'price']]
# print(data_mapa)
#
# import plotly.express as px
# mapa = px.scatter_mapbox(data_mapa, lat='lat', lon='long',
#                hover_name='id',
#                hover_data=['price'], #passe dentro de uma lista p/ ñ dar erro
#                color_discrete_sequence=['darkgreen'],
#                zoom=8.5,
#                height=850)
#
# mapa.update_layout( mapbox_style='open-street-map' )
# mapa.update_layout( height=850, margin={'r':0, 't':0, 'l':0, 'b':0} )
# mapa.show()
# mapa.write_html( 'datasets/aula02_atividade_mapa.html' )
# ===================================================================================================================
