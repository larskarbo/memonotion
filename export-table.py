
#%%
from notion.client import NotionClient
from notion.block import TextBlock, ImageBlock
import random
import os
import requests



#%%

client = NotionClient(token_v2=os.environ["NOTION_TOKEN"])

cv = client.get_collection_view(
    "https://www.notion.so/larskarbo/4439ff82ac764d45bdb0477c90f6c4e5?v=b82cafe8edaf4334a4cae22cfb01b3f0")

rows = cv.collection.get_rows()

#%%
strings = []
for row in rows:
    if "Squat" in row.ovelse:
        strings.append(row.dato.start.strftime("%d.%m.%Y")+"\t"+row.title)
    if "Press" in row.ovelse:
        strings.append(row.dato.start.strftime("%d.%m.%Y")+"\t\t"+row.title)
    if "Bench" in row.ovelse:
        strings.append(row.dato.start.strftime("%d.%m.%Y")+"\t\t\t"+row.title)
    if "Deadlift" in row.ovelse:
        strings.append(row.dato.start.strftime("%d.%m.%Y")+"\t\t\t\t"+row.title)

strings.reverse()

for s in strings:
    print(s)