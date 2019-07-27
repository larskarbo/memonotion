
from firebase_admin import credentials, firestore
import firebase_admin
import requests
import json
from urllib.request import urlopen, Request
from cloudant.client import CouchDB

added = 0
updated = 0
skipped = 0
removed = 0



cred = credentials.Certificate("key.json")
app = firebase_admin.initialize_app(cred)
store = firestore.client()
tasks = store.collection("tasks")

def addTask(n_id, fields, tp):

    global updated
    global added
    global skipped

    # deck = getDeck(deckName)
    # print('ninfo: ', ninfo)
    if not len(n_id) > 0:
        print('n_id: ', n_id)
        throw("check your notion id")

    # for item in deck:
    #     if item["fields"]["notion-id"]["value"] == n_id:

    #         changeDetected = False
    #         for field in fields:
    #             if item["fields"][field]["value"] != fields[field]:
    #                 changeDetected = True

    #         if changeDetected:
    #             print('fields: ', fields)
    #             result = invoke('updateNoteFields', note={
    #                 "id": item["noteId"],
    #                 "fields": fields
    #             })
    #             updated += 1
    #             return "updated"

    #         skipped += 1
    #         return "skipped"

    note = {
        "type": tp,
        "fields": fields,
    }

    tasks.document(n_id).set(note)
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
