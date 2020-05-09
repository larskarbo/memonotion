#!/usr/bin/env python
# %%
%load_ext autoreload
%autoreload 2

from notion.client import NotionClient
from notion.block import TextBlock, TodoBlock, BulletedListBlock
from datetime import datetime
from notionHelpers import findChild

# %%
client = NotionClient(token_v2=os.environ["NOTION_TOKEN"], monitor=True)

# %%
block = client.get_block("https://www.notion.so/larskarbo/Daily-entry-c9e4a17b8bdb4664b188a12521a62954")

# %%
today = datetime.today().strftime("%A")
print(today)
if today == "Thursday" or today == "Sunday":
    newchild = block.children.add_new(TodoBlock, title=("done [tor/søn biz](https://www.notion.so/larskarbo/tor-s-n-biz-e7d43e8da88b4cd785f6775fb80ef4d4)?"))
    newchild.move_to(newchild.parent, 'first-child')
else:
    victim = findChild(block, "tor/søn")
    victim.remove()
