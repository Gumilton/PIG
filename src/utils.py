import numpy as np


DIGIT_DECODE = {9: "J",
                10: "Q",
                11: "K",
                12: "A"}
DIGIT_DECODE.update({i: str(i + 2) for i in range(9)})

SHAPE_DECODE = {0: "club",
                1: "spade",
                2: "diamond",
                3: "heart"}

SCORE_ADD = {23: lambda x: x + 100,
             35: lambda x: x - 100,
             51: lambda x: x + 50,
             50: lambda x: x + 40,
             49: lambda x: x + 30,
             48: lambda x: x + 20}

SCORE_ADD.update({i: lambda x: x + 10 for i in range(42, 48, 1)})

SCORE_MUL = {8: lambda x: x * 2}

def reverse_dict(dic):
    return {v: k for k, v in dic.items()}


DIGIT_ENCODE = reverse_dict(DIGIT_DECODE)
SHAPE_ENCODE = reverse_dict(SHAPE_DECODE)


def get_starter_player_by_holding_card(all_cards, starter_card=0):
    return np.where(all_cards == starter_card)[0].tolist()[0] // 13


def who_get_pig(players_cards, pig_card=23):
    for pl, cards in players_cards.items():
        if 23 in cards:
            return pl


def isSameType(c1, c2):
    return c1 // 13 == c2 // 13


def who_collect(c1, c2, c3, c4):
    matched_cards = [c1]
    matched_cards.append(c2 if isSameType(c1, c2) else -1)
    matched_cards.append(c3 if isSameType(c1, c3) else -1)
    matched_cards.append(c4 if isSameType(c1, c4) else -1)
    return np.argmax(matched_cards)


def card_decode(n):
    shape = n // 13
    digit = n % 13
    return SHAPE_DECODE[shape] + "-" + DIGIT_DECODE[digit]


def card_encode(card):
    shape, digit = card.split("-")
    return SHAPE_ENCODE[shape] * 13 + DIGIT_ENCODE[digit]


def all_heart(cards):
    for i in range(39, 52, 1):
        if i not in cards:
            return False
    return True


def all_collected(cards):
    if all_heart(cards):
        if 8 in cards:
            if 23 in cards:
                if 35 in cards:
                    return True
    return False


def calculate_scores(player_cards):
    # TODO: implement score calculation
    return {pl: 0 for pl in range(4)}
