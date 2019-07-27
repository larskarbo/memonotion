from notion.client import NotionClient
import random
import json
from couch import addTask, printStats
import markdown

from progress.bar import Bar





def hello():
    client = NotionClient(
        token_v2="738991375dbb49e1050ead92da668fb277c43c6df82f1dd49b6e667a3d83a8da738051a0a7d489d04dccaa043b81e6d196beaa11f7e6a4e233a96491391d13337a9fbc7a2911f6a9f9a4452f1192")
    
    cv = client.get_collection_view(
        "https://www.notion.so/larskarbo/534d0728c32d474c9d23315d8afc82d5?v=f8eed84cbef6437ca18f9506f8469fe4")

    rows = cv.collection.get_rows()

    bar = Bar('Processing', max=len(rows))

    for row in rows:
        bar.next()
        print()
        types = ["objekt", "person", "handling"]
        for t in types:
            if t == "objekt":
                back = row.objekt
                mediaanswer = row.objektmedia
            if t == "person":
                back = row.person
                mediaanswer = row.personmedia
            if t == "handling":
                back = row.handling
                mediaanswer = row.handlingmedia
            res = addTask(n_id=row.id + t, fields={
                "question": t + " for tall " + row.name,
                "answer": back,
                "answerlink": row.get_browseable_url(),
                "mediaanswer":mediaanswer,
                "topic":"memotall"
            }, tp="memotall")

        
            
    bar.finish()

hello()

printStats()
