# %%
from notion.client import NotionClient
import random
import json
from anki import addNote, getNote, printStats, getDeck, invoke, mediaToHTML
import markdown
from progress.bar import Bar
import os

# %%
MEMOTALL_DECK = "all::memotall"
def hello():
	client = NotionClient(
		token_v2=os.environ["NOTION_TOKEN"])

	cv = client.get_collection_view(
		"https://www.notion.so/larskarbo/534d0728c32d474c9d23315d8afc82d5?v=f8eed84cbef6437ca18f9506f8469fe4")

	rows = cv.collection.get_rows()

	bar = Bar('Processing', max=len(rows))

	for row in rows:
		if not "37" in row.title:
			continue

		item = getNote(row.id, MEMOTALL_DECK)
		if item and item["fields"]["updated"]["value"] == str(row.upd):
			continue
		# return
		if not len(row.objektmedia):
			continue
		bar.next()
		back = row.objekt

		backstring = mediaToHTML(row.objektmedia)
		print(backstring)
		res = addNote({
			"Front": row.name,
			"Back": backstring,
			"n_id": row.id,
			"updated": str(row.upd)
		}, "all::memotall", model="Basic (and reversed card) with notion-id")

	bar.finish()


hello()

printStats()
