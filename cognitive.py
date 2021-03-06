#!/usr/bin/env python
# %%
import random

from notion.client import NotionClient
from notion.block import TextBlock, ImageBlock, BulletedListBlock
import os
import requests
import time
import json
from datetime import datetime
import sys

if not datetime.today().strftime("%a") == "Sat":
	print("exiting")
	sys.exit()

def findChild(page, searchString):
    for child in page.children:
        if child.type == "text" or child.type == "toggle":
            if searchString in child.title:
                return child

# %%
client = NotionClient(token_v2=os.environ["NOTION_TOKEN"], monitor=True)


# %%
block = client.get_block("https://www.notion.so/larskarbo/Cognitive-Biases-a76ec7177f9e403a9916e2c3c872cde6")


# %%
f=open("cognitive-biases.json", "r")
biases = json.load(f)
# %%
def writeFile():
    f=open("cognitive-biases.json","w+")
    json.dump(biases, f)
    f.close()

def findUntaken():
    chapter = random.choice(biases['children'])
    sub = random.choice(chapter['children'])
    bias = random.choice(sub['children'])
    if "taken" in bias:
        return findUntaken()
    bias["taken"] = True
    writeFile()
    return (chapter["name"], sub["name"], bias["name"])


# %%
gift_central = client.get_block("https://www.notion.so/larskarbo/Gift-central-c8420c0f914440e0a5d68e6c6e972701")
for child in gift_central.children:
    child.remove()

def addBias():
    (chapter, sub, bias) = findUntaken()
    gift_central.children.add_new(TextBlock, title=("**" + bias + "**"))
    gift_central.children.add_new(TextBlock, title="subsection: " + sub)
    gift_central.children.add_new(TextBlock, title="section: " + chapter + "")

def addSorry():
    gift_central.children.add_new(TextBlock, title=("sorry, no new biases"))

addBias()

requests.get("https://api.telegram.org/bot1196576929:AAFCVPBTMcSUlrHAIFBO_Ni7e9em0Nje10U/sendMessage?chat_id=912275377&text=remember to do a cognitive today!")
# %%

# %%
