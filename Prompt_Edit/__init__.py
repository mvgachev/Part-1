import json

import azure.functions as func
from Player_Login.db_operations import checkIfPasswordMatchesPlayers
from Player_Registration.db_operations import checkIfUserExists
from Prompt_Create.db_operations import checkIfPromptForUserWithTextExists

from Prompt_Edit.db_operations import checkIfPromptWithIdExists, editPrompt


def main(req: func.HttpRequest) -> func.HttpResponse:

    id = req.params.get('id')
    text = req.params.get('text')
    username = req.params.get('username')
    password = req.params.get('password')



    if not id or not text:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            id = req_body.get('id')
            text = req_body.get('text')
            username = req_body.get('username')
            password = req_body.get('password')

    if checkIfUserExists(username) == False or checkIfPasswordMatchesPlayers(username, password) == False:
        result = False
        msg = 'bad username or password'
    elif len(text) < 10:
        result = False
        msg = 'prompt is less than 10 characters'
    elif len(text) > 100:
        result = False
        msg = 'prompt is more than 100 characters'
    elif checkIfPromptWithIdExists(id) == False:
        result = False
        msg = 'prompt id does not exist'
    elif checkIfPromptForUserWithTextExists(username, text):
        result = False
        msg = 'user already has a prompt with the same text'
    else:
        editPrompt(id, text)
        result = True
        msg = 'OK'

    response = {
        'result': result,
        'msg': msg
    }

    return json.dumps(response)    
