import streamlit as st
import pandas as pd
import folium
import plotly.express as px

from numpy import int64
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

pd.set_option('display.float_format', lambda x: '%.2f' % x)

st.set_page_config(layout='wide')

st.markdown(
    """<style>
        .dataframe {text-align: center !important}
    </style>
    """, unsafe_allow_html=True)


@st.cache(allow_output_mutation=True)
def get_data(path):
    data = pd.read_csv(path)
    return data


# 1. Quais são os imóveis que a House Rocket deveria comprar e por qual preço?
def buy_houses(df):
    # st.write(df.style.format("{:.2}"))
    st.title(
        '1. Quais são os imóveis que a House Rocket deveria comprar e por qual preço?')  # Houses that should be bought Options

    c1, c2 = st.beta_columns((1, 1))

    c1.header('Tabela')
    price_median = df[['price', 'zipcode']].groupby('zipcode').median().reset_index()
    df2 = pd.merge(df, price_median, on='zipcode', how='inner')
    df2.rename(columns={"price_x": "price", "price_y": "price_median"}, inplace=True)

    house_buy = df2[['id', 'zipcode', 'price', 'price_median', 'condition', 'lat', 'long']].copy()

    # Calculating if it should be bought, so its percentual and price difference from the median
    house_buy['status'] = 'dont buy'
    house_buy.loc[(house_buy['price'] < house_buy['price_median']) & (house_buy['condition'] == 5),
                  'status'] = 'buy'
    house_buy['diff_perc'] = (house_buy['price'] * 100) / house_buy['price_median'] - 100
    house_buy['diff_price'] = house_buy['price_median'] - house_buy['price']

    st.sidebar.title(
        '1. Quais são os imóveis que a House Rocket deveria comprar e por qual preço?')  # Houses that should be bought Options

    # Filters
    min_ = int(1)
    max_ = int(house_buy.loc[house_buy['status'] == 'buy'].shape[0])

    f_order_table = st.sidebar.selectbox(
        'Ordenar por',  # 'Order by'
        ['diff_perc', 'diff_price']
    )
    f_zipcode = st.sidebar.multiselect(
        'Escolher por Zipcode',  # 'Enter zipcode'
        df['zipcode'].unique()
    )
    f_diff_price = st.sidebar.slider('Quantidade de casas',  # 'How many houses'
                                     1,
                                     1,  # max
                                     max_
                                     )

    if (f_order_table == 'diff_perc'):
        result = house_buy.loc[house_buy['status'] == 'buy'].sort_values('diff_perc', ascending=True)
        if (f_zipcode != []):
            result = result.loc[result['zipcode'].isin(f_zipcode)]

    elif (f_order_table == 'diff_price'):
        result = house_buy.loc[house_buy['status'] == 'buy'].sort_values('diff_price', ascending=False)
        if (f_zipcode != []):
            result = result.loc[result['zipcode'].isin(f_zipcode)]
    else:
        result = house_buy.loc[house_buy['status'] == 'buy']

    result1 = result[['id', 'zipcode', 'price', 'price_median', 'condition', 'status', 'diff_perc', 'diff_price']]
    result1 = result1.head(f_diff_price)
    c1.dataframe(result1, height=525)

    c2.header('Mapa')

    density_map = folium.Map(location=[result['lat'].mean(),
                                       result['long'].mean()],
                             default_zoom_start=15)

    marker_cluster = MarkerCluster().add_to(density_map)  # adiciona pontos dentro do mapa

    for name, row in result.head(
            f_diff_price).iterrows():  # popup é uma função de card, com informações dentro escolhidas
        folium.Marker([row['lat'], row['long']],
                      popup=folium.Popup('<p><b>ID {0}</b></p>Zipcode {1}<br>Price {2}<br>Price median ${3}'
                                         '<br>Diff_perc {4:.2f}%<br>Diff_price ${5}'
                                         .format(row['id'], row['zipcode'],
                                                 row['price'], row['price_median'],
                                                 row['diff_perc'], row['diff_price']),
                                         max_width=700),

                      ).add_to(marker_cluster)

    with c2:
        folium_static(density_map)

    return None


