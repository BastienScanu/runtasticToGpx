import os
import json
from datetime import datetime
import xml.etree.ElementTree as ET


def processActivity (file):
    with open('./data/Sport-sessions/' + file) as jsonFile:
        try:
            data = json.load(jsonFile)
            json.dumps(data, indent=4)
            time = data["start_time"]
            name = data.get("notes") or "Course"
            points = []
            try:
                with open('./data/Sport-sessions/GPS-data/' + file) as gpsFile:
                    try:
                        gpsData = json.load(gpsFile)
                        for point in gpsData:
                            obj = dict()
                            obj["lat"] = str(point["latitude"])
                            obj["lon"] = str(point["longitude"])
                            obj["time"] = str(point["timestamp"])
                            obj["ele"] = str(point["altitude"])
                            points.append(obj)
                        buildGpx(time, name, points, file)
                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)

def indent(elem, level=0):
  i = "\n" + level*"  "
  if len(elem):
    if not elem.text or not elem.text.strip():
      elem.text = i + "  "
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
    for elem in elem:
      indent(elem, level+1)
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
  else:
    if level and (not elem.tail or not elem.tail.strip()):
      elem.tail = i

def fTime(date):
    return datetime.strftime(datetime.utcfromtimestamp(datetime.timestamp(datetime.strptime(date, "%Y-%m-%d %H:%M:%S %z"))), "%Y-%m-%dT%H:%M:%SZ")


def buildGpx (date, name, points, id):
    gpx = ET.Element("gpx")
    gpx.set("creator", "StravaGPX Android")
    gpx.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    gpx.set("xsi:schemaLocation", "http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd")
    gpx.set("version", "1.1")
    gpx.set("xmlns", "http://www.topografix.com/GPX/1/1")
    metadata = ET.SubElement(gpx, "metadata")
    time = ET.SubElement(metadata, "time")
    time.text = datetime.strftime(datetime.utcfromtimestamp(date/1000), "%Y-%m-%dT%H:%M:%SZ")
    track = ET.SubElement(gpx, "trk")
    title = ET.SubElement(track, "name")
    title.text = name
    type = ET.SubElement(track, "type")
    type.text = "9"
    trkseg = ET.SubElement(track, "trkseg")
    for point in points:
        trkpt = ET.SubElement(trkseg, "trkpt")
        trkpt.set("lat", point["lat"])
        trkpt.set("lon", point["lon"])
        ele = ET.SubElement(trkpt, "ele")
        ele.text = point["ele"]
        subTime = ET.SubElement(trkpt, "time")
        subTime.text = fTime(point["time"])
    indent(gpx)
    ET.ElementTree(gpx).write(id + '.gpx', xml_declaration=True, encoding='utf-8', method="xml")



for root, dirs, files in os.walk('./data/Sport-sessions'):
    for file in files:
        processActivity(file)