

from notion.client import NotionClient
from bottle import route, run, template
import os

client = NotionClient(token_v2=os.environ["NOTION_TOKEN"])

def go():
	jojo = client.search_blocks("[BLOG]")
	blogBlocks = []
	for block in jojo:
		if "[BLOG]" in block.title:
			print('block: ', block.parent)
			if not block.parent.id == "6f34b26f-fa8f-49d4-8fd2-bd1374e51727":
				blogBlocks.append(block)
	cv = client.get_collection_view("https://www.notion.so/larskarbo/614df30f82b6467e8eb4ce0ebea5d721?v=18b0779a38fa4c4c85cbab3b9362d168")

	rows = cv.collection.get_rows()
	print('rows: ', rows)

	for post in blogBlocks:

		already_exists = False
		for row in rows:
			if row.n_id == post.id:
				already_exists = row
				break

		if not already_exists:
			thisrow = cv.collection.add_row()
			thisrow.title = post.title
			thisrow.n_id = post.id
		else:
			thisrow = already_exists


go()

# @route('/getentries')
# def index():
# 	jojo = client.search_blocks("[BLOG]")
# 	blogBlocks = []
# 	for block in jojo:
# 		if "[BLOG]" in block.title:
# 			blogBlocks.append(block.id)
# 	return {
# 		"blocks": blogBlocks
# 	}

# run(host='localhost', port=2232)
