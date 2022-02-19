from azure.cosmos import CosmosClient, container
import uuid

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


def getAllPrompts():
    container = connectToContainer('quiplashDB', 'prompts')
    prompts = []
    for item in container.query_items(        
            query='SELECT * FROM prompts',
            enable_cross_partition_query=True):
                out_item = {
                    'id': item['id'],
                    'text': item['text'],
                    'username': item['username']
                }
                prompts.append(out_item)
    return prompts
 
def getAllPromptsWithUsernames(usernames: list):
    container = connectToContainer('quiplashDB', 'prompts')
    prompts = []
    for username in usernames:
        for item in container.query_items(        
            query='SELECT * FROM prompts p WHERE p.username="{}"'.format(username),
            enable_cross_partition_query=True):
                prompts.append(item)
    return prompts





