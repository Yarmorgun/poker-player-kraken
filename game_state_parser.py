def get_active_players(game_state):
    players_list = game_state["players"]
    count = 0
    for player in players_list:
        if player["status"] == "active":
            count += 1

    return  count

def is_someone_allin(game_state):
    players_list = game_state["players"]
    count = 0
    for player in players_list:
        if player["status"] == "active" and player["stack"] == player["bet"]:
            return True

    return False

def is_someone_raise(game_state):
    players_list = game_state["players"]
    count = 0
    for player in players_list:
        if player["status"] == "active" and game_state["blind"] < player["bet"]:
            return True

    return False