from notion.client import NotionClient
import notion
import random
import json
from notionHelpers import blockToHTML
import markdown
import os
import random
from pyquery import PyQuery as pq
from progress.bar import Bar
import csv



def getProp(lst, str):
    matchingTel = [s for s in lst if str in s]
    if len(matchingTel):
        tel = matchingTel[0].split(":", 1)[1]
        d = pq(tel)
        return d.text().replace(",", "·")
    return ""

def go():
    # client = NotionClient(token_v2=os.environ["NOTION_TOKEN"])
    # cv = client.get_collection_view(
     #   "https://www.notion.so/larskarbo/44bb6987ee86404dac44d16c68e3fc1e?v=67bf67c08de745cd90d94531f7059624")
    endcsv = "Name,People,Address,Tel,Email,Website,Strategy"
    with open('dataminer (7).csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                endcsv += "\n"
                info = row[1]
                infolist = info.split("<br>")
                print('infolist: ', infolist)

                name = infolist[1].replace(",", "·")
                endcsv += name + ","
                people = infolist[0].replace(",", "·")
                endcsv += people + ","

                name = infolist[0]

                spacerIndex = infolist.index("")
                address = " · ".join(infolist[1:spacerIndex]).replace(",", "·")
                endcsv += address + ","
                tel = "+49 " + getProp(infolist, "Telefon")
                endcsv += tel + ","
                mail = getProp(infolist, "E-Mail")
                endcsv += mail + ","
                web = getProp(infolist, "Internet")
                endcsv += web + ","
                #print('matching: ', matching)
                endcsv += random.choice(["Group 1", "Group 2", "Group 3", "Group 4"])
                line_count += 1
                

                # newchild = row.children.add_new(TextBlock, title=d[0] if len(d[0]) else "Samtalelogg")
                # newchild.children.add_new(TextBlock, title=d[4])
        print(f'Processed {line_count} lines.')

        print(endcsv)

        f=open("outcsv.csv","w+")
        f.write(endcsv)
        f.close()



go()

