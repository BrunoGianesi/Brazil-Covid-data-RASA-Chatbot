# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


# %%
def filter_dataset(
    Places: list
) -> dict:
# try:
    full_df = pd.read_csv('actions/Image_Generation/database/Dados.csv', delimiter = ';')
# except Exception:
#     print(f"The data file does not exist")
    Places_dict = {}
    for place in Places:
        local_df = full_df.query(f'regiao == "{place}"')
        for chances in range(3):
            if chances == 0:
                local_df = full_df.query(f'regiao == "{place}"')
            elif local_df.empty and chances == 1:
                local_df = full_df.query(f'estado == "{place}"')
            elif local_df.empty and chances == 2:
                local_df = full_df.query(f'municipio == "{place}"')
                if local_df.empty:
                    raise Exception('O Local inserido não foi encontrado')
        Places_dict[place] = local_df
    
    return Places_dict


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
    for dataframe in dataframes.items():
        local = dataframe[0]
        #normalize local
        local_norm = local.replace("ã", "a")
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


