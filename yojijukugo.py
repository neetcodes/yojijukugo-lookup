#!/bin/python3
import sys
import os
import os.path

cache = "/home/msg/.cache/yojijukugo/"
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
def getentry(word, showreading=True):
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

    if os.path.isfile(cache + word):
        with open(cache + word,'r') as f:
            if showreading:
                return(f.read())
            else:
                text = f.read()
                return(text[text.find("\n"):])
    else:
        import requests
        from bs4 import BeautifulSoup
        import re
        headers = requests.utils.default_headers()
        headers.update({'User-Agent': useragent,})
        url = "https://yoji.jitenon.jp/cat/search.php?getdata={}&search=contain".format(word)
        try:
            req = requests.get(url, headers=headers)
        except:
            print("lol")
            return("")
        soup = BeautifulSoup(req.text, 'lxml')
        mainarea = soup.find("table", {"class": "kanjirighttb"})
        if mainarea != None:
            reading = mainarea.find("th", string="読み方").find_next_sibling("td").text.replace("\r","")
            defin  = mainarea.find("th", string="意味").find_next_sibling("td").text.replace("\r","")
            with open(cache + word, 'w') as f:
                f.write(reading + "\n" + defin)
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
