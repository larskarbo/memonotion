
import json
from cloudant.client import CouchDB
import os

added = 0
updated = 0
skipped = 0
removed = 0


client = CouchDB('admin', os.environ['UDOS_PASSWORD'], url='http://104.248.32.243:5984', connect=True)
session = client.session()
print('Username: {0}'.format(session['userCtx']['name']))
print('Databases: {0}'.format(client.all_dbs()))

db = client.create_database('udos')

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
        "type": 'task',
        "tag": tp,
        "fields": fields,
    }

    # Create a document using the Database API
    if n_id in db:
        # update id
        doc = db[n_id]
        doc['type'] = tp
        doc['fields'] = fields
        doc.save()
        updated +=1

        
    else:
        doc = db.create_document(note)
        added += 1



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
