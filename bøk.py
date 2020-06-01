#%%
# %reload_ext autoreload
# %autoreload 2
from notion.client import NotionClient
import random
import json
from anki import addNote, moveToTrash, printStats, sync
from notionHelpers import blockToHTML
import markdown
import os

from progress.bar import Bar

client = NotionClient(token_v2=os.environ["NOTION_TOKEN"])

#%%
def addAndUpdate():


	jojo = client.search_blocks("📖")

	bar = Bar('Processing', max=len(jojo))

	for block in jojo:
		bar.next()
		answer = ""
		answerLink = ""
		question = block.title.split(":")[0]
		if ":" in block.title:
			question += ":"
		try:
			block.parent.type
		except:
			print("skipping this:", block.title)
			continue

		# answerLink = block.get_direct_browseable_url()
		if block.get("content"):
			print(block.get("content"))
			# print(blockToHTML(client, "b6237023-b8e9-4fef-9674-cb149f97a0a9"))
			answer = blockToHTML(client, block)
		elif ":" in block.title:
			answer = markdown.markdown(block.title.split(":")[1])

		print(question, answer)
		path = []

		def recursiveFindPath(block):
			if type(block).__name__ == "Collection":
				path.append(block.name)
			elif type(block).__name__ == "Space":
				return
			else:
				if "page" in block._type:
					path.append(block.title)
				recursiveFindPath(block.parent)

		recursiveFindPath(block)
		path.reverse()

		res = addNote(fields={
			"n_id": block.id,
			"question": question,
			"answer": answer,
			"answerLink": answerLink,
			"path": "-".join(path)
		}, deckName="all::memo", model="memonote")

	bar.finish()


def deleteTrashNotions():

	client = NotionClient(
		token_v2=os.environ["NOTION_TOKEN"])
	cards = getTasks("all::Notion-deck")
	# for note in notes:

	# TODO UDOS

	# block.remove(True)
	bar = Bar('Processing', max=len(cards))

	for card in cards:
		block = client.get_block(card.n_id)
		print('block: ', block)
		if not block.alive or not "📚" in block.title:
			moveToTrash(card.n_id)
		bar.next()
	bar.finish()


sync()
addAndUpdate()
sync()
# deleteTrashNotions()

printStats()