# 2. Uma vez o imóvel comprado, qual o melhor momento para vendê-lo e por qual preço?
def sell_houses(df):
    st.title(
        '2. Uma vez o imóvel comprado, qual o melhor momento para vendê-lo e por qual preço?')  # Best moments to sell the houses
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    df['month'] = pd.to_datetime(df['date']).dt.strftime('%m')
    df['month'] = df['month'].astype(int64)

    df2 = df[['id', 'zipcode', 'price', 'month']].copy()

    # creating season columns
    # https://www.tripsavvy.com/the-weather-and-climate-in-seattle-4175384
    # Spring 3 4 5; summer 6 7 8; fall 9 10 11; Winter 12 1 2;

    # for i in range(len(df2)):
    #     if ((df2.loc[i, 'month'] >= 3) & (df2.loc[i, 'month'] <= 5)):
    #         df2.loc[i, 'season'] = 'Spring'
    #
    #     elif ((df2.loc[i, 'month'] >= 6) & (df2.loc[i, 'month'] <= 8)):
    #         df2.loc[i, 'season'] = 'Summer'
    #
    #     elif ((df2.loc[i, 'month'] >= 9) & (df2.loc[i, 'month'] <= 11)):
    #         df2.loc[i, 'season'] = 'Fall'
    #
    #     elif ((df2.loc[i, 'month'] <= 2) | (df2.loc[i, 'month'] == 12)):
    #         df2.loc[i, 'season'] = 'Winter'
    #     else:
    #         df2.loc[i, 'season'] = 'Not defined'
    # alternativa mais rápida (cuidado com a ordem)
    df2['season'] = 'Not defined'
    df2.loc[(df2['month'] <= 2) | (df2['month'] == 12), 'season'] = 'Winter'
    df2.loc[(df2['month'] >= 3) & (df2['month'] <= 5), 'season'] = 'Spring'
    df2.loc[(df2['month'] >= 6) & (df2['month'] <= 8), 'season'] = 'Summer'
    df2.loc[(df2['month'] >= 9) & (df2['month'] <= 11), 'season'] = 'Fall'

    season = df2[['price', 'zipcode', 'season']].groupby(['zipcode', 'season']).median().reset_index()
    df2 = pd.merge(df2, season, on=['zipcode', 'season'], how='inner')
    df2.rename(columns={"price_x": "price", "price_y": "price_median"}, inplace=True)

    df2 = df2[['id', 'zipcode', 'season', 'month', 'price_median', 'price']]

    # calculating the best houses to sell
    # for i in range(len(df2)):
    #     if ((df2.loc[i, 'price'] >= df2.loc[i, 'price_median'])):
    #         df2.loc[i, 'sale_price'] = ((df2.loc[i, 'price']) * (1.1))
    #         df2.loc[i, 'profit'] = ((df2.loc[i, 'sale_price']) - (df2.loc[i, 'price']))
    #         df2.loc[i, 'profit_perc'] = '30%'
    #
    #     elif ((df2.loc[i, 'price'] < df2.loc[i, 'price_median'])):
    #         df2.loc[i, 'sale_price'] = ((df2.loc[i, 'price']) * (1.3))
    #         df2.loc[i, 'profit'] = ((df2.loc[i, 'sale_price']) - (df2.loc[i, 'price']))
    #         df2.loc[i, 'profit_perc'] = '10%'

    # calculating the best houses to sell (alternativa mais rápida)
    df2.loc[(df2['price'] >= df2['price_median']), 'sale_price'] = df2['price'] * (1.1)
    df2.loc[(df2['price'] >= df2['price_median']), 'profit_perc'] = '30%'
    df2.loc[(df2['price'] < df2['price_median']), 'sale_price'] = df2['price'] * (1.3)
    df2.loc[(df2['price'] < df2['price_median']), 'profit_perc'] = '10%'
    df2['profit'] = df2['sale_price'] - df2['price']

    st.dataframe(df2)

    return None


