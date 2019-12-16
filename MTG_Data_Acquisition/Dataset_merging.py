import numpy as np
import pandas as pd
import datetime
import copy

card_data = pd.read_csv("./Data/MTG/filtered_data.csv")
price_data = np.load("./Data/MTG/priceData.npy")
count = 0
index = 0

merged_price = copy.deepcopy(card_data)

merged_price["profitable"] = 0
dict = {}

for price in price_data:
    dict[price[0]] = price[1]

for card in card_data.iterrows():
    try:
        card_released = datetime.datetime.strptime(card[1]["released_at"], '%Y-%m-%d')
        price = dict[str(card[1]['name']) + "-" + str(card[1]["set_name"])]

        # Let's assume a month is 30 days. As long as it's consistent it does not really matter.
        price_one_month = [price[i] for i in range(len(price)) if price[i][0] == (card_released + datetime.timedelta(days=30))]

        if len(price_one_month) == 0:
            continue

        # We will consider the card profitable iif it see's an increase of at least 20% in value (this accounts for
        # the Ebay/Paypal fees). This could be different if we had other selling avenues, but I considered we
        # are buying/selling through Ebay. We also want to sell in the two years after buying, since that is where
        # standard is going to affect the prices the most.
        profits_days = [price[i][1] for i in range(len(price)) if (price[i][1] > (price_one_month[0][1] * 1.2) and
                                                                   price_one_month[0][0] < price[i][0] and
                                                                   price_one_month[0][0] + datetime.timedelta(days=700) > price[i][0])]

        # Getting rids of short spikes, which we probably could not sell.
        if len(profits_days) > 7:
            count += 1
            #print(f"{card[1]['name']} is profitable")
            card[1]["profitable"] = 1
            merged_price.set_value(index,'profitable',1)
        index += 1
    except:
        print(f"Could not find data for {str(card[1]['name'])} from set {str(card[1]['set_name'])}")
        continue
    pass

print(f"{count}/{len(merged_price)} profitable cards detected.")
merged_price.to_csv("./Data/MTG/merged_data.csv",index=False)