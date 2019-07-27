from notion.client import NotionClient
import random
import json
from anki import addNote, printStats, getDeck, getDeckCards, moveToTrash
import markdown

from progress.bar import Bar

def hello():
    client = NotionClient(
        token_v2="738991375dbb49e1050ead92da668fb277c43c6df82f1dd49b6e667a3d83a8da738051a0a7d489d04dccaa043b81e6d196beaa11f7e6a4e233a96491391d13337a9fbc7a2911f6a9f9a4452f1192")
    
    cv = client.get_collection_view(
        "https://www.notion.so/larskarbo/ab34c70eca0e4362b08e8b9e50d8697f?v=50087fce41354391b7f65489ebf815c9")
    yo = open("res.csv", "r")
    yo = list(map(lambda item: item.split(","), yo))
    addedPeeps = []
    real = []
    for line in yo:
        # if line[6] != "OMEGAFADDER<3":
        if line[6] != "Gründerbrakka":
            continue
        name = line[3]
        if name in addedPeeps:
            continue
        addedPeeps.append(name)
        real.append(line)

    bar = Bar('Processing', max=len(real))
    for line in real:
        bar.next()
        print(line[3])
        row = cv.collection.add_row()
        row.name = line[3]
        row.bilde = line[2]
        row.link = line[0]
    
    bar.finish()
hello()
