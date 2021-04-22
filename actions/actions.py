# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from actions.Image_Generation import data_manipulation, get_data_MS, image_uploader, secrets_aws

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import matplotlib.pyplot as plt
import requests
import pandas as pd
import numpy as np


class SendGraphs(Action):

    def name(self) -> Text:
        return "send_graphs"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=f"Buscando dados...")
        places_list = tracker.slots.get('local')
        
        #Get data from Health Ministry database and build Graphs
        date = get_data_MS.download_data()

        dataframes = data_manipulation.filter_dataset(places_list)
        dataframes = data_manipulation.creating_rolling_mean(dataframes)
        data_manipulation.create_graphs(dataframes)

        #Send Images to AWS
        image_uploader.upload(secrets_aws.access_key, secrets_aws.secret_access_key)
        dispatcher.utter_message(text= f"Atualizado em: {date}")
        for place in places_list:
            #normalize local
            place_norm = place.replace("ã", "a")
            place_norm = place.replace(" ", "_")
            dispatcher.utter_message(text=f"Dados de: {place}")
            
            dispatcher.utter_message(text=f"https://rasa-project-image-holder.s3-sa-east-1.amazonaws.com/Graphs/Casos_{place_norm}.jpg")
            dispatcher.utter_message(text=f"https://rasa-project-image-holder.s3-sa-east-1.amazonaws.com/Graphs/Obitos_{place_norm}.jpg")



        return []
