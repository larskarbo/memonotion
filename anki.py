import json
import urllib.request
import os
import uuid

# if os.environ["ANKI_SERVER"]:
# 	anki_url = os.environ["ANKI_SERVER"]
# else:
anki_url = 'http://localhost:8765'


def request(action, **params):
	return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
	requestJson = json.dumps(request(action, **params)).encode('utf-8')
	response = json.load(urllib.request.urlopen(urllib.request.Request(anki_url, requestJson)))
	if len(response) != 2:
		raise Exception('response has an unexpected number of fields')
	if 'error' not in response:
		raise Exception('response is missing required error field')
	if 'result' not in response:
		raise Exception('response is missing required result field')
	if response['error'] is not None:
		raise Exception(response['error'])
	return response['result']

# invoke('createDeck', deck='test1')
# result = invoke('deckNames')
# print('got list of decks: {}'.format(result))

added = 0
updated = 0
skipped = 0
removed = 0


def sync(deck):
	yo = invoke("sync")


def getDeck(deck):
	yo = invoke("findNotes", query=("deck:"+deck))
	ninfo = invoke("notesInfo", notes=yo)
	return ninfo


def getDeckCards(deck):
	yo = invoke("findCards", query=("deck:"+deck))
	cinfo = invoke("cardsInfo", cards=yo)
	return cinfo

def getNote(n_id, deckName):
	deck = getDeck(deckName)
	for item in deck:
		if item["fields"]["n_id"]["value"] == n_id:
			return item
	return False

def addNote(fields, deckName, model):

	global updated
	global added
	global skipped

	deck = getDeck(deckName)
	# print('ninfo: ', ninfo)
	n_id = fields["n_id"]
	if not len(n_id) > 0:
		print('n_id: ', n_id)
		throw("check your notion id")
	for item in deck:
		if item["fields"]["n_id"]["value"] == n_id:

			changeDetected = False
			for field in fields:
				if item["fields"][field]["value"] != fields[field]:
					changeDetected = True


			if changeDetected:
				print('fields: ', fields)
				result = invoke('updateNoteFields', note={
					"id": item["noteId"],
					"fields": fields
				})
				updated += 1
				return "updated"

			skipped += 1
			return "skipped"

	note = {
		"deckName": deckName,
		"modelName": model,
		"fields": fields,
		"options": {
			"allowDuplicate": True
		},
		"tags": [],
		"id": n_id
	}
	print('note: ', note)
	result = invoke('addNote', note=note)
	added += 1
	return "added"


def moveToTrash(taskId):
	global removed
	taskRes = Task.Query.all().filter(n_id=taskId)
	if len(taskRes) == 0:
		print("not found!!")
		return
	task = taskRes[0]
	task.state="disabled"
	task.save()
	removed += 1

def getLocalFile(url):
	filename = uuid.uuid4()
	invoke("storeMediaFile", filename=str(filename), url=url)
	return str(filename)

def mediaToHTML(medias):
	s = ""
	for media in medias:
		ending = media.split(".")[-1].split("?")[0]
		if ending in ["gif", "png", "jpg"]:
			s += '<img src="' + getLocalFile(media) + '">'
		elif ending in ["mp3"]:
			s += "[sound:" + getLocalFile(media) + "]"
		else:
			print("ending ", ending, "not supported")
	return s


def printStats():
	print("")
	print("Updated: ", updated)
	print("Added: ", added)
	print("Skipped: ", skipped)
	print("Removed: ", removed)
