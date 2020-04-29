import os

def get_ipa(w):
  horse = os.popen("./dictionary " + w).read()
  try:
    wrd = horse.split("|")[1]
    return wrd
  except Exception as e:
    print("👎", e)
