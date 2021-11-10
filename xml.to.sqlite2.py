#!/usr/bin/env python3

import xmltodict
import sqlite3

xmlfile = "/home/tpasturel/Desktop/CCDD/InputFile"
dbfile = "/home/tpasturel/Desktop/CCDD/ccdd"

conn = sqlite3.connect(dbfile)
c = conn.cursor()

with open(xmlfile) as fd:
    obj = xmltodict.parse(fd.read())
    print(obj['concept']['id'])
    print(obj)

#c.execute("INSERT INTO therapeutic_moiety '?' VALUES '?'", [column["@name"], column["#text"]])

#print(obj['concept'])

#for tag, value in obj['concept'], obj:
 #   print(tag, value)
    #c.execute("INSERT INTO therapeutic_moiety '?' VALUES '?'", [column["@name"], column["#text"]])
    #print("item inserted \n")