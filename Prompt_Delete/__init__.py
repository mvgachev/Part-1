import json

import azure.functions as func
from Player_Login.db_operations import checkIfPasswordMatchesPlayers
from Player_Registration.db_operations import checkIfUserExists

from Prompt_Delete.db_operations import deletePrompt
from Prompt_Edit.db_operations import checkIfPromptWithIdExists


def main(req: func.HttpRequest) -> func.HttpResponse:

    id = req.params.get('id')
    username = req.params.get('username')
    password = req.params.get('password')

    if not id:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            id = req_body.get('id')
            username = req_body.get('username')
            password = req_body.get('password')

    if checkIfUserExists(username) == False or checkIfPasswordMatchesPlayers(username, password) == False:
        result = False
        msg = 'bad username or password'
    elif checkIfPromptWithIdExists(id) == False:
        result = False
        msg = 'prompt id does not exist'
    else:
        deletePrompt(id)
        result = True
        msg = 'OK'

    response = {
        'result': result,
        'msg': msg
    }

    return json.dumps(response)  
