import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

class GeraInfos():
    def __init__(self):
        return
    def get_data():
        url = "https://raw.githubusercontent.com/seade-R/dados-covid-sp/master/data/dados_covid_sp.csv"
        filename = 'data/' + url.split("/")[-1]
        with open(filename, "wb") as f:
            r = requests.get(url)
            f.write(r.content)

        url = "https://raw.githubusercontent.com/seade-R/dados-covid-sp/master/data/br.csv"
        filename = 'data/' +  url.split("/")[-1]
        with open(filename, "wb") as f:
            r = requests.get(url)
            f.write(r.content)

    def data_brasil():
        GeraInfos.get_data()
        #Dados Brasil
        df_BR = pd.read_csv('data/br.csv', delimiter = ';')

        df_BR = pd.DataFrame(df_BR)
        df_BR[['datahora','casos_acum','obitos_acum']]

        #casos diários Brasil
        aux1 = np.empty(len(df_BR))
        for i in range(1,len(df_BR)):
            aux1[i] = df_BR['casos_acum'][i] - df_BR['casos_acum'][i-1]
        df_BR['casos_dia'] = aux1

        #óbitos diários Brasil
        aux2 = np.empty(len(df_BR))
        for i in range(1,len(df_BR)):
            aux2[i] = df_BR['obitos_acum'][i] - df_BR['obitos_acum'][i-1]
        df_BR['obitos_dia'] = aux2

        #média móvel de casos Brasil
        df_BR['media_movel_casos'] = df_BR['casos_dia'].rolling(window=7).mean()

        #média movel de óbitos no Brasil
        df_BR['media_movel_obitos'] = df_BR['obitos_dia'].rolling(window=7).mean()

        pd.options.display.float_format = '{:g}'.format
        return df_BR['casos_dia'], df_BR['obitos_dia'], df_BR['media_movel_casos'], df_BR['media_movel_obitos']
    

    def data_SP_city():
        #Dados municipios de SP
        df_mSP = pd.read_csv('data/dados_covid_sp.csv', delimiter = ';')
        df_mSP = pd.DataFrame(df_mSP)
        df_mSP = df_mSP[['datahora','nome_munic','casos','obitos','casos_novos','obitos_novos']]

        #Dados Cidade de São Paulo
        df_SaoPaulo = df_mSP.loc[(df_mSP.nome_munic == "São Paulo")]

        #média móvel de casos na cidade de SP
        df_SaoPaulo['media_movel_casos'] = df_SaoPaulo['casos_novos'].rolling(window=7).mean()

        #média movel de óbitos na cidade de SP
        df_SaoPaulo['media_movel_obitos'] = df_SaoPaulo['obitos_novos'].rolling(window=7).mean()

        pd.options.display.float_format = '{:g}'.format
        return df_SaoPaulo['casos_novos'], df_SaoPaulo['obitos_novos'], df_SaoPaulo['media_movel_casos'], df_SaoPaulo['media_movel_obitos']

    def data_SaoCarlos():
        #Dados municipios de SP
        df_mSP = pd.read_csv('data/dados_covid_sp.csv', delimiter = ';')
        df_mSP = pd.DataFrame(df_mSP)
        df_mSP = df_mSP[['datahora','nome_munic','casos','obitos','casos_novos','obitos_novos']]
        #Dados Cidade de São Carlos
        df_SaoCarlos = df_mSP.loc[(df_mSP.nome_munic == "São Carlos")]

        #média móvel de casos na cidade de SP
        df_SaoCarlos['media_movel_casos'] = df_SaoCarlos['casos_novos'].rolling(window=7).mean()

        #média movel de óbitos na cidade de SP
        df_SaoCarlos['media_movel_obitos'] = df_SaoCarlos['obitos_novos'].rolling(window=7).mean()

        pd.options.display.float_format = '{:g}'.format
        return df_SaoCarlos['casos_novos'], df_SaoCarlos['obitos_novos'], df_SaoCarlos['media_movel_casos'], df_SaoCarlos['media_movel_obitos']

    def data_Atibaia():
        #Dados municipios de SP
        df_mSP = pd.read_csv('data/dados_covid_sp.csv', delimiter = ';')
        df_mSP = pd.DataFrame(df_mSP)
        df_mSP = df_mSP[['datahora','nome_munic','casos','obitos','casos_novos','obitos_novos']]
        #Dados Cidade de Atibaia
        df_Atibaia = df_mSP.loc[(df_mSP.nome_munic == "Atibaia")]

        #média móvel de casos na cidade de SP
        df_Atibaia['media_movel_casos'] = df_Atibaia['casos_novos'].rolling(window=7).mean()

        #média movel de óbitos na cidade de SP
        df_Atibaia['media_movel_obitos'] = df_Atibaia['obitos_novos'].rolling(window=7).mean()

        pd.options.display.float_format = '{:g}'.format

        fig, axs = plt.subplots(2,figsize = (20, 20))
        return df_Atibaia['casos_novos'], df_Atibaia['obitos_novos'], df_Atibaia['media_movel_casos'], df_Atibaia['media_movel_obitos']

    def plotGraphs():
        df_BR['casos_dia'], df_BR['obitos_dia'], df_BR['media_movel_casos'], df_BR['media_movel_obitos'] = data_brasil()
        df_SaoPaulo['casos_dia'], df_SaoPaulo['obitos_dia'], df_SaoPaulo['media_movel_casos'], df_SaoPaulo['media_movel_obitos'] = data_SP_city()
        df_SaoCarlos['casos_dia'], df_SaoCarlos['obitos_dia'], df_SaoCarlos['media_movel_casos'], df_SaoCarlos['media_movel_obitos'] = data_SaoCarlos()
        df_Atibaia['casos_dia'], df_Atibaia['obitos_dia'], df_Atibaia['media_movel_casos'], df_Atibaia['media_movel_obitos'] = data_Atibaia()
        #Plot Novos Casos Brasil
        axs[0].bar(df_BR['datahora'], df_BR['casos_dia'],  width = 0.7, color = 'c') 
        axs[0].plot(df_BR['datahora'], df_BR['media_movel_casos'], color = "b") 
        axs[0].set(xlabel='Data', ylabel='No. de casos',title = 'Novos casos diários no Brasil')
        axs[0].set_xticks([])


        #Plot novos óbitos Brasil
        axs[1].bar(df_BR['datahora'], df_BR['obitos_dia'],  width = 0.7, color = 'thistle') 
        axs[1].plot(df_BR['datahora'], df_BR['media_movel_obitos'], color = "purple") 
        axs[1].set(xlabel='Data', ylabel='No. de óbitos',title = 'Novos óbitos diários no Brasil')
        axs[1].set_xticks([])
        plt.savefig('Graphs/Dados_Brasil.jpg', transparent = False)

        fig, axs = plt.subplots(2,figsize = (20, 20))

        #Plot Novos Casos cidade de São Paulo
        axs[0].bar(df_SaoPaulo['datahora'], df_SaoPaulo['casos_novos'],  width = 0.7, color = 'c') 
        axs[0].plot(df_SaoPaulo['datahora'], df_SaoPaulo['media_movel_casos'], color = "b") 
        axs[0].set(xlabel='Data', ylabel='No. de casos',title = 'Novos casos diários na cidade de São Paulo')
        axs[0].set_xticks([])


        #Plot novos óbitos cidade de São Paulo
        axs[1].bar(df_SaoPaulo['datahora'], df_SaoPaulo['obitos_novos'],  width = 0.7, color = 'thistle') 
        axs[1].plot(df_SaoPaulo['datahora'], df_SaoPaulo['media_movel_obitos'], color = "purple") 
        axs[1].set(xlabel='Data', ylabel='No. de óbitos',title = 'Novos óbitos diários na cidade de São Paulo')
        axs[1].set_xticks([])
        plt.savefig('Graphs/Dados_Cidade_SP.jpg', transparent = False)

        fig, axs = plt.subplots(2,figsize = (20, 20))
        #Plot Novos Casos cidade São Carlos
        axs[0].bar(df_SaoCarlos['datahora'], df_SaoCarlos['casos_novos'],  width = 0.7, color = 'c') 
        axs[0].plot(df_SaoCarlos['datahora'], df_SaoCarlos['media_movel_casos'], color = "b") 
        axs[0].set(xlabel='Data', ylabel='No. de casos',title = 'Novos casos diários na cidade de São Carlos')
        axs[0].set_xticks([])


        #Plot novos óbitos cidade São Carlos
        axs[1].bar(df_SaoCarlos['datahora'], df_SaoCarlos['obitos_novos'],  width = 0.7, color = 'thistle') 
        axs[1].plot(df_SaoCarlos['datahora'], df_SaoCarlos['media_movel_obitos'], color = "purple") 
        axs[1].set(xlabel='Data', ylabel='No. de óbitos',title = 'Novos óbitos diários na cidade de São Carlos')
        axs[1].set_xticks([])
        plt.savefig('Graphs/Dados_Sao_Carlos.jpg', transparent = False)

        fig, axs = plt.subplots(2,figsize = (20, 20))
        #Plot Novos Casos cidade de Atibaia
        axs[0].bar(df_Atibaia['datahora'], df_Atibaia['casos_novos'],  width = 0.7, color = 'c') 
        axs[0].plot(df_Atibaia['datahora'], df_Atibaia['media_movel_casos'], color = "b") 
        axs[0].set(xlabel='Data', ylabel='No. de casos',title = 'Novos casos diários na cidade de Atibaia')
        axs[0].set_xticks([])


        #Plot novos óbitos cidade de Atibaia
        axs[1].bar(df_Atibaia['datahora'], df_Atibaia['obitos_novos'],  width = 0.7, color = 'thistle') 
        axs[1].plot(df_Atibaia['datahora'], df_Atibaia['media_movel_obitos'], color = "purple") 
        axs[1].set(xlabel='Data', ylabel='No. de óbitos',title = 'Novos óbitos diários na cidade de Atibaia')
        axs[1].set_xticks([])

        plt.savefig('Graphs/Dados_Atibaia.jpg', transparent = False)

