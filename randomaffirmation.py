

import random


import requests


text = random.choice([
"E e autentisk og meg sjøl på TikTok, har det gøy og på den måten tiltrekk meg likesinna folk.",
"E kjem til å være en kjent person — en autoritet — online",
"Det kan hende dei 10 første prosjekta mine går rett til helvette. Men stå i det og bad i kritikken."
])
requests.get("https://api.telegram.org/bot1196576929:AAFCVPBTMcSUlrHAIFBO_Ni7e9em0Nje10U/sendMessage?chat_id=912275377&text=" + text)

