import logging
import json
import azure.functions as func

from Player_Leaderboard.db_operations import getTopPlayers


def main(req: func.HttpRequest) -> func.HttpResponse:

    top = req.params.get('top')
    if not top:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            top = req_body.get('top')

       
    if top:
        top = int(top)
        if top < 0:
            output = 'The top value should be positive.'
        else:
            output = getTopPlayers(top)
    else:
        output = 'The top value is missing.'

    return json.dumps(output)
