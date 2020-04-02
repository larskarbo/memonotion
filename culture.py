from notion.client import NotionClient
import notion
import random
import json
from notionHelpers import blockToHTML
import markdown
import os
from notion.block import TextBlock

from progress.bar import Bar
from selenium import webdriver
import random
DRIVER = 'chromedriver'



def go():
    # driver = webdriver.Chrome(DRIVER)   
    client = NotionClient(token_v2=os.environ["NOTION_TOKEN"])
    
    block = client.get_block("https://www.notion.so/larskarbo/Culture-Poster-b17e335301694a619d0938ec68257af3")

    targetBlock = client.get_block("https://www.notion.so/larskarbo/Personal-work-preferences-d6b1cd3bff1f4969a4bf735674dbc2df#dde5cec4948240d5a957fdfcb5705d38")

    # delete all
    for child in targetBlock.children:
      child.remove()

    num = random.randint(1, len(block.children)) 
    selected = block.children[num - 1]

    page = client.get_block("https://www.notion.so/larskarbo/Random-976529219dde4b9bb66260b55b3f8a4f")

    newchild = page.children.add_new(TextBlock, title=("**" + selected.title + "**"))
    if len(selected.children):
      for child in selected.children:
        newchild.children.add_new(TextBlock, title=child.title)
    newchild.children.add_new(TextBlock, title="")
    newchild.move_to(targetBlock, "last-child")

    



    # driver.quit()
        

        


go()

