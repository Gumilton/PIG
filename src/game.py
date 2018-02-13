import numpy as np
from utils import *


def play_one_round(pl_list, starter):

    c1 = pl_list[starter].render(shown_cards=[], lead_card=None)
    c2 = pl_list[(starter + 1) % 4].render(shown_cards=[], lead_card=c1, previous=[c1])
    c3 = pl_list[(starter + 2) % 4].render(shown_cards=[], lead_card=c1, previous=[c1, c2])
    c4 = pl_list[(starter + 3) % 4].render(shown_cards=[], lead_card=c1, previous=[c1, c2, c3])
    cards = np.array([c1, c2, c3, c4])
    collector = (starter + who_collect(c1, c2, c3, c4)) % 4
    pl_list[collector].collect(cards)
    return cards, starter, collector


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
        rendered_cards, last_starter, collector = play_one_round(pl_list, starter)
        starter = collector

    next_starter = who_get_pig(received, 23)

    return received, scores, next_starter


def run(pl_list, n_games):

    final_scores = {pl: 0 for pl in pl_list}
    scores = {pl: [] for pl in pl_list}
    starter_player = None
    for counter_game in range(len(n_games)):
        received, temp_scores, next_starter = play_one_game(pl_list, starter=starter_player)
        starter_player = next_starter
        for pl, s in temp_scores.items():
            final_scores[pl] += s
            scores[pl].append(s)
