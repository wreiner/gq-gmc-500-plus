from flask import Flask
from flask import request
import time

app = Flask(__name__)

class GMCValues():
    def __init__(self):
        self.cpm = 0
        self.acpm = 0
        self.uSV = 0
        self.report_timestamp = time.time()

    def set_values(self, cpm, acpm, uSV):
        print(f"{time.time()} CPM: {cpm} | ACPM: {acpm} | uSV: {uSV}")

        self.cpm = cpm
        self.acpm = acpm
        self.uSV = uSV
        self.report_timestamp = time.time()

    def print_values_metric(self):
        line = "# HELP count_per_minute_cpm Radiation in count per minute\n"
        line += "# TYPE count_per_minute_cpm gauge\n"
        line += f"count_per_minute_cpm {self.cpm}\n"
        line += "# HELP average_count_per_minute_cpm Radiation in average count per minute\n"
        line += "# TYPE average_count_per_minute_cpm gauge\n"
        line += f"average_count_per_minute_cpm {self.acpm}\n"
        line += "# HELP micro_sievert_usv Radiation in uSV\n"
        line += "# TYPE micro_sievert_usv gauge\n"
        line += f"micro_sievert_uSV {self.uSV}\n"
        line += "# HELP last_record_timestamp Timestamp of last measurement received\n"
        line += "# TYPE last_record_timestamp gauge\n"
        line += f"last_record_timestamp {self.report_timestamp}\n"
        return line


gmcv = GMCValues()

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