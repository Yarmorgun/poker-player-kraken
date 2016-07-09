import converters
import parser



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

    VERSION = "1.1"
    NAME = "Kraken"

    def __init__(self):
        self.bet = 0
        self.risk = 1.
        self.accuracy = 1000
        self.our_player = None


    def get_preflop_probability(self, hand):
        preflop_probability_table = parser.Parser().parse_preflop("preflop.txt")
        hand_converted = converters.server_to_table(hand)
        try:
            preflop_probability = preflop_probability_table[hand_converted]
        except KeyError:
            hand_converted[0], hand_converted[1] = hand_converted[1], hand_converted[0]
            try:
                preflop_probability = preflop_probability_table[hand_converted]
            except:
                preflop_probability = 100

        return preflop_probability

    def checkBet(self):
        our_buy_in = self.our_player["current_buy_in"]
        if our_buy_in == self.our_player["bet"]:
            return 0
        else:
            return self.our_player["bet"]

    def foldBet(self):
        return 0

    def callBet(self):
        player_index = self.game_state['in_action']
        return self.game_state['current_buy_in'] - self.game_state['players'][player_index]['bet']

    def raiseBet(self):
        player_index = self.game_state['in_action']
        return self.game_state['current_buy_in'] - self.game_state['players'][player_index]['bet'] + self.game_state['minimum_raise']


    def betRequest(self, game_state):
        try:
            players_list = game_state["players"]

            for player in players_list:
                if player["name"] == Player.NAME:
                    self.our_player = player
                    break

            hand = self.our_player["hole_cards"]
            preflop_probability = self.get_preflop_probability(hand)
            if preflop_probability < 5.0:
                return self.foldBet()
            elif preflop_probability > 5.0:
                return self.checkBet()
            elif preflop_probability > 10.0:
                return self.callBet()
            elif preflop_probability > 15.0:
                return self.raiseBet()
        except:
            if self.our_player:
                our_stack = self.our_player["stack"]
                self.bet = our_stack
        finally:
            return self.bet

    def showdown(self, game_state):
        pass