def data(update: Update, context: CallbackContext) -> None:

    casos_dia_BR, obitos_dia_BR, media_movel_casos_BR, media_movel_obitos_BR = GeraInfos.data_brasil()
    casos_dia_SaoPaulo, obitos_dia_SaoPaulo, media_movel_casos_SaoPaulo, media_movel_obitos_SaoPaulo = GeraInfos.data_SP_city()
    casos_dia_SaoCarlos, obitos_dia_SaoCarlos, media_movel_casos_SaoCarlos, media_movel_obitos_SaoCarlos = GeraInfos.data_SaoCarlos()
    casos_dia_Atibaia, obitos_dia_Atibaia, media_movel_casos_Atibaia, media_movel_obitos_Atibaia = GeraInfos.data_Atibaia()    

    bot = telegram.Bot(token='1604268086:AAExs5Qxp6V1oj_uNSYRYTsk0qAmCZv9sTM')
    update.message.reply_text( 
        f"Dados do Brasil:\n" \
        f"Novos casos Hoje: {int(casos_dia_BR.iloc[-1])}\n" \
        f"Novos óbitos Hoje: {int(obitos_dia_BR.iloc[-1])}\n" \
        f"Graficos:")
    bot.send_photo(chat_id=update.message.chat_id, photo=open("Graphs/Dados_Brasil.jpg", "rb"))
    update.message.reply_text(
        f"Dados de São Paulo:\n" \
        f"Novos casos Hoje: {int(casos_dia_SaoPaulo.iloc[-1])}\n" \
        f"Novos óbitos Hoje: {int(obitos_dia_SaoPaulo.iloc[-1])}\n" \
        f"Graficos:")
    bot.send_photo(chat_id=update.message.chat_id, photo=open("Graphs/Dados_Cidade_SP.jpg", "rb"))
    update.message.reply_text(
        f"Dados de São Carlos:\n" \
        f"Novos casos Hoje: {int(casos_dia_SaoCarlos.iloc[-1])}\n" \
        f"Novos óbitos Hoje: {int(obitos_dia_SaoCarlos.iloc[-1])}\n" \
        f"Graficos:")
    bot.send_photo(chat_id=update.message.chat_id, photo=open("Graphs/Dados_Sao_Carlos.jpg", "rb"))
    update.message.reply_text(
        f"Dados de Atibaia:\n" \
        f"Novos casos Hoje: {int(casos_dia_Atibaia.iloc[-1])}\n" \
        f"Novos óbitos Hoje: {int(obitos_dia_Atibaia.iloc[-1])}\n" \
        f"Graficos:")
    bot.send_photo(chat_id=update.message.chat_id, photo=open("Graphs/Dados_Atibaia.jpg", "rb"))


updater = Updater('1604268086:AAExs5Qxp6V1oj_uNSYRYTsk0qAmCZv9sTM')

updater.dispatcher.add_handler(CommandHandler('data', data))

updater.start_polling()
updater.idle()

