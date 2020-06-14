

from notion.client import NotionClient
from bottle import route, run, template
import os
import datetime
from slugify import slugify
from threading import Timer

client = NotionClient(token_v2=os.environ["NOTION_TOKEN"])



def getPosts():
	cv = client.get_collection_view("https://www.notion.so/larskarbo/614df30f82b6467e8eb4ce0ebea5d721?v=18b0779a38fa4c4c85cbab3b9362d168")
	rows = cv.collection.get_rows()
	posts = {}
	for row in rows:
		posts[row.slug] = {
			"page": row.page,
			"tags": row.tags,
			"slug": row.slug,
			"published": row.published,
			"n_id": row.n_id,
			"date": (row.date.start-datetime.date(1970,1,1)).total_seconds() * 1000,
			"authors": ["Lars Karbø"],
		}
	return posts


def searchAndAddToTable():
	jojo = client.search_blocks("[BLOG]")
	blogBlocks = []
	for block in jojo:
		if "[BLOG]" in block.title:
			print('block: ', block.title)
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
			print(post.title)
			thisrow = cv.collection.add_row()
			thisrow.n_id = post.id
			thisrow.slug = slugify(post.title.replace("[BLOG]", ""))
		else:
			thisrow = already_exists

		thisrow.title = post.title.replace("[BLOG] ", "")

	Timer(10*60, searchAndAddToTable).start()

searchAndAddToTable()

@route('/getposts')
def index():
	return {"posts":getPosts()}


run(host='localhost', port=2232)
