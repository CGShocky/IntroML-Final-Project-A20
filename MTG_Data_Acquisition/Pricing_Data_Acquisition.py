import numpy as np
import pandas as pd
from datetime import datetime
import requests
import urllib.parse as parser
import re
import unidecode
import time

filtered_data = pd.read_csv("./Data/MTG/filtered_data.csv")
card_prices = []
for card in filtered_data.iterrows():
    name = card[1]['name']
    name = unidecode.unidecode(name)
    set = card[1]['set_name']

    if set == "Magic 2015" or set == "Magic 2014":
        set = set + " Core Set"
    print(f"Trying to get price info for: {set} - {name}")
    try:
        if len(name.split("//")) > 1:
            if len(name.split("//")[0].split(" ")) > 2:
                name = name.split("//")[0]

        regex = re.compile('[^a-zA-Z0-9 -]')
        name = ' '.join(regex.sub('', name).split())
        set = ' '.join(regex.sub('', set).split())
        card_name = parser.quote_plus(name)
        set_name = parser.quote_plus(set)
        http_request = f"https://www.mtggoldfish.com/price/{set_name}/{card_name}#paper"
        response = requests.get(http_request)
        if response.ok == False:
            print(f"Fail to retreive price info for: {set} - {name}")

        # Sometimes, Goldfish blacklists us for a little bit, so we have to wait a little. Goldfish only
        # seems to soft block us for a reasonable amount of time. We could accelerate collection with proxies though.
        while "Throttled" in response.text:
            print("Waiting 5 seconds to send new requests.")
            time.sleep(5)
            response = requests.get(http_request)

        # Request parsing here. It's hardcoded but the responses should not change in structure, so that should be ok.
        jsfunctionwithdata = response.text.split("<script type=\"text/javascript\">")[-1]
        jsfunctionwithdata = jsfunctionwithdata.split('var d')[-2]
        dataPrices = [(datetime.strptime(re.findall("([0-9]{4}\-[0-9]{2}\-[0-9]{2})", i)[0], '%Y-%m-%d'), float(i.split(',')[-1].split("\"")[0])) for i in jsfunctionwithdata.split('\n') if '+=' in i]
        card_prices.append((card[1]['name'] + "-" + card[1]['set_name'],dataPrices))
    except:
        print(f"Could not parse data for {card[1]['name']} : {card[1]['set_name']}")
        print(f"Response {response.text}")

np.save("./Data/MTG/priceData.npy",np.array(card_prices))
