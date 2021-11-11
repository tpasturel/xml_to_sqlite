#!/usr/bin/env python3

import sqlite3
import xml.etree.ElementTree as ET
from xml.dom.minidom import parse, parseString
from lxml import etree
import re, itertools, sys

therapeutic_moiety_input = "/home/tpasturel/Desktop/PythonScripts/CCDD/Therapeutic_Moiety_20211012.xml"
non_proprietary_therapeutic_product = "/home/tpasturel/Desktop/PythonScripts/CCDD/Non_Proprietary_Therapeutic_Product_20211012.xml"
manufactured_product = "/home/tpasturel/Desktop/PythonScripts/CCDD/Manufactured_Product_MP_20211105.xml"
sqlite_dbfile = "/home/tpasturel/Desktop/PythonScripts/CCDD/ccdd"

# Creating the sqlite DB and tables
conn = sqlite3.connect('ccdd.db')
cur = conn.cursor()

_tm = "CREATE TABLE IF NOT EXISTS therapeutic_moiety (\
    id INTEGER PRIMARY KEY,\
    name TEXT,\
    code_system_id TEXT,\
    code_system_name TEXT,\
    display_name TEXT,\
    description TEXT,\
    active INTEGER,\
    tm_status TEXT,\
    tm_status_effective_time TEXT)"

_ntp = "CREATE TABLE IF NOT EXISTS non_proprietary_therapeutic_product (\
     id INTEGER PRIMARY KEY,\
     name TEXT,\
     code_system_id TEXT,\
     code_system_name TEXT,\
     display_name_en TEXT,\
     display_name_fr TEXT,\
     description TEXT,\
     active INTEGER)"

_mp = "CREATE TABLE IF NOT EXISTS manufactured_product (\
     id INTEGER PRIMARY KEY,\
     name TEXT,\
     code_system_id TEXT,\
     code_system_name TEXT,\
     display_name_en TEXT,\
     display_name_fr TEXT,\
     description TEXT,\
     active INTEGER)"

def create_ccdd_tables():
    create_tables = [ _tm , _ntp, _mp ]
    for table in create_tables:
        try:
            cur.execute(table)
        except sqlite3.OperationalError as e:
            pass
        conn.commit()

# Parsing the xml input files and setting all rows to lists
def get_tm_rows():
    tm_tree = ET.parse(therapeutic_moiety_input)
    tm_root = tm_tree.getroot()
    tm_tags = []
    tm_rows = []
    tm_status = []
    tm_status_effective_time = []
    for value in tm_root.findall('./concepts/concept/'):
        tm_tags.append(value.tag)
    for each in tm_root.findall('.//concept'):
        row = []
        for x in range (0, 9):
            value = each.find('.//%s' %tm_tags[x])
            row.append(value.text)
        tm_rows.append(row)
    
    #Dealing with tm_status and tm_status_effective_time values nested under the string element 
    for each in tm_root.findall('./concepts/concept/properties/entry/string'):
        if 'tm_status' not in each.text:
            if each.text.isdecimal():
                tm_status_effective_time.append(each.text)
            else:
                tm_status.append(each.text)
    for list in tm_rows:
        for tm, tset in zip(tm_status, tm_status_effective_time):
            list[7] = tm
            list[8] = tset
    return tm_rows

def get_nptp_rows():
    ntpt_tree = ET.parse(non_proprietary_therapeutic_product)
    ntpt_root = ntpt_tree.getroot()
    ntpt_tags = []
    ntpt_rows = []
    for value in ntpt_root.findall('./concepts/concept/'):
        ntpt_tags.append(value.tag)
    for each in ntpt_root.findall('.//concept'):
        row = []
        for x in range (0, 8):
            value = each.find('.//%s' %ntpt_tags[x])
            row.append(value.text)
        ntpt_rows.append(row)
    return ntpt_rows

def get_mp_rows():
    mp_tree = ET.parse(manufactured_product)
    mp_root = mp_tree.getroot()
    mp_tags = []
    mp_rows = []
    for value in mp_root.findall('./concepts/concept/'):
        mp_tags.append(value.tag)
    for each in mp_root.findall('.//concept'):
        row = []
        for x in range (0, 8):
            try:
                value = each.find('.//%s' %mp_tags[x])
                row.append(value.text)
            except AttributeError:
                row.append('None')    
        mp_rows.append(row)
    return mp_rows
    

# Populating the sqlite DB
def sql_insert_statements():
        tm_sql_statement = 'INSERT INTO therapeutic_moiety VALUES (?,?,?,?,?,?,?,?,?);'
        cur.executemany(tm_sql_statement, get_tm_rows())
        ntpt_sql_statement = 'INSERT INTO non_proprietary_therapeutic_product VALUES (?,?,?,?,?,?,?,?);'
        cur.executemany(ntpt_sql_statement, get_nptp_rows())
        mp_sql_statement = 'INSERT INTO manufactured_product VALUES (?,?,?,?,?,?,?,?);'
        cur.executemany(mp_sql_statement, get_mp_rows())
        conn.commit()
        conn.close()
  
def insert_into_sqlite():
    print("Populating ccdd sqlite db...\n")
    try:
        sql_insert_statements()
    except sqlite3.IntegrityError:
        print("The ccdd sqliteDB already exists and some tables where already populated with this data")
    finally: 
        next_step = input('Do you want to drop that existing table? y/n \n')
        if next_step == 'y':
            cur.execute('''DROP TABLE therapeutic_moiety''')
            cur.execute('''DROP TABLE non_proprietary_therapeutic_product''')
            cur.execute('''DROP TABLE manufactured_product''')
            create_ccdd_tables()
            sql_insert_statements()
        else:
            print('Not importing the data. Exiting...')

def main():
    create_ccdd_tables()
    insert_into_sqlite()

if __name__ == '__main__':
    main()
