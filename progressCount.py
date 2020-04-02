from notion.client import NotionClient
import random
import json
from anki import addNote, printStats
import markdown
from random import randint
import os

from progress.bar import Bar
from notionHelpers import count_elements


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
        token_v2=os.environ["NOTION_TOKEN"])
    
    block = client.get_block(
        "https://www.notion.so/larskarbo/MEMO-100-e3443bc723324b6dbf346146a3edd61e#3f6b8251f8b84e4e8a04525cca37f70c")

    print('block: ', block)
    

    # rows = cv.collection.get_rows()
    jojo = client.search("🧮")

    for block_id in jojo["results"]:
        block = client.get_block(block_id)

        total = int(block.title.split(":")[1])
        children = block.parent.children
        nextIsOurView = False
        # faila å automatisk finne view id, så hardcoda urlen istedet
        url = "https://www.notion.so/larskarbo/534d0728c32d474c9d23315d8afc82d5?v=f8eed84cbef6437ca18f9506f8469fe4"
        print('children: ', children)
        for child in children:
            if nextIsOurView:
                collection = child.collection
                cv = client.get_collection_view(url)
                break
            if child.id == block_id:
                nextIsOurView = True
        done = count_elements(cv)
        print('done: ', done)
        print('total: ', total)

        progress = progressBar(done, total)
        print('progressBar(done, total): ', progressBar(0, 100))
        print('progressBar(done, total): ', progressBar(100, 100))
        child.title = child.title.split("|")[0] + " | " + progress
        
        print('progress: ', progress)


hello()
