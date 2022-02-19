import json


import azure.functions as func
from Player_Login.db_operations import checkIfPasswordMatchesPlayers
from Player_Registration.db_operations import checkIfUserExists

from Player_Update.db_operations import updatePlayer


def main(req: func.HttpRequest) -> func.HttpResponse:

    username = req.params.get('username')
    password = req.params.get('password')
    add_to_games_played = req.params.get('add_to_games_played')
    add_to_score = req.params.get('add_to_score')

    if not username:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            username = req_body.get('username')
            password = req_body.get('password')
            add_to_games_played = req_body.get('add_to_games_played')
            add_to_score = req_body.get('add_to_score')

    if add_to_games_played:
        add_to_games_played = int(add_to_games_played)
    if add_to_score:
        add_to_score = int(add_to_score)

    if username and password:
        if checkIfUserExists(username):
            
            if checkIfPasswordMatchesPlayers(username, password):
                if add_to_games_played < 0 or add_to_score < 0:
                    result = False
                    msg = 'Attempt to set negative score/games_played'
                else:
                    if not add_to_games_played:
                        add_to_games_played = 0

                    if not add_to_score:
                        add_to_score = 0

                    updatePlayer(username, add_to_games_played, add_to_score)
                    result = True
                    msg = 'OK'
            else:
                result = False
                msg = 'wrong password'
        else:
            result = False
            msg = 'user does not exist'


    response = {
        'result': result,
        'msg': msg
    }

    return json.dumps(response)

