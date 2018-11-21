#!/usr/bin/env python

import urllib2
import xml.etree.ElementTree as ET

FEED_URL = "https://macadmins.software/latest.xml"

try:
    raw_xml = urllib2.urlopen(FEED_URL)
    xml = raw_xml.read()
except BaseException as e:
    raise ProcessorError("Can't download %s: %s" % (FEED_URL, e))

entry = {}

csvfile = open("ms_products.csv", "w")
csvfile.write("Name,Version,Product ID\n")

root = ET.fromstring(xml)
for package in root.findall("package"):
    csvfile.write(package.find("title").text + "," + package.find("version").text + "," + package.find("download").text.split("=")[1] + "\n")

csvfile.close()