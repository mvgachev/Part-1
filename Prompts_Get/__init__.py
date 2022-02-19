import json

import azure.functions as func

from Prompts_Get.db_operations import getAllPrompts, getAllPromptsWithUsernames


def main(req: func.HttpRequest) -> func.HttpResponse:

    players = req.params.get('players')
    urlInput = True

    if not players:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            players = req_body.get('players')
            urlInput = False

    if players == '-1':
        response = getAllPrompts()
    else:
        if urlInput == True:
            players = players.split(',')
        response = getAllPromptsWithUsernames(players)

    return json.dumps(response)    
