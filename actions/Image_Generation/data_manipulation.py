# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from fuzzywuzzy import process
import logging

logger = logging.getLogger(__name__)

# %%
def filter_dataset(
    Places: list
) -> dict:
    try:
        full_df = pd.read_csv('actions/Image_Generation/database/Dados.csv', delimiter = ';')
    except Exception:
        logger.exception("The data file does not exist")
    Places_dict = {}
    cities_list = list_cities(full_df)
    for place in Places:
        place = process.extractOne(place, cities_list)
        place = place[0]
        correct_places = []
        correct_places.append(place)
        local_df = full_df.query(f'regiao == "{place}"')
        for chances in range(2):
            if chances == 0:
                local_df = full_df.query(f'regiao == "{place}"')
            elif local_df.empty and chances == 1:
                local_df = full_df.query(f'municipio == "{place}"')
                if local_df.empty:
                    return False
        Places_dict[place] = local_df
    return Places_dict, correct_places

# %%
def creating_rolling_mean(
    dataframes: dict
) -> dict:
    for dataframe in dataframes.values():
        dataframe['mediaMovelCasos'] = dataframe['casosNovos'].rolling(window=7).mean()
        dataframe['mediaMovelObitos'] = dataframe['obitosNovos'].rolling(window=7).mean()
    return dataframes
# %%
def create_graphs(
    dataframes: dict
) -> None:
    #remove remanecent graphs
    for f in os.listdir('actions/Image_Generation/Graphs'):
        os.remove(os.path.join('actions/Image_Generation/Graphs', f))
    logger.info('Generating graphs...')
    for dataframe in dataframes.items():
        local = dataframe[0]
        #normalize local
        local_norm = local.replace(" ", "_")
        dataframe = dataframe[1]
        #Plot Novos Casos 
        fig, axs = plt.subplots()
        axs.bar(dataframe['data'], dataframe['casosNovos'],  width = 0.7, color = 'c') 
        axs.plot(dataframe['data'], dataframe['mediaMovelCasos'], color = "b") 
        axs.set(xlabel='Data', ylabel='No. de casos',title = f'Novos casos diários em {local}')
        plt.xticks(rotation=60)
        plt.xticks(np.arange(0, len(dataframe)+1, 0.5))
        axs.locator_params(nbins=14, axis='x')
        plt.grid(axis='y', linestyle = '--', linewidth = 0.5)
        plt.savefig(f'{os.getcwd()}/actions/Image_Generation/Graphs/Casos_{local_norm}.jpg', transparent = False, dpi=100)

        #Plot Novos Óbitos
        fig, axs = plt.subplots()
        axs.bar(dataframe['data'], dataframe['obitosNovos'],  width = 0.7, color = 'm') 
        axs.plot(dataframe['data'], dataframe['mediaMovelObitos'], color = "purple") 
        axs.set(xlabel='Data', ylabel='No. de óbitos',title = f'Novos óbitos diários em {local}')
        plt.xticks(rotation=60)
        plt.xticks(np.arange(0, len(dataframe)+1, 0.5))
        axs.locator_params(nbins=14, axis='x')
        plt.grid(axis='y', linestyle = '--', linewidth = 0.5)
        plt.savefig(f'{os.getcwd()}/actions/Image_Generation/Graphs/Obitos_{local_norm}.jpg', transparent = False, dpi=100)


#%%
def list_cities(dataframe):
    full_df = dataframe
    local_df_regiao = full_df['regiao'].tolist()
    local_df_municipio = full_df['municipio'].tolist()
    local_df_regiao = list(dict.fromkeys(local_df_regiao))
    local_df_municipio = list(dict.fromkeys(local_df_municipio))
    local_df = []
    local_df = local_df_regiao + local_df_municipio

    return local_df
    # with open('nlu-lookup.yml', 'w') as file:

    #     file.write('- lookup: local\n')

    #     file.write('  examples: |\n')
    #     for listitem in local_df:
    #         file.write(f'    - Mostrar graficos de [{listitem}](local)\n')
