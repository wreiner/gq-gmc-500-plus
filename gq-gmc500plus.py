import argparse
import json
import requests
import time
import sys

from flask import Flask
from flask import request
from os.path import exists


class GMCValues():
    def __init__(self):
        self.config = None
        self.cpm = 0
        self.acpm = 0
        self.uSV = 0
        self.report_timestamp = time.time()

        config_file = "/etc/gq-gmc500plus.json"

        if exists(config_file):
            self.read_config(config_file)

    def set_values(self, cpm, acpm, uSV):
        print(f"{time.time()} CPM: {cpm} | ACPM: {acpm} | uSV: {uSV}")

        self.cpm = cpm
        self.acpm = acpm
        self.uSV = uSV
        self.report_timestamp = time.time()

        if self.config != None:
            self.publish_measurement()

    # https://www.gmcmap.com/AutomaticallySubmitData.asp
    def publish_measurement(self):
        payload = {
            "AID": self.config["account_id"],
            "GID": self.config["device_id"],
            "cpm": self.cpm,
            "acpm": self.acpm,
            "uSV": self.uSV,
        }
        response = requests.get(GMCMAP_URL, params=payload)
        print(response)
        print(response.status_code)

    def read_config(self, configfile):
        try:
            with open(configfile, "r") as jsonfile:
                self.config = json.load(jsonfile)
        except FileNotFoundError as fnferror:
            print("Error in parsing config file {}".format(fnferror))
            sys.exit(1)
        except PermissionError as permerror:
            print("Error in parsing config file {}".format(permerror))
            sys.exit(1)

    def print_values_metric(self):
        line = "# HELP gmcradiation_count_per_minute_cpm Radiation in count per minute\n"
        line += "# TYPE gmcradiation_count_per_minute_cpm gauge\n"
        line += f"gmcradiation_count_per_minute_cpm {self.cpm}\n"
        line += "# HELP gmcradiation_average_count_per_minute_cpm Radiation in average count per minute\n"
        line += "# TYPE gmcradiation_average_count_per_minute_cpm gauge\n"
        line += f"gmcradiation_average_count_per_minute_cpm {self.acpm}\n"
        line += "# HELP gmcradiation_micro_sievert_usv Radiation in uSV\n"
        line += "# TYPE gmcradiation_micro_sievert_usv gauge\n"
        line += f"gmcradiation_micro_sievert_uSV {self.uSV}\n"
        line += "# HELP last_record_timestamp Timestamp of last measurement received\n"
        line += "# TYPE last_record_timestamp gauge\n"
        line += f"gmcradiation_last_record_timestamp {self.report_timestamp}\n"
        return line


GMCMAP_URL = "http://www.gmcmap.com/log2.asp"
gmcv = GMCValues()
app = Flask(__name__)

@app.route("/u")
def uu():
    print(request.headers)
    gmcv.set_values(
        request.args.get('CPM'),
        request.args.get('ACPM'),
        request.args.get('uSV'))

    return "Values stored."

@app.route("/metrics")
def metrics():
    return gmcv.print_values_metric()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# www.gmcmap.com
# log2.asp
# /u?AID=&GID=&CPM=16&ACPM=22.64&uSV=0.10
# 192.168.2.136 - - [09/Apr/2023 17:38:05] "GET /u?AID=&GID=&CPM=21&ACPM=21.55&uSV=0.14 HTTP/1.1" 200 -
# 192.168.2.136 - - [09/Apr/2023 17:43:07] "GET /u?AID=&GID=&CPM=14&ACPM=21.86&uSV=0.09 HTTP/1.1" 200 -
# 192.168.2.136 - - [09/Apr/2023 17:48:09] "GET /u?AID=&GID=&CPM=31&ACPM=22.10&uSV=0.20 HTTP/1.1" 200 -
# 192.168.2.136 - - [09/Apr/2023 17:53:11] "GET /u?AID=&GID=&CPM=25&ACPM=22.18&uSV=0.16 HTTP/1.1" 200 -
