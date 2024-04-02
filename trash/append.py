import json, requests
from time import sleep

iteration = 0
while True:
    sleep(20)
    r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD')
    bitcoin_value = float(json.loads(r.content)["USD"])
    print(f'{iteration}) $ {bitcoin_value}')
    with open('btc cource.txt', 'r', encoding='utf-8') as f:
            file = str(f.readline(-1))
    with open('btc cource.txt', 'a', encoding='utf-8') as f:
            f.write(f'{file}\n{str(bitcoin_value)}')

    iteration+=1