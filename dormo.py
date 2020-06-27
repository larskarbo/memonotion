

from notion.client import NotionClient
from bottle import route, run, template
import os
import datetime
from slugify import slugify
from threading import Timer
import json
from datetime import datetime

client = NotionClient(token_v2=os.environ["NOTION_TOKEN"])

data = json.loads('[{"date":"2020-06-12T14:09:08.750Z","type":"evening","answers":{"coffee":false,"daytime_function":3,"bedtime":"02:00"},"user":"larskarbo"},{"date":"2020-06-12T14:21:51.918Z","type":"evening","answers":{"coffee":true,"daytime_function":3,"bedtime":"02:00"},"user":"larskarbo"},{"date":"2020-06-15T12:10:54.880Z","type":"morning","answers":{"sleep_onset_delay":30,"wake_up":"07:30","out_of_bed":"08:00","morning_feeling":2},"user":"larskarbo"},{"date":"2020-06-15T12:12:19.348Z","type":"morning","answers":{"sleep_onset_delay":30,"wake_up":"07:30","out_of_bed":"08:05","morning_feeling":3},"user":"larskarbo"},{"date":"2020-06-15T12:15:25.849Z","type":"morning","answers":{"sleep_onset_delay":20,"wake_up":"07:30","out_of_bed":"08:00","morning_feeling":2},"user":"larskarbo"},{"date":"2020-06-15T12:18:18.672Z","type":"morning","answers":{"sleep_onset_delay":20,"wake_up":"07:30","out_of_bed":"08:00","morning_feeling":1},"user":"larskarbo"}]')


def getPosts():
	cv = client.get_collection_view("https://www.notion.so/larskarbo/e43e66738e214613acb0b4afd18e0577?v=cc1eb3a474654b13b77080c97aa3e4e9")
	rows = cv.collection.get_rows()
	posts = {}
	for entry in data:
		print(entry)
		print(entry['answers']['daytime_function'])
		row = cv.collection.add_row()
		row.date = datetime.fromisoformat(entry['date'].replace("Z", "+00:00"))

		row.daytime = entry['answers']['daytime_function']
		row.bedtime = entry['answers']['bedtime']
		row.coffee = entry['answers']['coffee']
		break

getPosts()


# @route('/addEntry', method='POST')
# def index():
# 	return {"posts":getPosts()}


# run(host='localhost', port=2232)
