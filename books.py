
#%%
from notion.client import NotionClient
from notion.block import TextBlock, ImageBlock
import random
import os
import requests



#%%

client = NotionClient(token_v2=os.environ["NOTION_TOKEN"])

cv = client.get_collection_view(
    "https://www.notion.so/larskarbo/f2092f7d6c3648829ff60158cbc26d02?v=229aab90249741ec84abc517a4d3abfc")

rows = cv.collection.get_rows()


#%%
def addImage(page, path):
    if len(page.children):
        first = row.children[0]
        if first.type == 'image':
            return

    newchild = row.children.add_new(ImageBlock)
    newchild.upload_file(path)
    newchild.caption = "Cover"

    newchild.move_to(newchild.parent, 'first-child')

#%%
i = 0
for row in rows:
    if row.fixcover:
        print(row.title)
        resp = requests.get("http://go-to-book.local:9999/book/" + row.title)
        if resp.json()["status"] == "ok":
            # row.link = "http://localhost:9999/book/" + row.title.replace(" ", "-") + "/open"
            if resp.json()["cover"]:
                print("cover!", row.title)
                addImage(row, resp.json()["cover"])
                # break
                row.fixcover = False
        else:
            row.link = ""

# %%
for row in rows:
    if len(row.children):
        first = row.children[0]
        if first.type == 'image':
            continue
    row.state = "away"
print("horse")