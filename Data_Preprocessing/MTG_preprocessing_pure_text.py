import numpy as np
import pandas as pd

def _get_col_identity_tokens(mana_cost):
    color = ""
    if type(mana_cost) != int:
        color += mana_cost.count("G") * "G "
        color += mana_cost.count("U")* "U "
        color += mana_cost.count("R")* "R "
        color += mana_cost.count("W")* "W "
        color += mana_cost.count("B")*"B "
    return color[:-1]

def _get_col_req_tokens(requirement):
    num_color_symbols = requirement
    if type(requirement) != int:
        num_color_symbols = requirement.count("{")
    if num_color_symbols < 2:
        return "LOWCOLREQ"
    elif num_color_symbols == 2:
        return "MEDCOLREQ"
    else:
        return "HIGHCOLREQ"

def _get_cmc_req_tokens(requirement):
    if requirement < 3:
        return "LOWCMCREQ"
    elif requirement < 5:
        return "MEDCMCREQ"
    else:
        return "HIGHCMCREQ"

def _get_stats_tokens(cmc, power, thougness, loyalty):
    if cmc == 0:
        cmc = 1
    stats_ratio = (int(power) + int(thougness))/int(cmc)

    # Planeswalker are creatures(normally).
    if loyalty != 0:
        stats_ratio = int(loyalty)/int(cmc)

    if stats_ratio <= 0.6:
        return "LOWSTATS"
    elif stats_ratio <= 1:
        return "MEDSTATS"
    else:
        return "HIGHSTATS"


def get_useful_fields_raw_data():
    card_data = pd.read_csv("../Data/MTG/merged_data.csv")
    card_data.fillna(0, inplace=True)

    # Keeping only relevant columns for basic text analysis
    card_data = card_data.drop(columns=['object', 'id', 'oracle_id', 'multiverse_ids', 'lang',
       'released_at', 'uri', 'scryfall_uri', 'layout', 'highres_image',
       'image_uris', 'legalities', 'games', 'reserved', 'foil', 'nonfoil',
       'oversized', 'promo', 'reprint', 'variation', 'set',
       'set_type', 'set_uri', 'set_search_uri', 'scryfall_set_uri',
       'rulings_uri', 'prints_search_uri', 'collector_number', 'digital',
        'card_back_id', 'artist', 'artist_ids', 'illustration_id',
       'border_color', 'frame', 'full_art', 'textless', 'booster',
       'story_spotlight', 'related_uris', 'edhrec_rank',
       'frame_effects', 'promo_types', 'preview', 'tcgplayer_id',
       'flavor_text', 'watermark', 'all_parts', 'card_faces', 'printed_name',
       'printed_type_line', 'printed_text', 'life_modifier', 'hand_modifier',
       'color_indicator', 'arena_id', 'mtgo_id', 'variation_of',
       'mtgo_foil_id', 'colors'])

    return  card_data

def get_useful_fields_preprocessed_data():
    card_data = get_useful_fields_raw_data()
    prediction_ready_data = []

    for card in card_data.iterrows():
        try:
            cat_card_text = ""
            cat_card_text += _get_col_identity_tokens(card[1]['mana_cost']) + " "
            cat_card_text += _get_col_req_tokens(card[1]['mana_cost']) + " "
            cat_card_text += _get_cmc_req_tokens(card[1]['cmc']) + " "
            cat_card_text += str(card[1]['type_line']) + " " + str(card[1]['oracle_text']) + " "
            cat_card_text += card[1]['rarity'] + " "

            if card[1]['power'] in ["X", "*"] or card[1]['toughness'] in ["X", "*"] or card[1]['loyalty'] in ["X", "*"]:
                cat_card_text += "VARSTATS"
            elif int(card[1]['power']) + int(card[1]['toughness']) + int(card[1]['loyalty']) != 0:
                cat_card_text += _get_stats_tokens(card[1]['cmc'], card[1]['power'], card[1]['toughness'], card[1]['loyalty'])

            prediction_ready_data.append((cat_card_text, {"name": card[1]['name'], "set": card[1]['set_name'],"profitable": card[1]['profitable']}))

        except:
            print(card[1])

    return prediction_ready_data