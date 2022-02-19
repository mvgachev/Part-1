import logging
from azure.cosmos import CosmosClient, container

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

def getTopPlayers(top: int):
    container = connectToContainer('quiplashDB', 'players')
    players = []
    for item in container.query_items(        
        query='SELECT * FROM players p ORDER BY p.total_score DESC OFFSET 0 LIMIT 1'.format(top),
        enable_cross_partition_query=True):
            players.append(item)
    return players


