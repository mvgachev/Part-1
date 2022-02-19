import logging
from azure.cosmos import CosmosClient

from Player_Registration.db_operations import getPlayerWithUsername

updatedPlayer = {
    'id': '0',
    'username': 'username',
    'games_played': 0,
    'total_score': 0
}

def connectToClient():
    ACCOUNT_URI = 'https://quiplash-db.documents.azure.com:443/'
    ACCOUNT_KEY = 'VhRMquRsPTGLdGcGhSsDkqmebqPRqxWtdh0HodaToPz3tEPxh85rveN9O1Br0yPST1b7Fnv9hhnYcAaly5jDgg=='
    client = CosmosClient(ACCOUNT_URI, credential=ACCOUNT_KEY)
    return client


def connectToContainer(database_name, container_name):
    client = connectToClient()
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    return container

def getPlayerIdFromUsername(username):
    player = getPlayerWithUsername(username).__getitem__(0)
    return player['id']

def updatePlayer(username: str, add_to_games_played: int, add_to_score: int):
    container = connectToContainer('quiplashDB', 'players')

    id = getPlayerIdFromUsername(username)
    player = getPlayerWithUsername(username).__getitem__(0)

    player['games_played'] = player['games_played'] + int(add_to_games_played)
    player['total_score'] = player['total_score'] + int(add_to_score)
    container.replace_item(item=id, body=player)
    logging.info('The edited player now: "{}"'.format(player))

