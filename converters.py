__author__ = 'Artem Sliusar'


def server_to_table(hand):

    """ IN: list of dicts
        OUT: ATs ..."""

    ranks = []
    suits = []
    for i in xrange(2):
        rank = hand[i]["rank"]
        suit = hand[i]["suit"]

        if rank == "10":
            rank = "T"

        ranks.append(rank)
        suits.append(suit)

    hand_converted = ranks[0] + ranks[1]
    if ranks[0] == ranks[1]:
        return hand_converted

    if suits[0] == suits[1]:
        hand_converted += "s"

    else:
        hand_converted += "o"

    return hand_converted
