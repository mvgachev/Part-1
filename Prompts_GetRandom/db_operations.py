from azure.cosmos import CosmosClient, container
import random

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

def getPromptWithId(id: str):
    container = connectToContainer('quiplashDB', 'prompts')
    prompts = []
    for item in container.query_items(        
        query='SELECT * FROM prompts p WHERE p.id="{}"'.format(id),
        enable_cross_partition_query=True):
            prompts.append(item)
    return prompts.__getitem__(0)


def getAllPromptIds():
    container = connectToContainer('quiplashDB', 'prompts')
    prompt_ids = []
    for item in container.query_items(        
            query='SELECT * FROM prompts',
            enable_cross_partition_query=True):
                prompt_ids.append(int(item['id']))
    return prompt_ids

def getAllPrompts():
    container = connectToContainer('quiplashDB', 'prompts')
    prompts = []
    for item in container.query_items(        
            query='SELECT * FROM prompts',
            enable_cross_partition_query=True):
                prompts.append(item)
    return prompts

def getNRandomPrompts(n: int):
    allPrompts = getAllPromptIds()
    output = []

    if n <= len(allPrompts):
        random_ids = random.sample(allPrompts, n)
        for id in random_ids:
            output.append(getPromptWithId(id))
    else:
        output = getAllPrompts()

    return output
