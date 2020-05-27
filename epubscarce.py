
#%%
# %reload_ext autoreload
# %autoreload 2
from notion.client import NotionClient
from notion.block import TextBlock, ImageBlock
import random
import os
import requests
import shutil
from datetime import datetime, date
import glob

library = os.path.expanduser("~") + "/Library/Mobile Documents/iCloud~com~apple~iBooks/Documents/"
#%%

client = NotionClient(token_v2=os.environ["NOTION_TOKEN"])

cv = client.get_collection_view(
    "https://www.notion.so/larskarbo/f2092f7d6c3648829ff60158cbc26d02?v=229aab90249741ec84abc517a4d3abfc")

rows = cv.collection.get_rows()
# %%
startdate = date(2020, 5, 5)
today = date.today()  # get todays date
diff = today - startdate
weeknumber = (diff.days//7) + 1
print("You are on week " + str(weeknumber))

def remove(path):
    """ param <path> could either be relative or absolute. """
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)  # remove the file
    elif os.path.isdir(path):
        shutil.rmtree(path)  # remove dir and all contains
    else:
        raise ValueError("file {} is not a file or dir.".format(path))

#%%
i = 1
for row in rows:
    if "scarce" in row.tags:
        print(row.title)
        files = glob.glob('scarceproject/'+row.title+"/*.epub")
        files.sort()
        # todo handle week number 1

        filetodelete = files[weeknumber - 2]
        print('filetodelete: ', filetodelete)
        newfile = files[weeknumber - 1]
        print('newfile: ', newfile)

        remove(library + filetodelete.split("/")[-1])
        shutil.copyfile(newfile, library + newfile.split("/")[-1])
        row.scarcestatus = str(weeknumber) + " / " + str(len(files))
        row.scarcetag = "notread"
