# %%
from dictPro.getIpa import get_ipa
from anki import invoke
import json


import os
from notion.client import NotionClient
from notion.block import TextBlock, ImageBlock, BulletedListBlock
import random

client = NotionClient(token_v2=os.environ["NOTION_TOKEN"], monitor=True)

block = client.get_block(
	"https://www.notion.so/larskarbo/minimal-pairs-994661097f4b406ab012d0465e876c06#b49e00b7f2ff462ea723a0f36f1151d5")

# %%
print(get_ipa("cheval"))
# %%
for child in block.children:
	print(child.title)
	arr = child.title.split("vs")

	ipa1 = get_ipa(arr[0])
	ipa2 = get_ipa(arr[1])
4
	child.title = arr[0] + " /" + ipa1 + "/ vs " + arr[1] + " /" + ipa2 + "/"
	continue
	dice = random.randint(0,1)
	w1 = arr[dice]
	w2 = arr[(dice+1)%2]
	notes = invoke('addNote', note={
		"deckName": "French::minimal pairs",
		"modelName": "1. Minimal Pairs",
			"fields": {
				"Word 1": w1,
				"Word 2": w2
			},
			"options": {
				"allowDuplicate": False
			},
			"tags": [
				"horses"
			],
	})


# notes = invoke('findNotes', query="deck:French")
# notes = invoke('notesInfo', notes=notes)


# %%
print(random.randint(0,1))

# %%