# H1: imóveis que possuem vista para água, são 20% mais caros, na média.
def hypothesis1(df):
    st.title('')
    st.title('H1: Imóveis que possuem vista para água, são 20% mais caros, na média.')
    price_mean = df[['zipcode', 'price']].groupby('zipcode').mean().reset_index()

    df = pd.merge(df, price_mean, on='zipcode', how='inner')
    df.rename(columns={"price_x": "price", "price_y": "price_mean"}, inplace=True)

    df = df[['id', 'zipcode', 'price', 'price_mean', 'waterfront']].copy()

    # creating 20% column

    # alternativa mais lenta
    # for i in range(len(df)):
    #     if ((df.loc[i, 'waterfront'] == 1) & (df.loc[i, 'price'] >= (df.loc[i, 'price_mean'] * 1.2))):
    #         df.loc[i, '20perc_more_expensive'] = 'Yes'
    #     else:
    #         df.loc[i, '20perc_more_expensive'] = 'No'

    # alternativa mais rápida
    df['20perc_more_expensive'] = 'No'
    df.loc[(df['waterfront'] == 1) & (df['price'] >= (df['price_mean'] * 1.2)), '20perc_more_expensive'] = 'Yes'

    # df.head()
    # qtd_casas_waterfront = df.loc[(df['waterfront'] == 1)].count()
    # df.loc[(df['waterfront'] == 1)]

    qtd_casas_waterfront = df.loc[(df['waterfront'] == 1)].shape
    qtd_casas_waterfront_20 = df.loc[(df['waterfront'] == 1) & (df['20perc_more_expensive'] == 'Yes')].shape

    # showing the answer
    st.header('Imóveis que possuem vista para a água:')
    df.loc[(df['waterfront'] == 1)]
    result = str(
        'H1: Positivo. Existem {} casas com vista para a água. Dessas, {} casas têm o seu valor 20% maior do que a média.'
        .format(qtd_casas_waterfront[0], qtd_casas_waterfront_20[0]))
    # print(result)
    st.header(result)
    return result


# H2: Imóveis com data de construção menor que 1995, são 50% mais baratos, na média.
def hypothesis2(df):
    st.title('')
    st.title('H2: Imóveis com data de construção menor que 1995, são 50% mais baratos, na média.')
    price_mean = df[['zipcode', 'price']].groupby('zipcode').mean().reset_index()

    df = pd.merge(df, price_mean, on='zipcode', how='inner')
    df.rename(columns={"price_x": "price", "price_y": "price_mean"}, inplace=True)

    houses = df[['id', 'zipcode', 'price', 'price_mean', 'yr_built']].copy()

    qtd_casas_1995 = houses.loc[(houses['yr_built'] < 1995)]
    qtd_casas_1995['50%_mais_barata'] = 'No'
    qtd_casas_1995.loc[(qtd_casas_1995['yr_built'] < 1995) & (
                qtd_casas_1995['price'] < qtd_casas_1995['price_mean'] / 2), '50%_mais_barata'] = 'Yes'

    # showing the answer
    st.header('Casas construídas antes de 1995:')
    qtd_casas_1995
    result = str(
        'H2: Falso. Existem {} casas construídas antes de 1995. Dessas, {} casas têm o seu valor 50% menor do que a média.'
        .format(qtd_casas_1995.shape[0], qtd_casas_1995.loc[(qtd_casas_1995['50%_mais_barata'] == 'Yes')].shape[0]))
    st.header(result)

    return result


