#!/usr/bin/env python
#
# Copyright 2018 Mike Dowler, based on work by Allister Banks and Hannes Juutilainen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import urllib2
import xml.etree.ElementTree as ET

from autopkglib import Processor, ProcessorError


__all__ = ["OfficeDetailsProvider"]

FEED_URL = "https://macadmins.software/latest.xml"

class OfficeDetailsProvider(Processor):
    """Provides the details of products from the latest Office release"""
    input_variables = {
        "edition": {
            "required": True,
            "default": "365",
            "description": "The edition of Office required.  Either '365' or '2016'.",
        },
        "product": {
            "required": True,
            "default": "Office",
            "description": "The product required.  Acceptable values are: 'Office', 'Word', 'Excel', 'Powerpoint', and 'Outlook'.",
        },
    }
    output_variables = {
        "version": {
            "description": "Version number of the latest Office Suite release.",
        },
        "download_url": {
            "description": "The URL used to download the Office Suite required.",
        },
        "office_details_summary_results": {
            "description": "Summary of the recipe outcome",
        },
    }
    description = __doc__
    
    def get_longedition(self, shortedition):
        switcher = {
            "365": "o365",
            "2016": "vl2016",
        }
        return switcher.get(shortedition, "o365")
    
    def get_longproduct(self, shortproduct):
        switcher = {
            "Office": "office.suite",
            "Word": "word.standalone",
            "Excel": "excel.standalone",
            "Powerpoint": "powerpoint.standalone",
            "Outlook": "outlook.standalone",
        }
        return switcher.get(shortproduct, "office.suite")
    
    def get_version(self, FEED_URL):
        """Parse the macadmins.software/latest.xml feed for the latest Office Suite version number"""
        try:
            raw_xml = urllib2.urlopen(FEED_URL)
            xml = raw_xml.read()
        except BaseException as e:
            raise ProcessorError("Can't download %s: %s" % (FEED_URL, e))
        version = ""
        longedition = self.get_longedition(self.env["edition"])
        root = ET.fromstring(xml)
        version = root.find(longedition).text
        self.env["version"] = version
    
    def get_packagedetails(self, FEED_URL):
        """Parse the macadmins.software/latest.xml feed for the product download url and minimum os value"""
        try:
            raw_xml = urllib2.urlopen(FEED_URL)
            xml = raw_xml.read()
        except BaseException as e:
            raise ProcessorError("Can't download %s: %s" % (FEED_URL, e))
        download_url = ""
        longproduct = self.get_longproduct(self.env["product"])
        root = ET.fromstring(xml)
        for package in root.findall("package"):
            if package.find("id").text == "com.microsoft." + longproduct + "." + self.env["edition"]:
                download_url = package.find("download").text
                break
        
        self.env["download_url"] = download_url
        self.env["office_details_summary_results"] = {
            "summary_text": "The following details were found:",
            "report_fields": ["product", "edition", "version", "URL"],
            "data": {
                "product": self.env["product"],
                "edition": self.env["edition"],
                "version": self.env["version"],
                "URL": download_url,
            },
        }
    
    def main(self):
        self.get_version(FEED_URL)
        self.get_packagedetails(FEED_URL)
        
if __name__ == "__main__":
    processor = OfficeDetailsProvider()
    processor.execute_shell()
