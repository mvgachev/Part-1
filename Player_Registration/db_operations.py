import logging
from azure.cosmos import CosmosClient, container
import uuid

player = {
    'id': '0',
    'username': 'username',
    'password': 'password',
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

def getPlayerWithUsername(username: str):
    container = connectToContainer('quiplashDB', 'players')
    players = []
    for item in container.query_items(        
        query='SELECT * FROM players p WHERE p.username="{}"'.format(username),
        enable_cross_partition_query=True):
            players.append(item)
    return players

def checkIfUserExists(username: str):
    return len(getPlayerWithUsername(username)) == 1


def addPlayer(username: str, password: str):
    container = connectToContainer('quiplashDB', 'players')
    
    player['id'] = str(uuid.uuid4())
    player['username'] = username
    player['password'] = password
    return container.upsert_item(player)


