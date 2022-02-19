import logging, json

import azure.functions as func

from Player_Login.db_operations import checkIfPasswordMatchesPlayers
from Player_Registration.db_operations import checkIfUserExists


def main(req: func.HttpRequest) -> func.HttpResponse:

    username = req.params.get('username')
    password = req.params.get('password')

    if not username or not password:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            username = req_body.get('username')
            password = req_body.get('password')


    if username and password:
        if checkIfUserExists(username) == False or checkIfPasswordMatchesPlayers(username, password) == False:
            result = False
            msg = 'Username or password incorrect'
        else:
            result = True
            msg = 'OK'


    response = {
        'result': result,
        'msg': msg
    }

    return json.dumps(response)    