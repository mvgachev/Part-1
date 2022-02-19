from azure.cosmos import CosmosClient

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

def getPromptsWithText(username: str, text: str):
    container = connectToContainer('quiplashDB', 'prompts')
    prompts = []
    for item in container.query_items(        
        query='SELECT * FROM prompts p WHERE p.username="{}" AND p.text="{}"'.format(username, text),
        enable_cross_partition_query=True):
            prompts.append(item)
    return prompts


def checkIfPromptForUserWithTextExists(username: str, text: str):
    return len(getPromptsWithText(username, text)) == 1

def generateId():
    container = connectToContainer('quiplashDB', 'prompts')
    items = []
    for item in container.query_items(        
        query='SELECT * FROM prompts p ORDER BY p.id DESC OFFSET 0 LIMIT 1',
        enable_cross_partition_query=True):
        items.append(item)
    if len(items) != 0:
        last_item = items.__getitem__(0)
        last_id = int(last_item['id'])
        new_id = last_id + 1
    else:
        new_id = 1
    return new_id

    
def createPrompt(text:str, username: str):
    container = connectToContainer('quiplashDB', 'prompts')

    prompt = {
        'id': str(generateId()),
        'text': text,
        'username': username
    }

    container.upsert_item(prompt)




