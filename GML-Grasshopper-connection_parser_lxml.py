from lxml import etree
import csv


def join_list2gh(listitem):
    list_1 = []
    for i in listitem:
        list_1.append(",".join(map(str, i)))
    flatten = "+".join(list_1)
    return flatten


gml_filepath = "GML_files\A29-11_40_GML\A29-11_40.xml"

# ##################################################
# delete invalid xmlns
# ##################################################

with open(gml_filepath, "r", encoding="utf-8_sig") as f:
    gml_data = f.read()

gml_data = gml_data.replace(
    "xmlns:schemaLocation=\"http://nlftp.mlit.go.jp/ksj/schemas/ksj-app KsjAppSchema-A29-v1_0.xsd\"", "")

with open(gml_filepath, "w", encoding="utf-8_sig") as f:
    f.write(gml_data)

# ##################################################
# making property list
# ##################################################

tree = etree.parse(gml_filepath)
root = tree.getroot()

mynsmap = {}
mynsmap = root.nsmap
# need define xml name apce again to ue lxml

crv_id = [i.attrib["{http://www.opengis.net/gml/3.2}id"]
          for i in root.iterfind('gml:Curve', namespaces=mynsmap)]
crv_pt_x = [i.text.split()[0::2] for i in root.iterfind(
    'gml:Curve/gml:segments/gml:LineStringSegment/gml:posList', namespaces=mynsmap)]
crv_pt_y = [i.text.split()[1::2] for i in root.iterfind(
    'gml:Curve/gml:segments/gml:LineStringSegment/gml:posList', namespaces=mynsmap)]

srf_id = [i.attrib["{http://www.opengis.net/gml/3.2}id"]
          for i in root.iterfind('gml:Surface', namespaces=mynsmap)]
# srf_ex_crv_id = [i.attrib["{http://www.w3.org/1999/xlink}href"].replace("#", "")
#                  for i in root.iterfind('gml:Surface/gml:patches/gml:PolygonPatch/gml:exterior/gml:Ring/gml:curveMember', namespaces=mynsmap)]
# srf_in_crv_id = [i.attrib["{http://www.w3.org/1999/xlink}href"].replace("#", "")
#                  for i in root.iterfind('gml:Surface/gml:patches/gml:PolygonPatch/gml:interior/gml:Ring/gml:curveMember', namespaces=mynsmap)]

srf = [i for i in root.iterfind('gml:Surface', namespaces=mynsmap)]

srf_ex_elm = [i.findall(
    "gml:patches/gml:PolygonPatch/gml:exterior/gml:Ring/gml:curveMember", namespaces=mynsmap) for i in srf]
srf_ex_crv_id = [[n.attrib["{http://www.w3.org/1999/xlink}href"]
                  .replace("#", "") for n in i] for i in srf_ex_elm]

srf_in_elm = [i.findall(
    "gml:patches/gml:PolygonPatch/gml:interior/gml:Ring/gml:curveMember", namespaces=mynsmap) for i in srf]
srf_in_crv_id = [[n.attrib["{http://www.w3.org/1999/xlink}href"]
                  .replace("#", "") for n in i] for i in srf_in_elm]

area_id = [i.attrib["{http://www.w3.org/1999/xlink}href"].replace("#", "")
           for i in root.iterfind('ksj:DesignatedArea/ksj:cda', namespaces=mynsmap)]
area_aac = [i.text for i in root.iterfind(
    'ksj:DesignatedArea/ksj:aac', namespaces=mynsmap)]
area_pfn = [i.text for i in root.iterfind(
    'ksj:DesignatedArea/ksj:pfn', namespaces=mynsmap)]
area_lgn = [i.text for i in root.iterfind(
    'ksj:DesignatedArea/ksj:lgn', namespaces=mynsmap)]
area_dac = [i.text for i in root.iterfind(
    'ksj:DesignatedArea/ksj:dac', namespaces=mynsmap)]
area_kda = [i.text for i in root.iterfind(
    'ksj:DesignatedArea/ksj:kda', namespaces=mynsmap)]
area_bar = [i.text for i in root.iterfind(
    'ksj:DesignatedArea/ksj:bar', namespaces=mynsmap)]
area_cbr = [i.text for i in root.iterfind(
    'ksj:DesignatedArea/ksj:cbr', namespaces=mynsmap)]
area_src = [i.text for i in root.iterfind(
    'ksj:DesignatedArea/ksj:src', namespaces=mynsmap)]

crv_ditc = {key: {"x": ptx, "y": ptx}
            for key, ptx, pty in zip(crv_id, crv_pt_x, crv_pt_y)}

srf_ditc = {key: {"ex": exc, "in": inc}
            for key, exc, inc in zip(srf_id, srf_ex_crv_id, srf_in_crv_id)}

with open('points_id.csv', 'w',  newline='') as f:
    writer = csv.writer(f)
    writer.writerow(crv_id)

with open('points_x.csv', 'w',  newline='') as f:
    writer = csv.writer(f)
    writer.writerows(crv_pt_x)

with open('points_y.csv', 'w',  newline='') as f:
    writer = csv.writer(f)
    writer.writerows(crv_pt_y)

# --------------------------------------------------------------

with open('srf_id.csv', 'w',  newline='') as f:
    writer = csv.writer(f)
    writer.writerow(srf_id)

with open('srf_ex_crv_id.csv', 'w',  newline='') as f:
    writer = csv.writer(f)
    writer.writerows(srf_ex_crv_id)

with open('srf_in_crv_id.csv', 'w',  newline='') as f:
    writer = csv.writer(f)
    writer.writerows(srf_in_crv_id)

# --------------------------------------------------------------

with open('area_用途地域.csv', 'w', encoding="utf-8_sig", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(area_kda)

with open('area_建ぺい率.csv', 'w',  newline='') as f:
    writer = csv.writer(f)
    writer.writerow(area_bar)

with open('area_容積率.csv', 'w',  newline='') as f:
    writer = csv.writer(f)
    writer.writerow(area_cbr)

# --------------------------------------------------------------

print("end")
