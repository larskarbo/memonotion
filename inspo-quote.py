#!/usr/bin/env python

import random
from notion.client import NotionClient
from notion.block import TextBlock, ImageBlock, BulletedListBlock
import os
import requests
import random

def findChild(page, searchString):
    for child in page.children:
        if child.type == "text":
            if searchString in child.title:
                return child

client = NotionClient(token_v2=os.environ["NOTION_TOKEN"])

quotes = requests.get("https://type.fit/api/quotes")
quote = random.choice(quotes.json())
# print(quote)

template = client.get_block("https://www.notion.so/larskarbo/Daily-entry-c9e4a17b8bdb4664b188a12521a62954")

quoteHolder = findChild(template, "Motivational quote of the day")

for child in quoteHolder.children:
    child.remove()

if random.random() > 0.8:
    quoteHolder.children.add_new(TextBlock, title=("**" + quote["text"] + "** -" + quote["author"]))
else:
    quoteHolder.children.add_new(TextBlock, title=("no quote today..."))