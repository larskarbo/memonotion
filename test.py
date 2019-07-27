
import requests
import json
from urllib.request import urlopen, Request


added = 0
updated = 0
skipped = 0
removed = 0


def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}


def invoke(action, **params):
    requestJson = json.dumps(request(action, **params))
    response = requests.post("http://localhost:8765", data=requestJson).json()
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

def hi():
    cards = invoke("findCards", query="deck:all")
    # info = invoke("cardsInfo", cards=cards)
    due = invoke("areDue", cards=cards)
    
    for i, e in enumerate(due):
        if e:
            info = invoke("cardsInfo", cards=[cards[i]])[0]
            print('info: ', info)


hi()
