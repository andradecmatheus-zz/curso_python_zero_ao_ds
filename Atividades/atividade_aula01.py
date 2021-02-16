import pandas as pd

data = pd.read_csv('../datasets/kc_house_data.csv')

#1. Quantas casas estão disponíveis para compra?
#2. Quantos atributos as casas possuem?
#print( data.shape )

#3. Quais são os atributos das casas?
#print( data.columns)

#4. Qual a casa mais cara ( casa com o maior valor de venda )?
#print( data[['id', 'price']].sort_values('price', ascending=False) )

#5. Qual a casa com o maior número de quartos?
#print( data[['id', 'bedrooms']].sort_values('bedrooms', ascending=False) )

#6. Qual a soma total de quartos do conjunto de dados?
#print( data["bedrooms"].sum() )

#7. Quantas casas possuem 2 banheiros?
#print( (data["bedrooms"] == 2).sum() )

#8. Qual o preço médio de todas as casas no conjunto de dados?
#soma_custo_casas = data['price'].sum()
#soma_qtdd_casas = len(data.index) #row_count, column_count = df.shape
#print(round(soma_custo_casas / soma_qtdd_casas, 2) )

# #9. Qual o preço médio de casas com 2 banheiros?
#
# casas_2banheiros = data.loc[data["bedrooms"] == 2, 'price']
# #soma_custo_casas_2banheiros = soma_qtdd_casas_2banheiros['price'].sum()
# #casas_2banheiros.shape #qtdd = 2760
# #Resposta 9.
# print( round(casas_2banheiros.sum() /2760, 2)  )
# #Outra maneira de responder a 9.
#print( round( data.loc[ data["bedrooms"] == 2, 'price' ].sum() /2760, 2 )  )

#10. Qual o preço mínimo entre as casas com 3 quartos?
#print( data.loc[(data["bedrooms"] == 3, 'price')].min() )

#11. Quantas casas possuem mais de 300 metros quadrados na sala de estar?
#print( data.loc[data["sqft_living"] > 300, 'sqft_living']) #] #R: 21612+1

# #12. Quantas casas tem mais de 2 andares?
#print( data.loc[ data['floors'] > 2, 'floors']) #R: 782 casas

# 13. Quantas casas tem vista para o mar?
#print(data.loc[data['waterfront'] == True, 'waterfront']) #R: 163

# 14. Das casas com vista para o mar, quantas tem 3 quartos?
# vista_mar_3quartos = data.loc[(data.waterfront == 1) & (data.bedrooms == 3)]
# print( vista_mar_3quartos )

# 15. Das casas com mais de 300 metros quadrados de sala de estar, quantas tem mais de 2 banheiros?
#print(data.loc[ (data.sqft_living > 300) & (data.bathrooms > 2)]) R:11242