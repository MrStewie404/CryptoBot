import requests
import json
from config import coins

def get_coins() -> list:
    values = []

    for coin in coins:
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={coin[0]}&tsyms={coin[1]}')
        value = float(json.loads(r.content)[f"{coin[1]}"])
        values.append([coin[0], value])

    # page_values = ""
    # for coin in values:
    #     page_values += f'{coin[0]} = {coin[1]}\n'

    return values


def get_rub():
    # r = requests.get('https://api.currencyapi.com/v3/latest?apikey=cur_live_Glm4tURq3pUl0ncm5tsSNukm1vlui74b5p2gdEL0&currencies=RUB')
    # return float(json.loads(r.content)['data']['RUB']['value'])
    return 1


# for value in get_coins():
#     print(value)