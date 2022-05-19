import re
from db import Db
import json

"""
for i, s in enumerate(sheet.rows):
    if "SIMAR" in s[5]:
        sheet.update_index(row=i+1, col=6, val=re.sub(r"IA[0-9][0-9]-", s[10], s[5]))

pylightxl.writexl(db=db, fn='spreadsheet/Redes e Beaglebones.xlsx')
"""

TYPES = {
    "Temp-Mon": "Temperature",
    "Pressure-Mon": "Pressure",
    "RackOpen-Mon": "Rack Open",
    "Humidity-Mon": "Humidity",
    "Voltage-Mon": "Voltage",
    "PwrFactor-Mon": "PFactor",
    "PwrFrequency-Mon": "Frequency",
    "Glitches-Mon": "Glitches",
    "WaterLeak-Mon": "Leak",
}

db = Db("./spreadsheet/Redes e Beaglebones.xlsx", "PVs Redis")

bases = {"items": {}}
last_sub_name = ""
for ip, board in db.data.items():
    base = {}
    index = -1
    if any(
        ["SIMAR" in device["PV"] and device["ENABLE"] == "True" for device in board]
    ):
        name = board[0]["Hostname"]
        if ip not in ["10.0.38.59", "10.0.38.46", "10.0.38.42"]:
            name += " - {}".format(ip)

        bases["items"][name] = []
    else:
        continue
    for device in board:
        if "SIMAR" in device["PV"] and device["ENABLE"] == "True":
            sub_name = device["PV"].split(":")[0]
            if sub_name != last_sub_name:
                device_name = device["Location"]
                if sub_name[0:2] in ["SI", "IA"]:
                    device_name += ", {}".format(sub_name[5:])
                else:
                    device_name = ", ".join(sub_name.split("-"))

                bases["items"][name].append({"name": device_name, "pvs": {}})
                last_sub_name = sub_name
                index += 1

            if "Current-Mon" in device["PV"]:
                bases["items"][name][index]["pvs"]["Current"] = {
                    "name": re.sub(":CH[0-9]", ":CH?", device["PV"])
                }
            else:
                for pv_type, value in TYPES.items():
                    if pv_type in device["PV"]:
                        bases["items"][name][index]["pvs"][value] = {
                            "name": device["PV"]
                        }
                        break

with open("config.json", "w") as file:
    file.write(json.dumps(bases))
