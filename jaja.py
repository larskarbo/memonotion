from notion.client import NotionClient
import random
import json
from anki import addNote, printStats, getDeck, getDeckCards, moveToTrash
import markdown

from progress.bar import Bar

def blockToHTML(client, blockID):
    block = client.get_block(blockID)
    print('block.type: ', block.type)
    out = ""
    childrenOut = ""
    try:
        children = block.get("content")
        for child in children:
            childrenOut += blockToHTML(client, child)
    except Exception as e:
        print(e)
        childrenOut = block.title

    print('children: ', children)

    if block.type == "toggle":
        out = "<div class='toggle'>" + block.title + "<div>" + childrenOut + "</div></div>"
    elif block.type == "column_list":
        out = "<div class='column_list'>" + childrenOut + "</div>"
    elif block.type == "column":
        out = "<div class='column'>" + childrenOut + "</div>"
    elif block.type == "bulleted_list":
        out = "<ul><li>" + childrenOut + "</li></ul>"
    elif block.type == "text":
        out = "<p>" + childrenOut + "</p>"
    else:
        print("what to do with " + block.type)
    
    
    


    return out
    # if (block.title):
    #     return block.title

    # for child in children:
    #     blockToHTML(client, blockID)



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
        question = markdown.markdown(block.title.split(":")[0])
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
        res = addNote({
            "Question": question,
            "Answer": answer,
            "AnswerLink": answerLink,
            "Topic": topicTitle,
            "notion-id": block_id
        }, deckName="all::Notion-deck", model="notion-model2")

    bar.finish()


def deleteTrashNotions():
    client = NotionClient(
        token_v2="738991375dbb49e1050ead92da668fb277c43c6df82f1dd49b6e667a3d83a8da738051a0a7d489d04dccaa043b81e6d196beaa11f7e6a4e233a96491391d13337a9fbc7a2911f6a9f9a4452f1192")

    cards = getDeckCards("all::Notion-deck")
    # for note in notes:

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
