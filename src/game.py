import numpy as np
from utils import *


def show_cards(pl_list):
    shown_cards = []
    for pl in pl_list:
        shown_cards.extend(pl.show_card())
    return shown_cards


def play_one_round(pl_list, starter, shown_cards, rendered_cards):
    collected_cards = {pl: [] for pl in range(len(pl_list))}
    collected_value_cards = {pl: [] for pl in range(len(pl_list))}

    c1 = pl_list[starter].render(shown_cards=shown_cards, previous=[],
                                 rendered_cards=rendered_cards)
    c2 = pl_list[(starter + 1) % 4].render(shown_cards=shown_cards, previous=[c1],
                                           rendered_cards=rendered_cards)
    c3 = pl_list[(starter + 2) % 4].render(shown_cards=shown_cards, previous=[c1, c2],
                                           rendered_cards=rendered_cards)
    c4 = pl_list[(starter + 3) % 4].render(shown_cards=shown_cards, previous=[c1, c2, c3],
                                           rendered_cards=rendered_cards)
    cards = [c1, c2, c3, c4]
    collector = (starter + who_collect(c1, c2, c3, c4)) % 4

    pl_list[collector].collect(cards)
    collected_cards[collector].extend(cards)

    for card in cards:
        if card in VALUE_CARDS:
            pl_list[collector].collect_value_cards(card)
            collected_value_cards[collector].append(card)

    return cards, starter, collector, collected_cards, collected_value_cards, rendered_cards + cards


def play_one_game(pl_list, starter=None):
    final_collected = {pl: [] for pl in range(len(pl_list))}
    final_collected_value_cards = {pl: [] for pl in range(len(pl_list))}

    all_cards = np.arange(52)
    np.random.shuffle(all_cards)

    for i in range(len(pl_list)):
        pl_list[i].add_cards(all_cards[(i * 13): ((i + 1) * 13)])

    shown_cards = show_cards(pl_list)

    if starter is None:
        # spade 2 is numbered as 0
        starter = get_starter_player_by_holding_card(all_cards, 0)

    round_game = 0
    rendered_cards = []
    while round_game < 13:
        round_game += 1
        _, _, collector, collected_cards, collected_value_cards, \
            rendered_cards = play_one_round(pl_list, starter, shown_cards, rendered_cards)
        starter = collector

        for pl, cards in collected_cards.items():
            final_collected[pl].extend(cards)

        for pl, cards in collected_value_cards.items():
            final_collected_value_cards[pl].extend(cards)

    next_starter = who_get_pig(final_collected_value_cards, 23)
    scores = calculate_scores(final_collected_value_cards, shown_cards=shown_cards)

    return final_collected_value_cards, scores, next_starter


def run(pl_list, n_games, verbose=False):
    final_scores = {pl: 0 for pl in range(len(pl_list))}
    scores = {pl: [] for pl in range(len(pl_list))}
    starter_player = None
    for counter_game in range(n_games):
        if verbose:
            print("Start Game:", counter_game)

        received, temp_scores, next_starter = play_one_game(pl_list, starter=starter_player)
        starter_player = next_starter
        if verbose:
            print("Player", starter_player, "Got PIG in Game", counter_game)
            # print("Collected cards\n", {pl: decode_card_list(cards) for pl, cards in received.items()})
            print("Game", counter_game, "Game Scores:", temp_scores)

        for pl, s in temp_scores.items():
            final_scores[pl] += s
            scores[pl].append(s)

        if verbose:
            print("Game", counter_game, "Accumulated Scores:", final_scores)
