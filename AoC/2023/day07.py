data = """"""


cards = "A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2".split(", ")
p2_cards = "A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J".split(", ")

p2 = False

from collections import Counter


def convert_hand(hand):
    if p2:
        return "".join([chr(p2_cards.index(i)) for i in hand])
    return "".join([chr(cards.index(i)) for i in hand])


def worker(hand: str):
    counter = Counter(hand)

    hand = convert_hand(hand)

    two_pair = 0
    three_pair = 0
    j_pair = counter["J"]

    for key, value in counter.most_common():
        if p2 and key == "J":
            if value == 5:
                return "1" + hand
            continue

        if value == 5 or (p2 and value + j_pair == 5):
            return "1" + hand
        elif value == 4 or (p2 and value + j_pair >= 4):
            return "2" + hand
        elif value == 3 or (p2 and value + j_pair >= 3):
            three_pair += 1
            j_pair -= 3 - value
        elif value == 2 or ((p2 and value + j_pair >= 2)):
            two_pair += 1
            j_pair -= 2 - value

    if three_pair == 1 and two_pair == 1:
        return "3" + hand
    if three_pair == 1 and two_pair == 0:
        return "4" + hand
    if two_pair == 2:
        return "5" + hand
    if two_pair == 1:
        return "6" + hand
    return "7" + hand


options = {i.split(" ")[0]: int(i.split(" ")[1]) for i in data.split("\n")}

print(sum(options[i] * x for x, i in enumerate(sorted(options, key=worker, reverse=True), 1)))

p2 = True

print(sum(options[i] * x for x, i in enumerate(sorted(options, key=worker, reverse=True), 1)))
