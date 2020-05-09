
#%%
from notion.client import NotionClient
from notion.block import TextBlock, ImageBlock
import random
import os
import requests
import shutil


import glob

#%%

client = NotionClient(token_v2=os.environ["NOTION_TOKEN"])

cv = client.get_collection_view(
    "https://www.notion.so/larskarbo/f2092f7d6c3648829ff60158cbc26d02?v=229aab90249741ec84abc517a4d3abfc")

rows = cv.collection.get_rows()

#%%
i = 1
for row in rows:
    if "scarce" in row.tags:
        print(row.title)
        files = glob.glob('scarceproject/'+row.title+"/*.epub")
        files.sort()
        name = files[0]
        print(name)
        shutil.copyfile(name, "/Users/lars/Library/Mobile Documents/iCloud~com~apple~iBooks/Documents/" + "Part " + str(i) + " of " + row.title + ".epub")
        row.scarcestatus = str(i) + " / " + str(len(files))
        row.scarcetag = "notread"