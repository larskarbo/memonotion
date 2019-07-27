
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

def yo(deck):
    # res = invoke("guiBrowse", query=("deck:"+deck))
    res = invoke("guiCurrentCard")
    print('res: ', res)

def addNote(fields, deckName, model):

    global updated
    global added
    global skipped

    deck = getDeck(deckName)
    # print('ninfo: ', ninfo)
    n_id = fields["notion-id"]
    if not len(n_id) > 0:
        print('n_id: ', n_id)
        throw("check your notion id")
    for item in deck:
        if item["fields"]["notion-id"]["value"] == n_id:

            changeDetected = False
            for field in fields:
                if item["fields"][field]["value"] != fields[field]:
                    changeDetected = True
            

            if changeDetected:
                print('fields: ', fields)
                result = invoke('updateNoteFields', note={
                    "id": item["noteId"],
                    "fields": fields
                })
                updated += 1
                return "updated"
            
            skipped += 1
            return "skipped"

    note = {
        "deckName": deckName,
        "modelName": model,
        "fields": fields,
        "options": {
            "allowDuplicate": True
        },
        "tags": [],
        "id": n_id
    }
    result = invoke('addNote', note=note)
    added += 1
    return "added"


def getDeck(deck):
    yo = invoke("findNotes", query=("deck:"+deck))
    ninfo = invoke("notesInfo", notes=yo)
    return ninfo


def getDeckCards(deck):
    yo = invoke("findCards", query=("deck:"+deck))
    cinfo = invoke("cardsInfo", cards=yo)
    return cinfo


def moveToTrash(cardId):
    global removed
    susp = invoke("areSuspended", cards=[cardId])[0]
    if susp:
        return
    yo = invoke("suspend", cards=[cardId])
    removed += 1

def printStats():
    print("")
    print("Updated: ", updated)
    print("Added: ", added)
    print("Skipped: ", skipped)
    print("Removed: ", removed)
