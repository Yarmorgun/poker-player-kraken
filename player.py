import converters
import parser
import sys


# // test bot logic
def bot_logic(game_state):
    return 0
	# // todo: need parsing game_state: is_someone_allin(), is_someone_rise(), get_active_players(), get_all_money_in_game()
	# // todo: get_probabillity()
	# // todo:
	#fold = 0
	#someone_allin = True # is_someone_allin()
	#noone_rise = False # is_someone_rise()
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

    VERSION = "1.4"
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
        player_index = self.game_state['in_action']
        print "player_index: ", player_index
        self.bet = self.game_state['current_buy_in'] - self.game_state['players'][player_index]['bet']
        print "BET_CALL:", self.bet

    def raiseBet(self):
        print >> sys.stderr, "raiseBet"
        player_index = self.game_state['in_action']
        self.bet = self.game_state['current_buy_in'] - self.game_state['players'][player_index]['bet'] + self.game_state['minimum_raise']

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
            preflop_probability = self.get_preflop_probability(hand, self.active_players)
            print >> sys.stderr, "HAND:", hand, "preflop probability: " + str(preflop_probability)
            if preflop_probability < 5.0:
                self.foldBet()
            elif preflop_probability >= 5.0 and preflop_probability < 10.0:
                self.checkBet()
            elif preflop_probability >= 10.0 and preflop_probability < 15.0:
                self.callBet()
            elif preflop_probability > 15.0:
                self.raiseBet()
            elif preflop_probability == 100:
                self.all_in()
        except Exception as e:
            print >> sys.stderr, "MAIN EXCEPTION: ", e.message
            self.all_in()
        finally:
            print self.bet
            return self.bet

    def showdown(self, game_state):
        pass

