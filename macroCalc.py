from notion.client import NotionClient
import random
import json
from anki import addNote, printStats, getDeck, getDeckCards, moveToTrash
import markdown
import os

from progress.bar import Bar

def macroCalcTable(cv, tittel, porsj):
    print('porsj: ', porsj)
    rows = cv.collection.get_rows()
    macros = {
        "protein": 0,
        "fett": 0,
        "karbohydrat": 0,
        "kcal": 0,
        "kroner": 0
    }
    print('tittel: ', tittel)
    for row in rows:
        if len(row.matvare) == 0:
            continue
        if tittel != row.recipe[0].title:
            continue
        print('row: ', row)
        print('row.recipe: ', row.recipe)
        print('row.name: ', row.name)
        print('row.matvare: ', row.matvare)
        # row.matvare burde vert en enkel matvare, men er istedet en array
        # med mange. Vi tar å søker gjennom for å finne elementet som ikkje
        # er None
        for matvareKandidat in row.matvare:
            if matvareKandidat:
                matvare = matvareKandidat
        

        print('matvare: ', matvare)
        hektogram = row.gram / (100 * porsj)
        if matvare.protein is None:
            matvare.protein = 0
        if matvare.fett is None:
            matvare.fett = 0
        if matvare.kcal is None:
            matvare.kcal = 0
        if matvare.karbohydrat is None:
            matvare.karbohydrat = 0
        row.protein = round(matvare.protein * hektogram)
        row.fett = round(matvare.fett * hektogram)
        row.karbohydrat = round(matvare.karbohydrat * hektogram)
        row.kcal = round(matvare.kcal * hektogram)
        macros["protein"] += matvare.protein * hektogram
        macros["fett"] += matvare.fett * hektogram
        macros["karbohydrat"] += matvare.karbohydrat * hektogram
        macros["kcal"] += matvare.kcal * hektogram

        if row.kroner:
            macros["kroner"] += row.kroner/porsj

    for macro in macros:
        macros[macro] = round(macros[macro])
    print('macros: ', macros)
    return macros


def hello():
    client = NotionClient(token_v2=os.environ.get("NOTION_TOKEN"))

    cv = client.get_collection_view(
        "https://www.notion.so/larskarbo/7aa8bbb6129241dbb03f9460e6270113?v=5ebb4bee12c34ef09408c8c0cbb0df45")

    rows = cv.collection.get_rows()
    bar = Bar('Processing', max=len(rows))
    for row in rows:
        bar.next()
        # if row.name == "2 brødskiver med kaviar og egg":
        
        for child in row.children:
            if child.type == "collection_view":
                # child
                cv2 = client.get_collection_view(
                    child.views[0].id, collection=child.collection)
                macros = macroCalcTable(cv2, row.name, row.antall_porsjoner)
                row.protein = macros["protein"]
                row.fett = macros["fett"]
                row.karbohydrat = macros["karbohydrat"]
                row.kcal = "🔥 " + str(macros["kcal"]) + " kcal"
                row.kroner = "💰 " + str(macros["kroner"]) + " kr"
    
    if cv2 is None:
        print("cv2 is none")
        return
    
    bar.finish()


hello()
