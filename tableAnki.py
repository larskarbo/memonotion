from notion.client import NotionClient
import random
import json
from udos import addNote, printStats
import markdown
from random import randint
from udos import addNote, printStats, getDeck, getDeckCards, moveToTrash

from progress.bar import Bar
from notionHelpers import count_elements, get_next_cv


def progressBar(at, max):
    strng = "["
    for i in range(15):
        if i / 15 < at / max:
            strng += "="
        else:
            strng += "_"
    strng += "] " + str(at) + "/" + str(max)

    return strng

def hello():
    client = NotionClient(
        token_v2="738991375dbb49e1050ead92da668fb277c43c6df82f1dd49b6e667a3d83a8da738051a0a7d489d04dccaa043b81e6d196beaa11f7e6a4e233a96491391d13337a9fbc7a2911f6a9f9a4452f1192")
    
    # rows = cv.collection.get_rows()
    jojo = client.search("🏓")

    for block_id in jojo["results"]:
        block = client.get_block(block_id)

        cv = get_next_cv(client, block)
        rows = cv.collection.get_rows()
        for row in rows:
            obj = {
                "Question": row.title,
                "Answer": row.answer,
                "AnswerLink": block.parent.get_browseable_url(),
                "Topic": cv.collection.name
            }
            # print('obj: ', obj)
            res = addTask(row.id, obj, "notion")
        # done = count_elements(cv)
        # print('done: ', done)



hello()


printStats()
