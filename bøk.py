from notion.client import NotionClient
import random
import json
from parse import addTask, getTasks, moveToTrash, printStats
from notionHelpers import blockToHTML
import markdown
import os

from progress.bar import Bar


def addAndUpdate():
    client = NotionClient(token_v2=os.environ["NOTION_TOKEN"])

    jojo = client.search("📚")
    bar = Bar('Processing', max=len(jojo["results"]))

    for block_id in jojo["results"]:
        bar.next()
        block = client.get_block(block_id)
        print('block: ', block)

        answer = ""
        answerLink = ""
        question = block.title.split(":")[0]
        if ":" in block.title:
            question += ":"
        try:
            block.parent.type
        except:
            print("skipping this:", block.title)
            continue

        if "↑" in block.title:
            continue
        if block.parent.type == "column":
            answerLink = block.parent.parent.get_direct_browseable_url()
        else:
            answerLink = block.get_direct_browseable_url()
            if block.get("content"):
                # print(blockToHTML(client, "b6237023-b8e9-4fef-9674-cb149f97a0a9"))
                answer = blockToHTML(client, block_id)
                print('answer: ', answer)
            elif ":" in block.title:
                answer = markdown.markdown(block.title.split(":")[1])

        path = []

        def recursiveFindPath(block):
            if type(block).__name__ == "Collection":
                path.append(block.name)
            elif type(block).__name__ == "Space":
                return
            else:
                if "page" in block._type:
                    path.append(block.title)
                recursiveFindPath(block.parent)

        recursiveFindPath(block)
        print('path: ', path)

        path.reverse()

        state = "active"
        if "nossr" in "".join(path):
            state = "disabled"

        res = addTask(n_id=block_id), fields={
            "question": question,
            "answer": answer,
            "answerLink": answerLink,
            "path": path,
            "state": state
        }, tp="📚")

    bar.finish()


def deleteTrashNotions():

    client = NotionClient(
        token_v2=os.environ["NOTION_TOKEN"])
    cards = getTasks("all::Notion-deck")
    # for note in notes:

    # TODO UDOS

    # block.remove(True)
    bar = Bar('Processing', max=len(cards))

    for card in cards:
        block = client.get_block(card.n_id)
        print('block: ', block)
        if not block.alive or not "📚" in block.title:
            moveToTrash(card.n_id)
        bar.next()
    bar.finish()


addAndUpdate()
# deleteTrashNotions()

printStats()
