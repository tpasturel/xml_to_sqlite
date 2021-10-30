import os, sqlite3
import xml.etree.ElementTree as ET
from xml.dom.minidom import parse, parseString


xmlfile = "C:\\Users\\thiba\\Desktop\\CCDD\\Sample_Therapeutic_Moiety_(TM)_20211012.xml"
tree = ET.parse(xmlfile)
root = tree.getroot()

for child in root:
    print(child.tag, child.text)
    