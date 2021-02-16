#carregar um arquivo do disco rígido para a memória
#função: parâmetros de entrada -> um resultado

import pandas as pd
from numpy import int64

#data = pd.read_csv('datasets/kc_house_data.csv')

# print(data.head())
#
# #mostrar na tela os tipos de variáveis de cada coluna
# #print(data.dtypes) #por default o pandas ler todas as datas como object
#
# #função que converte de object (string) -> data
# data['date'] = pd.to_datetime( data['date'] )
#
#
# #mostrar na tela os tipos de variáveis de cada coluna
# print(data.dtypes)
# print(data.head())

# =======================================================
# Como converter os tipos de variáveis:
# =======================================================
# #inteiro -> float
# data['bedrooms'] = data['bedrooms'].astype( float )
# print(data.dtypes)
# print(data[['id', 'bedrooms']].head(3))
#
# #float -> inteiro
# #se deixar só 'int' é int32, converteu-se para int64 p/ ficar padrão; p/ isso foi importada a lib numpy.
# data['bedrooms'] = data['bedrooms'].astype( int64 )
#
# #inteiro -> string
# data['bedrooms'] = data['bedrooms'].astype( str )
#
# #string -> inteiro
# data['bedrooms'] = data['bedrooms'].astype( int64 )
#
# #string -> data
# data['date'] = pd.to_datetime(data['date'])
#ctrol + barra invertida = comentar mais uma linha


# # =======================================================
# # Criando novas variáveis
# # =======================================================
# data = pd.read_csv('datasets/kc_house_data.csv')
#
# data['nova_coluna'] = 'conteúdo da nova coluna'
# print( data[['id', 'date', 'nova_coluna']].head() )
#
# data['data_abertura_comunidade'] = pd.to_datetime('2020-02-28') #converter na criação
#
# # =======================================================
# # Deletar variáveis
# # =======================================================
# cols =  ['nova_coluna', 'data_abertura_comunidade']
# data = data.drop( cols, axis=1) #axis - é definir o sentido
# print( data.columns )


# =======================================================
# Seleção dos dados
# =======================================================
# -------------------------------------------------------
# Forma 01: direto pelo nome das colunas
# -------------------------------------------------------
#data = pd.read_csv('datasets/kc_house_data.csv')
#col = ['price', 'id', 'date']
#print( data[col])
#print( data[['price', 'id', 'date']])

# -------------------------------------------------------
# Forma 02: pelos índices das linhas e colunas
# -------------------------------------------------------
#iloc é o q seleciona as linhas e colunas apartir do índice: selecione pelo i(ndex)
#dados[linhas, colunas]
#print( data.iloc[0:10, :] )

# -------------------------------------------------------
# Forma 03: pelos índices das linhas e nomes das colunas
# -------------------------------------------------------
#loc é o q seleciona as linhas e colunas apartir do nome: selecione nome
# print( data.loc[0:10, 'price'] )
# print( data.loc[ 0:10, ['price', 'id', 'date'] ] )

# -------------------------------------------------------
# Forma 04: índice booleanos
# -------------------------------------------------------
#o número de True ou False tem que ser o mesmo número de colunas
# cols = [True, False, False, False, False, False,
#         True, False, False, False, False, False,
#         True, False, False, False, False, False, False, False, False]
# print( data.loc[ 0:10, cols ] )
# =======================================================


# =======================================================
# Respondendo às perguntas de negócio
# =======================================================
data = pd.read_csv('../datasets/kc_house_data.csv')

#-------------------------------------------------------
#1. Qual a data do imóvel mais antigo no portfólio?
# data['date'] = pd.to_datetime( data['date'] )
# print( data.sort_values( 'date', ascending=True))
#--------------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------------
#2. Quantos imóveis possuem o número máximo de andares (3.5)?
#print( data['floors'].unique()) #informa em um vetor todos os valores únicos da coluna

#print( data['floors'] == 3.5 ) #retorna true or false

# # print( data[data['floors'] == 3.5]) #retorna as colunas de data que obedecem à condição 'data['floors'] == 3.5'
# condicao = data['floors'] == 3.5
# print( data[condicao][['floors', 'id']] ) #pegar somente as colunas floors e id que obdecem a dada condição
# print( data[data['floors'] == 3.5][['floors', 'id']].shape )

#resposta da 2.
#print( data[ data['floors'] == 3.5 ].shape )
#--------------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------------
#3. Criar uma classificação para os imóveis, separando-os em baixo e alto padrã o de acordo com o preço
#data['level'] = 'standard' #nova coluna chamada level criada, e nela colocada o valor 'standard'
# print(data.columns)
# print(data.head())

# seleciona a coluna price, dps retorna os booleanos de acordo com a condição passada
#print(data['price'] > 540000 )

# seleciona a coluna price, dps retorna as linhas que obedecem a condição
#print(data.loc[ data['price'] > 540000 ])

#mostra somente a(s) coluna(s) seleciona, 'level', das linhas que obedecem à condição
#print(data.loc[ data['price'] > 540000, 'level' ])

#resposta da 3.
#substituir o campo das linnhas da coluna ('level') que obedecem a condição (data['price'] > 540000) por 'high_level'
# data.loc[ data['price'] > 540000, 'level' ] = 'high_level'
# print( data.head() )

# data.loc[ data['price'] < 540000, 'level' ] = 'low_level'
# print( data.head() )
#--------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------
#4. Fazer um relatório ordenado pelo preço e contendo algumas informações específicas
#report = data[ ['id', 'date', 'price', 'bedrooms', 'sqft_lot', 'level'] ] #ou ->
# col_selecionas = ['id', 'date', 'price', 'bedrooms', 'sqft_lot', 'level'] #sqft = m2 em pés
# report = data[col_selecionas]
# print(report)

# #ordenar pela coluna price e com o sentido ascending do maior para o menor (false)
# report = data[ ['id', 'date', 'price', 'bedrooms', 'sqft_lot', 'level'] ].sort_values('price', ascending=False)
# print(report.head())
#
# #salvando o dataframe num arquivo .csv
# ## não pode esquecer do parâmetro index=false, pq se ñ será salvo os index originais, o que baguncará a lista resultado; assim vai reconfigurar o index antes de salvar
# report.to_csv( 'datasets/report_aula02.csv', index=False)
#--------------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------------
# 5. Criar um mapa indicando onde as casas estão localizadas geograficamente

# Plotly - biblioteca que armazena uma função que desenha mapa
# Scatter MapBox - função que desenha um mapa

data_mapa = data[['id', 'lat', 'long', 'price']]
print(data_mapa)

# scatter_mapbox(data_mapa, lat= , lon= , hover_name='',
#                hover_data='',
#                color_discrete_sequence=['fuchsia'],
#                zoom=3,
#                height=300)

import plotly.express as px
mapa = px.scatter_mapbox(data_mapa, lat='lat', lon='long',
               hover_name='id',
               hover_data=['price'], #passe dentro de uma lista p/ ñ dar erro
               color_discrete_sequence=['fuchsia'],
               zoom=3,
               height=300)

#defino que o mapa plotado tem um estilo urbano (como o do google maps )
mapa.update_layout( mapbox_style='open-street-map' )

mapa.update_layout( height=600, margin={'r':0, 't':0, 'l':0, 'b':0} )

#por fim, para visualizar o mapa usa-se a função show
mapa.show()
#como o primeiro valor é uma número muito alto, será mostrado de longe

#salvar em html
mapa.write_html( 'datasets/mapa_house_rocket.html' )