from requests import Request,Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from dotenv import dotenv_values
import re
from os.path import exists
from os import listdir, remove
from os.path import isfile, join

config = dotenv_values(".env")
COINTOKEN=config['COIN_TOKEN']
def sync_coin_list():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
    parameters = {
    'start':'1',
    'limit':'5000',
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': COINTOKEN,
    }
    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        
        with open('./resources/coin_list.json','w+') as f:
            f.write(json.dumps(data,indent=4))
        
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

def add_coin(name, coins):
    coins = re.split(',\s*', coins)
    path_to_file=f'./resources/coin_list/{name}.json'
    coins_data=load_coin(path_to_file)
    not_found = []
    found = []
    for coin in coins:
        f_coin = find_coin(coin)
        if f_coin==None:
            not_found.append(coin)
        else:
            found.append(coin)
            coins_data.append(f_coin)
        
        
    coins_data = [i for n, i in enumerate(coins_data) if i not in coins_data[n + 1:]]
    
    with open(path_to_file,'w+') as f:
        f.write(json.dumps(coins_data,indent=4))
    Message = ""
    if len(found) > 0:
        Message = f"Added {', '.join(found)}"
    if len(not_found) > 0:
        Message += f"\nUnable to find {', '.join(not_found)}"
    
    return Message
def remove_coin(name, coins):
    coins = re.split(',\s*', coins)
    path_to_file=f'./resources/coin_list/{name}.json'
    coins_data=load_coin(path_to_file)
    
    new_coins_data = []
    
    for c in coins_data:
        if c['symbol'].lower() not in coins:
            new_coins_data.append(c)
    
    with open(path_to_file,'w+') as f:
        f.write(json.dumps(new_coins_data,indent=4))

def remove_list(name):
    path_to_file=f'./resources/coin_list/{name}.json'
    remove(path_to_file)

def find_coin(coin_symbol):
    with open('./resources/coin_list.json','r') as f:
        data=json.loads(f.read())
        data=data['data']
    coin_data = [icoin for icoin in data if icoin['symbol'].lower() == coin_symbol.lower()]
    if coin_data==[]:
        return None
    else:
        return coin_data[0]

def load_coin(path_to_file):
    if exists(path_to_file):
        with open(path_to_file,'r') as f:
                return json.loads(f.read())
    else:
        return []

def get_coin_list(name):
    path_to_file=f'./resources/coin_list/{name}.json'
    data = load_coin(path_to_file)
    if data==[]:
        return "list not exist"
    else:
        message = ["Name: "+d['name']+"\tSymbol:"+d['symbol'] for d in data]
        return "\n".join(message)

def get_coin_lists():
    path_to_file=f'./resources/coin_list/'
    filenames = [f.split('.')[0] for f in listdir(path_to_file) if isfile(join(path_to_file, f))]
    filenames = "\n".join(filenames)
    return filenames

def get_coin_price(name,convert="AUD"):
    path_to_file=f'./resources/coin_list/{name}.json'
    coins_data=load_coin(path_to_file)
    coin_id=""
    for coin in coins_data:
        if coin_id =="":
            coin_id += str(coin['id'])
        else:
            coin_id += ","+str(coin['id'])

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
    'id':coin_id,
    'convert':convert
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': COINTOKEN,
    }
    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        data = data['data']
        results = []
        for ci in coin_id.split(","):
            d = data[ci]
            name = d['name']
            symbol = d['symbol']
            rank = d['cmc_rank']
            price = d['quote'][f"{convert}"]["price"]
            price = round(price,2)
            per_change_1h = d['quote'][f"{convert}"]["percent_change_1h"]
            per_change_1h = round(per_change_1h,2)
            per_change_24h = d['quote'][f"{convert}"]["percent_change_24h"]
            per_change_24h = round(per_change_24h,2)
            message = f"[{name}-{symbol}]\nrank: {rank}\nprice: {price} {convert}\nper_change_1h: {per_change_1h}\nper_change_24h: {per_change_24h}"
            results.append(message)
        return "\n------\n".join(results)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

if __name__ == '__main__':
    
    #get_coin_price('tam')
    # remove_list('terry')
    # Message=add_coin("tam", "adsfadsfds, fdafdsa, icx")
    # # print(Message)
    # sync_coin_list()
    pass