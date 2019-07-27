from notion.client import NotionClient
import random
import json
from anki import addNote, printStats
import markdown
from random import randint

from progress.bar import Bar


def hello():
    client = NotionClient(
        token_v2="738991375dbb49e1050ead92da668fb277c43c6df82f1dd49b6e667a3d83a8da738051a0a7d489d04dccaa043b81e6d196beaa11f7e6a4e233a96491391d13337a9fbc7a2911f6a9f9a4452f1192")

    cv = client.get_collection_view(
        "https://www.notion.so/larskarbo/534d0728c32d474c9d23315d8afc82d5?v=f8eed84cbef6437ca18f9506f8469fe4")

    rows = cv.collection.get_rows()

    for i in range(5):
        nums = []

        rand = rows[randint(-1, len(rows)-1)]
        p = rand.person
        nums.append(rand.name)

        rand = rows[randint(-1, len(rows)-1)]
        h = rand.handling
        nums.append(rand.name)

        rand = rows[randint(-1, len(rows)-1)]
        o = rand.objekt
        nums.append(rand.name)


        print("{} {} på {}".format(p, h.lower(), o.lower()))
        val = input("Enter your value: ")
        if val[0:2] == nums[0] and val[2:4] == nums[1] and val[4:6] == nums[2]:
            print("hurray!!")
        else:
            print("wrong")
            print(val)
        print(nums)







hello()
