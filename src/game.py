import numpy as np
from utils import *


def play_one_round():
    raise NotImplementedError()


def play_one_game(pl_list, starter=None):
    received = {pl: [] for pl in pl_list}
    scores = {pl: 0 for pl in pl_list}

    all_cards = np.arange(52)
    np.random.shuffle(all_cards)

    for i in range(len(pl_list)):
        pl_list[i].add_cards(all_cards[(i * 13): ((i + 1) * 13)])

    if starter is None:
        # spade 2 is numbered as 0
        starter = get_starter_player_by_holding_card(all_cards, 0)

    round_game = 0
    while round_game < 14:
        round_game += 1
        play_one_round()

        raise NotImplementedError()

    next_starter = who_get_pig(received, 23)

    return received, scores, next_starter


def run(pl_list, n_games):

    scores = {pl: 0 for pl in pl_list}
    starter_player = None
    for counter_game in range(len(n_games)):
        received, temp_scores, next_starter = play_one_game(pl_list, starter=starter_player)
        starter_player = next_starter
        for pl, s in temp_scores.items():
            scores[pl] += s
