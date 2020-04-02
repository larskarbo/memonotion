
import json
import os
import sys

# os.environ["PARSE_API_ROOT"] = "https://pg-app-3mjkbjxesqq7ejfiys8ahzyqiycdhc.scalabl.cloud/1"
# APPLICATION_ID = 'gRVOPbmAuYHBC3ZK4nvA8tA85OEN3doQEMQdrV3E'
# REST_API_KEY = '6ejWpvzOydYfTGqsatUtfkLKdCEdQ8NQK5bM3WrE'
# MASTER_KEY = 'cq6clU4wvdkmz6eeDoJMJODQNWQFE38jddM5drEM'

os.environ["PARSE_API_ROOT"] = "http://localhost:1337/1/"
APPLICATION_ID = 'udos'
REST_API_KEY = ''
MASTER_KEY = 'lars-key'


from parse_rest.datatypes import Function, Object, GeoPoint
from parse_rest.connection import register
from parse_rest.query import QueryResourceDoesNotExist
from parse_rest.connection import ParseBatcher
from parse_rest.core import ResourceRequestBadRequest, ParseError

register(APPLICATION_ID, REST_API_KEY, master_key=MASTER_KEY)

added = 0
updated = 0
skipped = 0
removed = 0

class Task(Object):
    pass


def addTask(n_id, fields):

    global updated
    global added
    global skipped

    # deck = getDeck(deckName)
    # print('ninfo: ', ninfo)
    if not len(n_id) > 0:
        print('n_id: ', n_id)
        throw("check your notion id")

    n_id = "".join(n_id.split("-"))

    taskRes = Task.Query.all().filter(n_id=n_id)
    if len(taskRes) > 0:
        task = taskRes[0]
        updated += 1
    else:
        added += 1
        task = Task(n_id=n_id, **fields)
        
    # print('gameScore: ', gameScore)
    for key in fields:
        if key == "question":
            task.question = fields[key]
        if key == "answer":
            task.answer = fields[key]
        if key == "answerLink":
            task.answerLink = fields[key]
        if key == "path":
            task.path = fields[key]
        if key == "state":
            task.state = fields[key]

    
    print('task: ', task)
    try:
        task.save()
    except:
        print("👎👎👎👎ERROR when saving", sys.exc_info()[0])



def getTasks(deck):
    taskRes = Task.Query.all().limit(9999)
    return taskRes


def moveToTrash(taskId):
    global removed
    taskRes = Task.Query.all().filter(n_id=taskId)
    if len(taskRes) == 0:
        print("not found!!")
        return
    task = taskRes[0]
    task.state="disabled"
    task.save()
    removed += 1


def printStats():
    print("")
    print("Updated: ", updated)
    print("Added: ", added)
    print("Skipped: ", skipped)
    print("Removed: ", removed)
