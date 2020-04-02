from notion.client import NotionClient
import random
import json
from parse import addTask, printStats
import markdown
import os
from progress.bar import Bar





def hello():
    client = NotionClient(token_v2=os.environ["NOTION_TOKEN"])
    
    cv = client.get_collection_view(
        "https://www.notion.so/larskarbo/b7fa0ea238224fa0a0c947e7b81f14de?v=b5bc7261778446dda00869546855fdc0")

    rows = cv.collection.get_rows()

    # bar = Bar('Processing', max=len(rows))

    for row in rows:
        # bar.next()
        print("row.name" ,row.name)
        print("row.bilde" ,row.bilde)
        state = "active"
        if len(row.bilde) == 0:
            state = "disabled"

        addTask(n_id=(row.id), fields={
            "question": "wtf",
            "answer": row.name,
            "answerLink": row.get_direct_browseable_url(),
            "path": ["DIV"],
            "state": state
        })

        

        
            
    # bar.finish()

hello()

printStats()
