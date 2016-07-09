import converters
import parser
import sys
import probability_analysis as pa
import game_state_parser as gsp
import json

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
        try:
            preflop_probability = preflop_probability_table[hand_converted][players_count-1]
        except KeyError:
            hand_converted[0], hand_converted[1] = hand_converted[1], hand_converted[0]
            try:
                preflop_probability = preflop_probability_table[hand_converted][players_count-1]
            except:
                preflop_probability = 100

        return preflop_probability

    def checkBet(self):
        print >> sys.stderr, "checkBet"
        current_buy_in = self.game_state["current_buy_in"]
        if current_buy_in == self.our_player["bet"]:
            self.bet = 0
        else:
            self.bet = self.our_player["bet"]

    def foldBet(self):
        print >> sys.stderr, "foldBet"
        self.bet = 0

    def callBet(self):
        print >> sys.stderr, "callBet"
        self.bet = self.game_state['current_buy_in'] - self.our_player['bet']
        print "BET_CALL:", self.bet

    def raiseBet(self):
        print >> sys.stderr, "raiseBet"
        self.bet = self.game_state['current_buy_in'] - self.our_player['bet'] + self.game_state['minimum_raise']

    def all_in(self):
        print >> sys.stderr, "allIn"
        if self.our_player:
            our_stack = self.our_player["stack"]
            self.bet = our_stack
            return self.bet

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

            hand = self.our_player["hole_cards"]
            #preflop_probability = self.get_preflop_probability(hand, self.active_players)
            preflop_probability = 0.0
            preflop_probability = pa.getProbability(self.active_players, 1000, converters.server_to_propobility_gen(hand),
                                                    converters.server_to_propobility_gen(game_state["community_cards"]))
            print >> sys.stderr, "HAND:", hand, "preflop probability: " + str(preflop_probability)
            if preflop_probability < 16.0:
                self.foldBet()
            elif preflop_probability >= 16.0 and preflop_probability < 36:
                self.checkBet()
            elif preflop_probability >= 36 and preflop_probability < 50:
                self.callBet()
            elif preflop_probability > 50.0:
                self.raiseBet()
            elif preflop_probability >= 80:
                self.all_in()
        except Exception as e:
            print >> sys.stderr, "MAIN EXCEPTION: ", e.message
            self.all_in()
        finally:
            print self.bet
            return self.bet

    def showdown(self, game_state):
        pass

# EXAMPLE TEST bet
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