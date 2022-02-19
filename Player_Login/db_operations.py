from Player_Registration.db_operations import getPlayerWithUsername

def checkIfPasswordMatchesPlayers(username: str, password: str):
    player = getPlayerWithUsername(username).__getitem__(0)
    return player['password'] == password
        
    



