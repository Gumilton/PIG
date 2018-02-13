import numpy as np


def get_starter_player_by_holding_card(all_cards, starter_card=0):
    return np.where(all_cards == starter_card)[0].tolist()[0] // 13


def who_get_pig(received_card_dict, pig_card=23):
    for pl, cards in received_card_dict.items():
        if 23 in cards:
            return pl