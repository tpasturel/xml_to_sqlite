#!/usr/bin/env python3

import sqlite3
import xml.etree.ElementTree as ET
from xml.dom.minidom import parse, parseString
import xmltodict

xmlfile = "/home/tpasturel/Desktop/CCDD/InputFile"
dbfile = "/home/tpasturel/Desktop/CCDD/ccdd"

_therapeutic_moiety = "CREATE TABLE therapeutic_moiety("\
        "id INTEGER PRIMARY KEY,"\
        "name TEXT,"\
        "code_system_id TEXT,"\
        "code_system_name TEXT,"\
        "display_name TEXT,"\
        "description TEXT,"\
        "active INTEGER,"\
        "subsets TEXT,"\
        "associations TEXT,"\
        #"properties TEXT)"

create_tables = [ _therapeutic_moiety ]
##create_tables = [ _therapeutic_moiety, _colorramp, _tag, _tagmap, _symgroup ]

# Create the DB with required Schema
conn = sqlite3.connect(dbfile)
c = conn.cursor()
print("Creating tables in the Database\n")
for table in create_tables:
    try:
        c.execute(table)
        #print(table)
    except sqlite3.OperationalError as e:
        pass
    conn.commit()

# parse the XML file &  write therapeutic_moiety into DB
tree = ET.parse(xmlfile)
root = tree.getroot()
rows = []
for child in root:
    rows.append(child.text)
print(rows)
    #id = root[0]
    #name = root[1]
    #code_system_id = root[2]
    #code_system_name = root[3]
    #display_name = root[4]
    #description = root[5]
    #active = root[6]
    #subsets = root [7]
    #associations = root[8]
    #properties = root[9]

rows = tree.findall('.//concept')
#for i in rows:
#    name = i.find('id').text
    #print(name)

#print(root.findall('.//concept'))

rows = tree.findall('*')
for row in rows:
#    print(row.tag, row.text)
    headers = [(row.tag) for row in rows]
#print(headers)

with open(xmlfile) as fd:
    obj = xmltodict.parse(fd.read())
    h1 = obj['concept']['id']
    h2 = obj['concept']['name']
    h3 = obj['concept']['codeSystemId']
    h4 = obj['concept']['codeSystemName']
    h5 = obj['concept']['frDisplayName']
    h6 = obj['concept']['frDescription']
    h7 = obj['concept']['active']
    h8 = obj['concept']['subsets']
    h9 = obj['concept']['associations']
    #h10 = obj['concept']['properties']
    print(h5, h6)
    #print(headers)
    #for header in headers:
        #value = obj['concept'][header]
        #print(obj['concept'][header])
        #print(value)
        #c.execute( "INSERT INTO therapeutic_moiety VALUES ()", ( None, therapeutic_moiety_name, therapeutic_moiety.toxml(), None ) )

#c.execute("INSERT INTO therapeutic_moiety VALUES (h1,h2,h3,h4,h5,h6,h7,h8,h9)", (id, name, code_system_id, code_system_name, display_name, description, active, subsets, associations))
#conn.commit()

#dom = parse(xmlfile)
#therapeutic_moietys = dom.getElementsByTagName( "concept" )
#for element in therapeutic_moietys:
#    elements = element.getAttribute( "name" )
#    print(elements)
#    if '@' in therapeutic_moiety_name:
#        parts = therapeutic_moiety_name.split('@')
#        parent_name = parts[1]
#        layerno = int(parts[2])
#        c.execute( "SELECT xml FROM therapeutic_moiety WHERE name=(?)", (parent_name,) )
#        symdom = parseString( c.fetchone()[0] ).getElementsByTagName( 'therapeutic_moiety' )[0]
#        symdom.getElementsByTagName( "layer" )[ layerno ].appendChild( therapeutic_moiety )
#        c.execute( "UPDATE therapeutic_moiety SET xml=? WHERE name=?", ( symdom.toxml(), parent_name ))
#    else:
#        c.execute( "INSERT INTO therapeutic_moiety VALUES (?,?,?,?)", ( None, therapeutic_moiety_name, therapeutic_moiety.toxml(), None ) )
#conn.commit()


# ColorRamps
#colorramps = dom.getElementsByTagName( "colorramp" )
#for ramp in colorramps:
#    ramp_name = ramp.getAttribute( "name" )
#    c.execute( "INSERT INTO colorramp VALUES (?,?,?)", ( None, ramp_name, ramp.toxml() ) )
#conn.commit()

# Finally close the sqlite cursor
c.close()