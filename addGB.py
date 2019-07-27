from notion.client import NotionClient
from notionHelpers import cv_props
import random
import json
from anki import addNote, printStats
import markdown
import os
import logging

# logging.basicConfig(level=logging.DEBUG)
from progress.bar import Bar


def hello():
    client = NotionClient(token_v2=os.environ.get("NOTION_TOKEN"))

    cv = client.get_collection_view(
        "https://www.notion.so/larskarbo/ab34c70eca0e4362b08e8b9e50d8697f?v=50087fce41354391b7f65489ebf815c9")

    rows = cv.collection.get_rows()

    bar = Bar('Processing', max=len(rows))

    for row in rows:
        bar.next()
        take = ""
        if len(row.take):
            take = row.take[0]

        res = addNote({
            "Front": row.bilde[0],
            "link": row.link,
            "memolink": row.get_browseable_url(),
            "Back": row.name,
            "notion-id": row.id,
            "Backimg": take
        }, "all::GBF", model="Basic-notion-id-front-bilde")
        
            

    bar.finish()


hello()

printStats()
