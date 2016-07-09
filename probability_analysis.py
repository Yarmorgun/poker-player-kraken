import numpy as np
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
        count_Straight          = 0
        StraightIdx             = 0
        is_Three_of_a_Kind      = False
        Three_of_a_Kind_idx     = 0
        is_One_pair             = False
        One_pair_idx            = 0
        two_pair_idx            = 0
        is_two_pair             = False
        Kicker                  = 0
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
                is_Three_of_a_Kind = True
                Three_of_a_Kind_idx = idx
            if(count==2):
                if is_One_pair:
                    is_two_pair  = True
                    two_pair_idx = idx
                    if idx < One_pair_idx:
                        two_pair_idx = One_pair_idx
                is_One_pair = True
                One_pair_idx = idx
            if(count>0):
                count_Straight = count_Straight + 1
            elif count==0:
                if count_Straight<5:
                    count_Straight = 0
                if    StraightIdx == 0:
                    StraightIdx = idx-1

        if(is_Three_of_a_Kind and is_One_pair):
            return [Full_House, Three_of_a_Kind_idx]

        if(count_Straight>=5):
            return [Straight, StraightIdx]

        if(is_Three_of_a_Kind):
            return [Three_of_a_Kind , Three_of_a_Kind_idx]

        if(is_two_pair):
            return [Two_pair,two_pair_idx]

        if(is_One_pair):
            return [One_pair,One_pair_idx]

        return [0,Kicker]

