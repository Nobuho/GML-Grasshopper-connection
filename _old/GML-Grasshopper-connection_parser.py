from lxml import etree
import csv
import codecs
import re
from bs4 import BeautifulSoup


gml_filepath = "GML_files\A29-11_27_GML\A29-11_27.xml"
with open(gml_filepath, encoding="utf-8_sig") as doc:
    soup = BeautifulSoup(doc, "xml")

cod_dict_list = []

cod_elms = soup.find_all("gml:posList")
curve_ids = soup.find_all("gml:Curve")

for i in range(len(cod_elms)):
    cod_dict = {}
    x_cod = cod_elms[i].string.split()[0::2]
    y_cod = cod_elms[i].string.split()[1::2]
    curve_id = curve_ids[i]["gml:id"]

    cod_dict["s_id"] = curve_id
    cod_dict["x"] = x_cod
    cod_dict["y"] = y_cod

    cod_dict_list.append(cod_dict)

print(cod_dict_list[0])

# ##################################################
# making property list
# ##################################################

# This csv is just mapping list between classification and property.
# You need to combine these two list based on this mapping table.
