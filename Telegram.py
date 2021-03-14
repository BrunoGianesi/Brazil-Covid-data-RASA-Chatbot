import telegram_send
import Atualizacao

Atualizacao.GeraInfos.gera()

telegram_send.send(messages=["Graficos do Brasil:"])
with open("Dados_Brasil.jpg", "rb") as f:
        telegram_send.send(images=[f])
telegram_send.send(messages=["Graficos da cidade de São Paulo:"])        
with open("Dados_Cidade_SP.jpg", "rb") as f:
        telegram_send.send(images=[f])
telegram_send.send(messages=["Graficos da cidade de São Carlos:"])   
with open("Dados_Sao_Carlos.jpg", "rb") as f:
        telegram_send.send(images=[f])
telegram_send.send(messages=["Graficos da cidade de Atibaia:"])   
with open("Dados_Atibaia.jpg", "rb") as f:
        telegram_send.send(images=[f])