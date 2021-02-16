import pandas as pd

data = pd.read_csv('../datasets/kc_house_data.csv')

#mostrar os cinco primeiros elementos
#print( data.head() )

#mostrar o número de colunas e linhas
#print( data.shape)

#mostrar o nome das colunas do banco de dados
#print( data.columns )

#mostrar o conj. de dados ordenados pela coluna price
#print( data.sort_values('price') )

#mostrar o conj. de dados ordenados pela coluna price do maior para o menor
#print( data[['id', 'price']].sort_values('price') )

#print( data[['id', 'price']].sort_values('price', ascending=False) )

