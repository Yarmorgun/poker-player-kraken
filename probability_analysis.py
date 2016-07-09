import sys
g_numpy_ok = False
# try:
#     import numpy as np
#     g_numpy_ok = True
# except ImportError:
#     sys.stdout.write('numpy not exist')
import numpy as np
import random
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

#suits idx
heart             = 0
diamond           = 1
club              = 2
spade             = 3



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

# card_test  = np.array[int(0)*52]
# card_test.shape(4,13)
class Combinator:

    def __init__(self, card_deck):
        self.Card_deck = card_deck

    #get combinations from Card_deck
    def getCombination(self):
        combinationIdx = []
        #combinationIdx = self.Royal_Flush()
        #if combinationIdx[0] > 0:
            #return combinationIdx
        combinationIdx = self.Straight_Flush_and_Flush()
        if combinationIdx[0] > 0:
            return combinationIdx
        combinationIdx = self.Else_Combination()
        if combinationIdx[0] > 0:
            return combinationIdx
        return combinationIdx

    # check for Royal Flush
    def Royal_Flush(self):
        found = True
        pass

    # check for Straight Flush and Flush
    def Straight_Flush_and_Flush(self):
        count_Straight_F = 0
        count_flash      = 0
        for suitCardList in range(heart, spade+1):
            count_Straight_F = 0
            count_flash      = 0
            for idx in range(Two,Ace+1):
                if self.Card_deck[suitCardList][idx] == 0 :
                    count_Straight_F = 0
                    continue
                count_Straight_F    = count_Straight_F + 1
                count_flash         = count_flash      + 1
                if( count_Straight_F >=5):
                    return [Straight_F , idx]
                if( count_flash >=5):
                    return [Flash , idx]
        return [0,0]

    # check for pair, two pairs, full house, Straight , Three_of_a_Kind
    def Else_Combination(self):
        Three_of_a_Kind      = False
        _idx_Three_of_a_Kind    = 0
        One_pair             = False
        One_pair_idx            = 0
        two_pair_idx            = 0
        two_pair             = False
        Kicker                  = 0

        _Straight_count          = 0
        IdxStraight             = 0
        for idx in range(Two,Ace+1):
            count = 0
            for suitCardList in range(heart, spade+1):
                if self.Card_deck[suitCardList][idx] == 0 :
                    continue
                count += 1
                if(Kicker< idx):
                    Kicker = idx

            if(count==4):
                return [Four_of_K,idx]

            if(count==3):
                Three_of_a_Kind = True
                _idx_Three_of_a_Kind = idx
                
            if(count==2):
                if One_pair:
                    two_pair  = True
                    two_pair_idx = idx
                    if idx < One_pair_idx:
                        two_pair_idx = One_pair_idx
                One_pair = True
                One_pair_idx = idx
            if(count>0):
                _Straight_count = _Straight_count + 1
            elif count==0:
                if _Straight_count<5:
                    _Straight_count = 0
                if    IdxStraight == 0:
                    IdxStraight = idx-1

        if(Three_of_a_Kind and One_pair):
            return [Full_House, _idx_Three_of_a_Kind]

        if(_Straight_count>=5):
            return [Straight, IdxStraight]

        if(Three_of_a_Kind):
            return [Three_of_a_Kind , _idx_Three_of_a_Kind]

        if(two_pair):
            return [Two_pair,two_pair_idx]

        if(One_pair):
            return [One_pair,One_pair_idx]

        return [0,Kicker]


class CardWorker:
    def __init__(self):
        #base array for cards
        self.Card_deck = np.array([int(0)]*52)
        self.Card_deck.shape = (4, 13)

        #array for cards, needed for generate unique cards
        self.Memory_deck = np.array([int(0)]*52)
        self.Memory_deck.shape = (4, 13)

    # mark that card is already used
    def putCard_to_mamemory(self, a):
        self.Memory_deck[a] = 1

    # clear all card
    def clearMemory(self):
        self.Memory_deck.fill(0)

    #clear all card in game
    def clearCard_deck(self):
        self.Card_deck.fill(0)

    # set card in deck , in which will be checked combination
    def setCard(self, a):
        self.Card_deck[a] = 1

    # take out from deck , in which will be checked combination
    def un_setCard(self, a):
        self.Card_deck[a] = 0

    # generate random card
    def genCards(self, count):
        i = 0
        cardList = []
        while(i!=count):
            rang = random.randint(Two,Ace)
            suit = random.randint(heart,spade)
            if(self.Memory_deck[suit][rang]!=0):
                continue
            i = i + 1
            cardList.append((suit,rang))
            self.Memory_deck[suit][rang] = 1
        return cardList



# get probability
def getProbability(countOfPlayers, distrib, myPair, existOnTable):
    # if g_numpy_ok:
    cw_obj = CardWorker()
    comb_obj = Combinator(cw_obj.Card_deck)

    remaining_number    = 5 - len(existOnTable)
    countOurWins  = 0
    genCardCount        = remaining_number

    for test_i in range(0, distrib+1):

        for card in existOnTable:
            cw_obj.putCard_to_mamemory(card)  # put in array
            cw_obj.setCard(card)
        for card in myPair:
            cw_obj.putCard_to_mamemory(card)
            cw_obj.un_setCard(card)

        BestRaundScore = [0, 0]
        BestRaundScore[0] = 0
        BestRaundScore[1] = 0

        playerCardList = []  # cards on hand for other players
        for player_i in range(0,countOfPlayers):
            player_i_cards =  cw_obj.genCards(2)
            playerCardList.append(player_i_cards)
            for card in player_i_cards:
                cw_obj.putCard_to_mamemory(card)

        onTableCards = cw_obj.genCards(genCardCount)
        for card in onTableCards:
            cw_obj.putCard_to_mamemory(card)#
            cw_obj.setCard(card)

        # get combinations for players
        for player_i in range(0,countOfPlayers):

            for card in playerCardList[player_i]:
                cw_obj.setCard(card)

            res = comb_obj.getCombination()
            if(BestRaundScore[0] < res[0]):
                BestRaundScore = res
            elif(BestRaundScore[0] == res[0]):
                if BestRaundScore[1] < res[1]:
                    BestRaundScore[1] = res[1]

            for card in playerCardList[player_i]:
                cw_obj.un_setCard(card)

        # get combination for myself
        for card in myPair:
            cw_obj.setCard(card)
        res = comb_obj.getCombination()
        if BestRaundScore[0] < res[0]:
            countOurWins = countOurWins + 1

        elif BestRaundScore[0] == res[0]:
            if BestRaundScore[1] < res[1]:
                countOurWins = countOurWins + 1

        cw_obj.clearCard_deck()
        cw_obj.clearMemory()
    return (float(countOurWins) / distrib) * 100
    # else:
    #     return 1
