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


__all__ = ["OfficeExtrasDetailsProvider"]

FEED_URL = "https://macadmins.software/latest.xml"

class OfficeExtrasDetailsProvider(Processor):
    """Provides the details of additional products associated with Office"""
    input_variables = {
        "product": {
            "required": True,
            "default": "OneNote",
            "description": "The product required.  Acceptable values are: 'OneNote', 'OneDrive', 'SkypeforBusiness', 'Teams', 'Intune', 'RemoteDesktop', 'MAU'.",
        },
    }
    output_variables = {
        "version": {
            "description": "Version number of the selected Office product.",
        },
        "download_url": {
            "description": "The URL used to download the Office product required.",
        },
        "office_extras_details_summary_result": {
            "description": "Summary of the product details found.",
        }
    }
    description = __doc__
    
    def get_longproduct(self, shortproduct):
        switcher = {
            "OneNote": "onenote.standalone.365",
            "OneDrive": "onedrive.standalone",
            "SkypeforBusiness": "skypeforbusiness.standalone",
            "Teams": "teams.standalone",
            "InTune": "intunecompanyportal.standalone",
            "RemoteDesktop": "remotedesktop.standalone",
            "MAU": "autoupdate.standalone",
        }
        return switcher.get(shortproduct, "onenote.standalone.365")
    
    def get_packagedetails(self, FEED_URL):
        """Parse the macadmins.software/latest.xml feed for the product download url and minimum os value"""
        try:
            raw_xml = urllib2.urlopen(FEED_URL)
            xml = raw_xml.read()
        except BaseException as e:
            raise ProcessorError("Can't download %s: %s" % (FEED_URL, e))
        version = ""
        download_url = ""
        longproduct = self.get_longproduct(self.env["product"])
        root = ET.fromstring(xml)
        for package in root.findall("package"):
            if package.find("id").text == "com.microsoft." + longproduct:
                version = package.find("version").text
                download_url = package.find("download").text
                minimum_os_ver = package.find("min_os").text
                break
        self.env["version"] = version.split()[0]
        self.env["download_url"] = download_url
        self.env["office_extras_details_summary_result"] = {
            "summary_text": "The following details were found:",
            "report_fields": ["product", "version", "download_url"],
            "data": {
                "product": self.env["product"],
                "version": version,
                "download_url": download_url,
            }
        }
    
    def main(self):
        self.get_packagedetails(FEED_URL)
        
if __name__ == "__main__":
    processor = OfficeExtrasDetailsProvider()
    processor.execute_shell()