# H3: Imóveis sem porão, possuem área total (sqrt_lot), são 40% maiores do que os imóveis com porão.
def hypothesis3(df):
    st.title('')
    st.title('H3: Imóveis sem porão, possuem área total (sqrt_lot), são 40% maiores do que os imóveis com porão.')
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

    # houses without basement
    basement0 = df.loc[df['sqft_basement'] == 0]
    basement0 = basement0[['sqft_lot', 'zipcode']].groupby('zipcode').mean().reset_index()

    # houses with basement
    basement1 = df.loc[df['sqft_basement'] > 1]
    basement1 = basement1[['sqft_lot', 'zipcode']].groupby('zipcode').mean().reset_index()

    basement = pd.merge(basement0, basement1, on='zipcode', how='inner')
    basement.rename(columns={"sqft_lot_x": "Sem_porao_sqrt_lot", "sqft_lot_y": "Com_porao_sqrt_lot"}, inplace=True)

    tam = basement.shape[0]  # len(basement)

    for i in range(tam):
        if ((basement.loc[i, 'Sem_porao_sqrt_lot'] > basement.loc[i, 'Com_porao_sqrt_lot'] * 1.4)):
            basement.loc[i, 'Sem_porao_40%maior'] = 'Yes'
        else:
            basement.loc[i, 'Sem_porao_40%maior'] = 'No'

    result = basement.loc[basement['Sem_porao_40%maior'] == 'Yes']

    # showing the answer
    resultT = str('H#: Falso. No total são {} localidades(zipcode), somente em {} as casas sem porão apresentam a ' \
                  'média do porão maior que 40% em relação as casas com porão. Nas outras 68 localidades (zipcodes),' \
                  'os imóveis sem porão não são maiores em 40%.' \
                  .format(basement.shape[0], result.shape[0]))
    basement
    st.header(resultT)

    # data = df
    # data['porao'] = data['sqft_basement'].apply(lambda x: 'nao' if x == 0
    # else 'sim')
    #
    # h3 = data[['porao', 'sqft_lot', 'price']].groupby('porao').sum().reset_index()
    # fig3 = px.bar(h3, x='porao', y='sqft_lot', color='porao', labels={'price': 'Preço',
    #                                                                  'sqft_lot': 'Área Total'},
    #               template='simple_white')
    # fig3.update_layout(showlegend=False)
    # c3 = st.beta_columns(1)
    # folium_static(fig3)
    # #c3.plotly_chart(fig3, use_container_width=True)

    return result
    # r: Falso, em somente duas localidades (zipcode), de 70, as casas sem porão apresentam a média do porão > que 40% em relação as casas com porão, nas outras 68 localidades (zipcodes), os imóveis sem porão não são maiores em 40%+
    # Melhoria: e no geral, sem restringir as casas por localidades?


# H4: O crescimento do preço dos imóveis YoY (Year over Year) é de 10%
def hypothesis4(df):
    st.title('')
    st.title('H4: O crescimento do preço dos imóveis YoY (Year over Year) é de 10%.')
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    df['year'] = pd.to_datetime(df['date']).dt.strftime('%Y')

    price_median_year = df[['price', 'zipcode', 'year']].groupby(['zipcode', 'year']).median().reset_index()

    zipcodes = price_median_year['zipcode'].unique().tolist()
    result = pd.DataFrame(zipcodes, columns=['Zipcode'])
    count = 0

    # calculating if YOY == 10 %
    for i in range(1, len(price_median_year)):
        if ((price_median_year.loc[i - 1, 'zipcode'] == price_median_year.loc[i, 'zipcode'])):
            result.loc[count, '2014_median'] = price_median_year['price'].values[i - 1]
            result.loc[count, '2015_median'] = price_median_year['price'].values[i]

            if ((price_median_year.loc[i - 1, 'price'] * 1.1) < (price_median_year.loc[i, 'price'])):
                result.loc[count, 'YoY_10%'] = 'Yes'

            else:
                result.loc[count, 'YoY_10%'] = 'No'

            result.loc[count, 'percent_YoY'] = (
                    (price_median_year['price'].values[i] * 100) / price_median_year['price'].values[i - 1] - 100)
            count = count + 1

    result

    # showing the answer
    result = str('H4: Falso. O crescimento do preço dos imóveis YoY não é de 10%, ele é de {:0.2f}%. ' \
                 'Das {} localidades, somente {} apresentam uma média YoY do preço dos imóveis maior que 10%.'
                 .format(result['percent_YoY'].mean(), result.shape[0],
                         result.loc[(result['YoY_10%'] == 'Yes')].shape[0]))

    st.header(result)
    return result


