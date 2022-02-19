import logging

import azure.functions as func
from Player_Login.db_operations import checkIfPasswordMatchesPlayers
from Player_Registration.db_operations import checkIfUserExists

from Prompt_Create.db_operations import checkIfPromptForUserWithTextExists, createPrompt

import json


def main(req: func.HttpRequest) -> func.HttpResponse:

    text = req.params.get('text')
    username = req.params.get('username')
    password = req.params.get('password')

    if not text or not username:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            text = req_body.get('text')
            username = req_body.get('username')
            password = req_body.get('password')


    if len(text) < 10:
        result = False
        msg = 'prompt is less than 10 characters'
    elif len(text) > 100:
        result = False
        msg = 'prompt is more than 100 characters'
    elif checkIfUserExists(username) == False or checkIfPasswordMatchesPlayers(username, password) == False:
        result = False
        msg = 'bad username or password'
    elif checkIfPromptForUserWithTextExists(username, text) == True:
        result = False
        msg = 'User already has a prompt with the same text'
    else:
        createPrompt(text, username)
        result = True
        msg = 'OK'

    response = {
        'result': result,
        'msg': msg
    }

    return json.dumps(response)
