# This file will contain the parsing logic to get all <w:t> and <w:tbl> elements from a Word document
import xml.etree.ElementTree as ET

tree = ET.parse('document.xml')
root = tree.getroot()
list = []

for item in root.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"):
    if item.text:
        list.append(item.text)

print("".join(list))