# H5: Imóveis com 3 banheiros tem um crescimento de MoM (Month over Month) de 15%
def hypothesis5(df):
    st.title('')
    st.title('H5: Imóveis com 3 banheiros tem um crescimento de MoM (Month over Month) de 15%.')
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

    df['year'] = pd.to_datetime(df['date']).dt.strftime('%Y')
    df['month'] = pd.to_datetime(df['date']).dt.strftime('%m')

    bathrooms3 = df.loc[df['bathrooms'] == 3]

    bathroom_median = bathrooms3[['price', 'zipcode', 'year', 'month']].groupby(
        ['zipcode', 'year', 'month']).median().reset_index()

    # bathroom_median

    # months = bathroom_median['month'].tolist()
    result = bathroom_median[['zipcode', 'year', 'month', 'price']].copy()
    count = 0

    # result

    for i in range(1, len(bathroom_median)):
        if ((bathroom_median.loc[i - 1, 'zipcode'] == bathroom_median.loc[i, 'zipcode'])):
            if (bathroom_median.loc[i - 1, 'year'] == bathroom_median.loc[i, 'year']):
                result.loc[count, 'month_current'] = float(bathroom_median['month'].values[i - 1])
                result.loc[count, 'month_next'] = float(bathroom_median['month'].values[i])

                if ((int(bathroom_median.loc[i, 'month']) - float(bathroom_median.loc[i - 1, 'month']) == 1)):
                    result.loc[count, 'month_diff'] = result.loc[count, 'month_next'] - result.loc[
                        count, 'month_current']

                elif ((int(bathroom_median.loc[i, 'month']) - float(bathroom_median.loc[i - 1, 'month']) > 1)):
                    result.loc[count, 'month_diff'] = result.loc[count, 'month_next'] - result.loc[
                        count, 'month_current']

            else:
                result.loc[count, 'month_current'] = int(bathroom_median['month'].values[i - 1])
                result.loc[count, 'month_next'] = int(bathroom_median['month'].values[i])

                result.loc[count, 'month_diff'] = (12 - result.loc[count, 'month_current']) + result.loc[
                    count, 'month_next']

            result.loc[count, 'percent_MoM/diff'] = (
                    (((bathroom_median.loc[i, 'price'] * 100) / bathroom_median.loc[i - 1, 'price']) - 100) /
                    result.loc[count, 'month_diff']
            )
            count += 1

    # casas com 3 banheiros com crescimento MoM > 15
    result['MoM_maisDe15%'] = 'No'
    result.loc[(result['percent_MoM/diff'] > 15), 'MoM_maisDe15%'] = 'Yes'
    result

    # showing the answer
    resultT = str(
        'H5: Falso, menos da metade tem. Existem {} casas com 3 banheiros. Dessas, {} casas tiveram um crescimento MoM maior que 15%.'
        .format(result.shape[0], result.loc[(result['percent_MoM/diff'] >= 15)].shape[0]))

    st.header(resultT)
    return resultT


if __name__ == '__main__':
    # ETL
    # ---- Data Extraction
    path = '../datasets/kc_house_data.csv'
    df = get_data(path)

    # ---- Transformation
    buy_houses(df)
    sell_houses(df)
    df_h1 = hypothesis1(df)
    df_h2 = hypothesis2(df)
    df_h3 = hypothesis3(df)
    df_h4 = hypothesis4(df)
    df_h5 = hypothesis5(df)
