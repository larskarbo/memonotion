#!/usr/bin/env python
# %%

# todo move these to global config ↓
# %load_ext autoreload
# %autoreload 2

from notion.client import NotionClient
from notion.block import TextBlock, TodoBlock, BulletedListBlock
from datetime import datetime
from notionHelpers import findChild
import requests
import os

# %%
client = NotionClient(token_v2=os.environ["NOTION_TOKEN"], monitor=True)

# %%
block = client.get_block("https://www.notion.so/larskarbo/Daily-entry-c9e4a17b8bdb4664b188a12521a62954")

# %%
today = datetime.today().strftime("%A")
print(today)
if today == "Thursday" or today == "Sunday":
    requests.get("https://api.telegram.org/bot1196576929:AAFCVPBTMcSUlrHAIFBO_Ni7e9em0Nje10U/sendMessage?chat_id=912275377&text=remember thur sun!")
    newchild = block.children.add_new(TodoBlock, title=("done [tor/søn biz](https://www.notion.so/larskarbo/tor-s-n-biz-e7d43e8da88b4cd785f6775fb80ef4d4)?"))
    newchild.move_to(newchild.parent, 'first-child')
else:
    victim = findChild(block, "tor/søn")
    if victim:
        victim.remove()

#%%
if today == "Tuesday":
    requests.get("https://api.telegram.org/bot1196576929:AAFCVPBTMcSUlrHAIFBO_Ni7e9em0Nje10U/sendMessage?chat_id=912275377&text=remember to read scarce books!")
    newchild = block.children.add_new(TodoBlock, title=("are scarce books read? (todo fix delete and update script)"))
    newchild.move_to(newchild.parent, 'first-child')
else:
    victim = findChild(block, "carce books re")
    if victim:
        victim.remove()