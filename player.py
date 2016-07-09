

// test bot logic
def bot_logic(game_state):

	// todo: need parsing game_state: is_someone_allin(), is_someone_rise(), get_active_players(), get_all_money_in_game()
	// todo: get_probabillity()
	// todo: 
	fold = 0
	someone_allin = true # is_someone_allin()
	noone_rise = false # is_someone_rise()
	active_player_count = # get_active_players()
	our_probabillity_to_win = get_probabillity()
	current_pot = get_all_money_in_game()
	if someone_allin:
		if is_good_chance_to_win():
			return all_in
		else
			return fold
	elif noone_rise:
		return big_blind * 3
	else:
		amount_to_call = get_max_rise();
		if is_probabillity_good_to_play():
			return amount_to_call
	
	
	

class Player:

    VERSION = "1.1"
    NAME = "Kraken"

    def __init__(self):
        self.bet = 0
        self.risk = 1.
        self.accuracy = 1000
        self.our_player = None

    def betRequest(self, game_state):
        players_list = game_state["players"]

        for player in players_list:
            if player["name"] == Player.NAME:
                self.our_player = player
                break

        if self.our_player:
            our_stack = self.our_player["stack"]
            self.bet = our_stack
        print self.bet
        return self.bet

    def showdown(self, game_state):
        pass

