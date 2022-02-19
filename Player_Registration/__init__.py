import logging
import json
from Player_Registration import db_operations as dbo

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

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
        if len(username) < 4:
            result = False
            msg = 'Username less than 4 characters'
        elif len(username) > 16:
            result = False
            msg = 'Username more than 16 characters'
        elif len(password) < 8:
            result = False
            msg = 'Password less than 8 characters'
        elif len(password) > 24:
            result = False
            msg = 'Password more than 24 characters'
        elif dbo.checkIfUserExists(username):
            result = False
            msg = 'Username already exists'
        else:
            dbo.addPlayer(username, password)
            result = True
            msg = 'OK'

    response = {
        'result': result,
        'msg': msg
    }

    return json.dumps(response)
