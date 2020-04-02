import pandas as pd
import re
import math
from email_scraper import scrape_emails
from pyquery import PyQuery as pq
df = pd.read_excel("nfbgermany.xlsx")
lst = df.values.tolist()
#   print(row)
endcsv = ""
for el in lst[1:]:
  if el[0]  == "stop":
    break
  mail = el[3].replace("(at)", "@")
  mail = mail.replace("(at) ", "@")
  mail = mail.replace("(at)<br> ", "@")
  lst = scrape_emails(mail)
  # print('lst: ', lst)
  if len(lst) == 0:
    continue

  d = pq(el[0])
  info = d.text().split("\n")
  endcsv += "\n" + info[0] + "," + lst.pop()
  # print('mail: ', mail)

f=open("outcsv.csv","w+")
f.write(endcsv)
f.close()