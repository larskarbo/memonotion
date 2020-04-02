from notion.client import NotionClient
import notion
import random
import json
from notionHelpers import blockToHTML
import markdown
import os

from progress.bar import Bar
from selenium import webdriver

DRIVER = 'chromedriver'



def addAndUpdate():
    # driver = webdriver.Chrome(DRIVER)   
    client = NotionClient(token_v2=os.environ["NOTION_TOKEN"])
    cv = client.get_collection_view(
        "https://www.notion.so/larskarbo/44bb6987ee86404dac44d16c68e3fc1e?v=67bf67c08de745cd90d94531f7059624")

    rows = cv.collection.get_rows()

    # bar = Bar('Processing', max=len(rows))

    for row in rows:
        # bar.next()
        print("row.name" ,row.name)
        print("row.url" ,row.url)
        # driver.get(row.url)
        # screenshot = driver.save_screenshot('my_screenshot.png')
        print('row.screenshot: ', row.screenshot)
        # row.setProperty("screenshot", "my_screenshot.png")
        # row.screenshot.upload_file('my_screenshot.png')
        row.set_property("screenshot", "https://www.notion.so/larskarbo/1-Trigonometric-shit-7dca248983d349e9b5b6db47b1f33fd6#c54824d713134a6ea56c228b25500dc6")


    # driver.quit()
        

        


addAndUpdate()

