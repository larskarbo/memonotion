import os
from anki import invoke
words ="sol,chevaux,verb,corps,embrasser,je,voiture,vêtement,garderobe".split(",")
# words ="je,suis"
donewords = []

def checkAnki():
  words = []
  f=open("out.txt", "r")
  if f.mode == 'r':
    for line in f:
      for word in line.split():
        words.append(word)
  print(len(words))
  notes = []
  
  for w in words:
    notes.append({
      "deckName": "French",
      "modelName": "2. Picture Words",
      "fields": {
        "Word": w,
      },
      "tags": [
          "asdf"
      ]
    })
  h = invoke("canAddNotes", notes=notes)
  print('h: ', h)
  i = 0
  for w in words:
    if not h[i]:
      print(w + " is in anki ✅")
    i+=1


checkAnki()

def parsewords():
  os.system("echo " + " > out.txt")
  words = []
  f=open("hp1.txt", "r")
  if f.mode == 'r':
    for line in f:
      for word in line.split():
        words.append(word)

  for w in words:
    horse = os.popen("./dictionary " + w).read()
    # print("🔭🔭🔭", word)
    # print('horse: ', horse)
    try:
      wrd = horse.split("|")[0].split(" ")[0]
      wrd.replace(",","")
      if wrd in donewords:
        continue
      donewords.append(wrd)
      st = wrd# + " " + horse.split("|")[1]+ ""
      horse = os.popen("echo \"" + st + "\" >> out.txt").read()
    except Exception as e:
      print("👎", e, word)
    # print('"./dictionary " + w + " > out.txt": ', "./dictionary " + w + " > out.txt")