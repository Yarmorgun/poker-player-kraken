import converters
import parser
import sys
import json


# // test bot logic
def bot_logic(game_state):
    return 0


# // todo: need parsing game_state: is_someone_allin(), is_someone_rise(), get_active_players(), get_all_money_in_game()
# // todo: get_probabillity()
# // todo:
# fold = 0
# someone_allin = True # is_someone_allin()
# noone_rise = False # is_someone_rise()
# active_player_count = # get_active_players()
# our_probabillity_to_win = get_probabillity()
# current_pot = get_all_money_in_game()
# if someone_allin:
# 	if is_good_chance_to_win():
# 		return all_in
# 	else
# 		return fold
# elif noone_rise:
# 	return big_blind * 3
# else:
# 	amount_to_call = get_max_rise();
# 	if is_probabillity_good_to_play():
# 		return amount_to_call




class Player:
    VERSION = "1.5"
    NAME = "Kraken"

    def __init__(self):
        self.bet = 0
        self.risk = 1.
        self.accuracy = 1000
        self.active_players = 0
        self.our_player = None

    def get_preflop_probability(self, hand, players_count):
        preflop_probability_table = parser.Parser().parse_preflop("preflop.txt")
        hand_converted = converters.server_to_table(hand)
        print "HAND_CONVERTED:", hand_converted
        try:
            preflop_probability = preflop_probability_table[hand_converted][players_count - 1]
        except:
            print "START_CONVERTING"
            hand_converted_2 = hand_converted[1] + hand_converted[0]
            if len(hand_converted) == 3:
                hand_converted_2 += hand_converted[2]
            print
            "HAND_CONVERTED_2:", hand_converted_2
            try:
                preflop_probability = preflop_probability_table[hand_converted_2][players_count - 1]
            except:
                preflop_probability = 100

        print "PREFLOP_PROB_EXIT"
        return preflop_probability

    def checkBet(self):
        print >> sys.stderr, "CHECK_BET"
        current_buy_in = self.game_state["current_buy_in"]
        if current_buy_in == self.our_player["bet"]:
            self.bet = 0
        else:
            self.bet = self.our_player["bet"]

    def foldBet(self):
        print >> sys.stderr, "FOLD_BET"
        self.bet = 0

    def callBet(self):
        print >> sys.stderr, "CALL_BET"
        self.bet = self.game_state['current_buy_in'] - self.our_player['bet']

    def raiseBet(self):
        print >> sys.stderr, "RAISE_BET"
        self.bet = self.game_state['current_buy_in'] - self.our_player['bet'] + self.game_state['minimum_raise']

    def all_in(self):
        print >> sys.stderr, "ALL_IN"
        if self.our_player:
            our_stack = self.our_player["stack"]
            self.bet = our_stack
            return self.bet

    def maxStack(self):
        players_list = self.game_state["players"]
        maxStack = 0
        for pl in players_list:
            if pl["status"] == "active" and pl["name"] != Player.NAME:
                if pl["stack"] > maxStack:
                    maxStack = pl["stack"]

        return maxStack

    def betRequest(self, game_state):
        self.game_state = game_state

        try:
            players_list = game_state["players"]
            for pl in players_list:
                if pl["status"] == "active":
                    self.active_players += 1

            for player in players_list:
                if player["name"] == Player.NAME:
                    self.our_player = player
                    break

            print "ACTIVE PLAYERS: ", self.active_players
            hand = self.our_player["hole_cards"]
            preflop_probability = self.get_preflop_probability(hand, self.active_players)


            tmphand = []
            lastProb = 0
            if len(game_state["community_cards"]) > 0:
                for cardOne in hand:
                    for cardTwo in game_state["community_cards"]:
                        tmphand = [cardOne, cardTwo]
                        preflop_probability = self.get_preflop_probability(tmphand, self.active_players)
                        if (preflop_probability > lastProb):
                            lastProb = preflop_probability
                preflop_probability = lastProb
            else:
                preflop_probability = self.get_preflop_probability(hand, self.active_players)




            print >> sys.stderr, "HAND:", hand, "PROBABILITY: " + str(preflop_probability)
            if preflop_probability < 35.0:
                self.foldBet()
            # elif preflop_probability >= 35.0 and preflop_probability < 37.0:
            #     self.checkBet()
            elif preflop_probability >= 37.0 and preflop_probability < 50.0:
                self.callBet()
            elif preflop_probability > 50.0:
                maxUsersStack = self.maxStack()
                if maxUsersStack != 0 and maxUsersStack < self.our_player["stack"]:
                    self.all_in()
                else:
                    self.raiseBet()
            elif preflop_probability == 100:
                self.all_in()
        except Exception as e:
            print >> sys.stderr, "MAIN EXCEPTION: ", e.message
            self.all_in()
        finally:
            print "FINAL_BET:", self.bet
            return self.bet

    def showdown(self, game_state):
        pass


# pl = Player()
# data = {
#     "tournament_id":"550d1d68cd7bd10003000003",
#     "game_id":"550da1cb2d909006e90004b1",
#     "round":0,
#     "bet_index":0,
#     "small_blind": 10,
#     "current_buy_in": 320,
#     "pot": 400,
#     "minimum_raise": 240,
#     "dealer": 1,
#     "orbits": 7,
#     "in_action": 1,
#     "players": [
#         {
#             "id": 0,
#             "name": "bob",
#             "status": "active",
#             "version": "Default random player",
#             "stack": 1010,
#             "bet": 320
#         },
#         {
#             "id": 1,
#             "name": "Kraken",
#             "status": "active",
#             "version": "Default random player",
#             "stack": 1590,
#             "bet": 80,
#             "hole_cards": [
#                 {
#                     "rank": "6",
#                     "suit": "hearts"
#                 },
#                 {
#                     "rank": "K",
#                     "suit": "spades"
#                 }
#             ]
#         },
#         {
#             "id": 2,
#             "name": "Chuck",
#             "status": "out",
#             "version": "Default random player",
#             "stack": 0,
#             "bet": 0
#         }
#     ],
#     "community_cards": [
#         {
#             "rank": "4",
#             "suit": "spades"
#         },
#         {
#             "rank": "A",
#             "suit": "hearts"
#         },
#         {
#             "rank": "6",
#             "suit": "clubs"
#         }
#     ]
# }
# json_data = json.dumps(data)
# json_msg = json.loads(json_data)
# pl.betRequest(json_msg)
