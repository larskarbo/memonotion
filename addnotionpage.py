from notion.client import NotionClient
import random
import json
from anki import addNote, printStats
import markdown

from progress.bar import Bar
import os
from notion.block import PageBlock





def hello():
    client = NotionClient(
        token_v2=os.environ["NOTION_TOKEN"])
    
    page = client.get_block("https://www.notion.so/larskarbo/Random-976529219dde4b9bb66260b55b3f8a4f")

    newchild = page.children.add_new(PageBlock, title="")
    id = newchild.get_browseable_url().split("/")[-1]
    os.system("open notion://larskarbo/" + newchild.get_browseable_url().split("/")[-1])



hello()
