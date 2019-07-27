from notion.client import NotionClient
import random
import json
from couch import addTask, printStats
import markdown

from progress.bar import Bar


def addAndUpdate():
    client = NotionClient(
        token_v2="738991375dbb49e1050ead92da668fb277c43c6df82f1dd49b6e667a3d83a8da738051a0a7d489d04dccaa043b81e6d196beaa11f7e6a4e233a96491391d13337a9fbc7a2911f6a9f9a4452f1192")

    jojo = client.search("📚")
    bar = Bar('Processing', max=len(jojo["results"]))

    for block_id in jojo["results"]:
        bar.next()
        block = client.get_block(block_id)
        print('block: ', block)

        answer = ""
        answerLink = ""
        question = block.title.split(":")[0]
        try:
            block.parent.type
        except:
            print("skipping this:", block.title)
            continue

        if "↑" in block.title:
            continue
        if block.parent.type == "column":
            answerLink = block.parent.parent.get_direct_browseable_url()
        elif block.get("content"):
            answerLink = block.get_direct_browseable_url()
            # print(blockToHTML(client, "b6237023-b8e9-4fef-9674-cb149f97a0a9"))
            # print(blockToHTML(client, block_id))
        elif ":" in block.title:
            answer = markdown.markdown(block.title.split(":")[1])

        # block.parent.title
        def title(block):
            if "page" in block._type:
                return block.title
            else:
                return title(block.parent)

        topicTitle = title(block)
        res = addTask(n_id=block_id, fields={
            "question": question,
            "answer": answer,
            "answerLink": answerLink,
            "topic": topicTitle
        }, tp="📚")


    bar.finish()


def deleteTrashNotions():
    client = NotionClient(
        token_v2="738991375dbb49e1050ead92da668fb277c43c6df82f1dd49b6e667a3d83a8da738051a0a7d489d04dccaa043b81e6d196beaa11f7e6a4e233a96491391d13337a9fbc7a2911f6a9f9a4452f1192")

    return
    cards = getDeckCards("all::Notion-deck")
    # for note in notes:

    
    ## TODO UDOS

    # block.remove(True)
    bar = Bar('Processing', max=len(cards))

    for card in cards:
        block = client.get_block(card["fields"]["notion-id"]["value"])
        if "↑" in block.title or not block.alive or not "📚" in block.title:
            moveToTrash(card["cardId"])
        bar.next()
    bar.finish()


addAndUpdate()
deleteTrashNotions()

printStats()
