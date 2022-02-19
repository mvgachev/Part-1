import logging
import json

import azure.functions as func

from Prompts_GetRandom.db_operations import getNRandomPrompts


def main(req: func.HttpRequest) -> func.HttpResponse:
    
    n = req.params.get('n')
    if not n:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            n = req_body.get('n')

    if n:
        n = int(n)

    return json.dumps(getNRandomPrompts(n))

