__author__ = 'Artem Sliusar'

#suits idx
heart             = 0
diamond           = 1
club              = 2
spade             = 3

# ranks idx
Two     =   0
Three   =   1
Four    =   2
Five    =   3
Six     =   4
Seven   =   5
Eight   =   6
Nine    =   7
Ten     =   8
Jack    =   9
Queen   =   10
King    =   11
Ace     =   12

# combinations idx
Royal_F         = 9
Straight_F      = 8
Four_of_K       = 7
Full_House      = 6
Flash           = 5
Straight        = 4
Three_of_a_Kind = 3
Two_pair        = 2
One_pair        = 1


convertDictRanks =   {
                      "2":Two,
                      "3":Three,
                      "4":Four,
                      "5":Five,
                      "6":Six,
                      "7":Seven,
                      "8":Eight,
                      "9":Nine,
                      "10":Ten,
                      "J" :Jack,
                      "Q" :Queen,
                      "K" :King,
                      "A" :Ace
                            }


convertDictRanks =   {
                      "2":Two,
                      "3":Three,
                      "4":Four,
                      "5":Five,
                      "6":Six,
                      "7":Seven,
                      "8":Eight,
                      "9":Nine,
                      "10":Ten,
                      "J" :Jack,
                      "Q" :Queen,
                      "K" :King,
                      "A" :Ace
                            }
converDictSuit = {
                      "hearts":heart,
                      "spades":spade,
                      "clubs":club,
                      "diamonds":diamond
                }

def server_to_propobility_gen(card_list):
    resList = []
    for card in card_list:
        a = tuple
        a = (converDictSuit[card["suit"]],convertDictRanks[card["rank"]])
        resList.append(a)
    return resList


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
