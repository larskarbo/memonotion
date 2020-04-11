#!/usr/bin/env python
# %%
import random

from notion.client import NotionClient
from notion.block import TextBlock, ImageBlock, BulletedListBlock
import os
import requests
import time

def findChild(page, searchString):
    for child in page.children:
        if child.type == "text" or child.type == "toggle":
            if searchString in child.title:
                return child

# %%
client = NotionClient(token_v2=os.environ["NOTION_TOKEN"], monitor=True)


# %%
block = client.get_block("https://www.notion.so/larskarbo/French-31afa53ea32b44e9a52c9525fae99d0f#26ce76377f784964bae3bd01300bc665")


# %%
def countStreak():
    alltext = ""
    for child in block.children:
        alltext += child.title

    streak = alltext.count("🏇")
    streakHolder = findChild(block, "🔥")
    oldstreak = int(streakHolder.title.split(":")[1])
    if streak != oldstreak:
        streakHolder.title = "🔥 The current streak is: " + str(streak)
    if streak > oldstreak:
        giveNewGift(streak)

def giveNewGift(streak):
    gift_central = client.get_block("https://www.notion.so/larskarbo/Cyri-Streak-Gifts-d7679ab742244db7ac6d717e0f5195fd")
    giftHolder = findChild(block, "🎁")
    gift = findChild(gift_central, str(streak))
    if not gift:
        giftHolder.children.add_new(TextBlock, title=("There are no gifts for you for " + str(streak)))
    else:
        gift.move_to(giftHolder)
# %%
# %%

# define a callback (note: all arguments are optional, just include the ones you care about)
def my_callback(record, changes):
    countStreak()
    for change in changes:
        if change[0] == "content_added":
            client.get_block(change[2]).add_callback(my_callback)

countStreak()
# move my block to after the video
block.add_callback(my_callback)
for child in block.children:
    if "🔥" in child.title:
        continue
    if "🔥" in child.title:
        continue
    child.add_callback(my_callback)
client.start_monitoring()

print("Running habitsstreak")
# %%
while(True):
    time.sleep(1)