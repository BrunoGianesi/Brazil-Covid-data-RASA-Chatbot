
#%%
import requests
import os
import aiohttp
import asyncio
import json

#%%
def download_data():
    
    
    API = f"https://xx9p7hp1p7.execute-api.us-east-1.amazonaws.com/prod/PortalGeral?X-Parse-Application-Id=unAFkcaNDeXajurGB7LChj8SgQYS2ptm"
    r = requests.get(API)
    r = r.json()
    r_json = dict(r)
    url = r_json['results'][0]['arquivo']['url']
    date = r_json['results'][0]['dt_atualizacao']
    filename = f'{os.getcwd()}/actions/Image_Generation/database/' + "Dados.csv"
    Date_filename = f'{os.getcwd()}/actions/Image_Generation/database/' + 'date_infos.json'
    with open(Date_filename) as json_file:
        saved_date = json.load(json_file)
        saved_date = saved_date['saved_date']
    if not os.path.isfile(f'{os.getcwd()}/actions/Image_Generation/database/' + "Dados.csv") or \
         str(date) != str(saved_date):
        print("Downloading data...")
        database = requests.get(url)
        with open(Date_filename, "w") as f:
            dictionary = dict({'saved_date': date})
            json.dump(dictionary, f, indent=1)
        with open(filename, "wb") as f:
            f.write(database.content)
            print("Minister of Health data downloaded")
    else:
        print("Data already downloaded")
    return date
