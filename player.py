
class Player:

    VERSION = "1.0"
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

