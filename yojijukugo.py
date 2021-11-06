#!/bin/python3
import sys
import os
import os.path
import requests
from bs4 import BeautifulSoup
import re

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
def getentry(word, showreading=True):
    # check if the input is in Japanese to eliminate unnecessary lookups
    japanese = False
    for char in word:
        o = ord(char)
        if (0x3000 <= o <= 0x303f) or\
           (0x3040 <= o <= 0x309f) or\
           (0x30a0 <= o <= 0x30ff) or\
           (0xff00 <= o <= 0xffef) or\
           (0x4e00 <= o <= 0x9faf) or\
           (0x3400 <= o <= 0x4dbf):
                japanese = True
                break
    if not japanese:
        return("")

    headers = requests.utils.default_headers()
    headers.update({'User-Agent': useragent,})
    url = "https://yoji.jitenon.jp/cat/search.php?getdata={}&search=contain".format(word)
    try:
        req = requests.get(url, headers=headers)
    except:
        print("Failed to connect", file=sys.stderr)
        return("")
    soup = BeautifulSoup(req.text, 'lxml')
    mainarea = soup.find("table", {"class": "kanjirighttb"})
    if mainarea != None:
        reading = mainarea.find("th", string="読み方").find_next_sibling("td").text.replace("\r","")
        defin  = mainarea.find("th", string="意味").find_next_sibling("td").text.replace("\r","")
        if showreading:
            return(reading + "\n" + defin)
        else:
            return(defin)
    return("")

if __name__ == "__main__":
    word = sys.argv[1]
    entry = getentry(word)
    if entry != None:
        print(entry)
