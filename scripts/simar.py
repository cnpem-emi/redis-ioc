import argparse
import re
from db import Db
import json
import pylightxl as xl
import os

"""
for i, s in enumerate(sheet.rows):
    if "SIMAR" in s[5]:
        sheet.update_index(row=i+1, col=6, val=re.sub(r"IA[0-9][0-9]-", s[10], s[5]))

pylightxl.writexl(db=db, fn='spreadsheet/Redes e Beaglebones.xlsx')
"""

TYPES = {
    "Temp": "Temperature",
    "Pressure": "Pressure",
    "RackOpen": "Rack Open",
    "Humidity": "Humidity",
    "Voltage": "Voltage",
    "PwrFactor": "PFactor",
    "PwrFrequency": "Frequency",
    "Glitch": "Glitches",
    "WaterLeak": "Leak",
    "Current": "Current",
}

SENSOR_HEADERS = ["Tipo Sensor", "Localização", "Canal", "Endereço", "Base Associada"]
BASE_HEADERS = ["Hostname", "IP", "Localização"]


def generate_report(bases: dict):
    base_row = 2
    sensor_row = 2

    del bases["items"][""]

    report_db.add_ws(ws="Sensores")
    report_db.add_ws(ws="Base")

    for i, header in enumerate(SENSOR_HEADERS):
        report_db.ws("Sensores").update_index(row=1, col=i + 1, val=header)

    for i, header in enumerate(BASE_HEADERS):
        report_db.ws("Base").update_index(row=1, col=i + 1, val=header)

    for base, sensors in bases["items"].items():
        try:
            hostname, ip = base.split(" - ")
        except ValueError:
            hostname = base.split(" - ")[0]
            ip = ""

        report_db.ws("Base").update_index(row=base_row, col=1, val=hostname)
        report_db.ws("Base").update_index(row=base_row, col=2, val=ip)
        report_db.ws("Base").update_index(
            row=base_row, col=3, val=sensors[0]["name"].split(",")[0]
        )
        base_row += 1

        for sensor in sensors:
            report_db.ws("Sensores").update_index(
                row=sensor_row,
                col=1,
                val="BME280" if "Humidity" in sensor["pvs"] else "BMP280",
            )
            report_db.ws("Sensores").update_index(
                row=sensor_row, col=2, val=sensor["name"]
            )
            report_db.ws("Sensores").update_index(
                row=sensor_row, col=3, val=sensor["channel"]
            )
            report_db.ws("Sensores").update_index(
                row=sensor_row, col=4, val=sensor["address"]
            )
            report_db.ws("Sensores").update_index(row=sensor_row, col=5, val=base)
            sensor_row += 1

    xl.writexl(db=report_db, fn="report.xlsx")


if __name__ == "__main__":  # noqa: C901
    parser = argparse.ArgumentParser(
        description="Automatically create SIMAR's web interface configuration file"
    )
    parser.add_argument(
        "--report", action="store_true", help="enable report generation"
    )

    args = parser.parse_args()

    db = Db("./spreadsheet/Redes e Beaglebones.xlsx", "PVs Redis")
    report_db = xl.Database()
    bases = {"items": {}}
    used_names = []

    last_sub_name = ""
    for ip, board in db.data.items():
        base = {}
        index = -1
        if any(
            ["SIMAR" in device["PV"] and device["ENABLE"] == "True" for device in board]
        ):
            name = board[0]["Hostname"]
            if ip not in ["10.0.38.59", "10.0.38.46", "10.0.38.42"]:
                name = "{} - {}".format(ip, board[0]["Hostname"])
                bases["items"][name] = []
            else:
                for dev in board:
                    bases["items"][dev["Hostname"]] = []
        else:
            continue
        for device in board:
            if (
                "SIMAR" in device["PV"]
                and device["ENABLE"] == "True"
                and device["Hostname"]
            ):
                sub_name = device["PV"].split(":")[0]
                if "Mini" in device["Hostname"]:
                    name = device["Hostname"]
                    index = -1

                if sub_name != last_sub_name:
                    device_name = device["Location"]
                    if sub_name[0:2] in ["SI", "IA"]:
                        if not sub_name[5:]:
                            device_name += ", {}".format(device["Rack"])
                        else:
                            device_name += ", {}".format(sub_name[5:])
                    else:
                        location_data = sub_name.split("-")
                        device_name = ", ".join(location_data)

                    if device_name in used_names:
                        device_name += " (1)"

                    try:
                        dev_channel = int(device["Key"][7])
                        dev_addr = int(device["Key"][9:11])
                    except (ValueError, IndexError):
                        dev_channel, dev_addr = (
                            (0, 76) if "wgen" in device["Key"] else (9, 99)
                        )

                    sensor_dict = {"name": device_name, "pvs": {}}
                    used_names.append(device_name)

                    if args.report:
                        sensor_dict = sensor_dict | {
                            "channel": dev_channel,
                            "address": dev_addr,
                        }

                    bases["items"][
                        device["Hostname"] if "Mini" in device["Hostname"] else name
                    ].append(sensor_dict)

                    last_sub_name = sub_name
                    index += 1

                pv_name = (
                    re.sub(":CH[0-9]", ":CH?", device["PV"])
                    if "Current-Mon" in device["PV"]
                    else device["PV"]
                ).replace(" ", "")

                for pv_type, value in TYPES.items():
                    if pv_type in device["PV"].split(":")[-1]:
                        bases["items"][name][index]["pvs"][value] = {"name": pv_name}
                        break

    if args.report:
        generate_report(bases)

    dir_name = os.path.dirname(os.path.abspath(__file__))

    if not os.path.exists(os.path.join(dir_name, "../json/")):
        os.makedirs(os.path.join(dir_name, "../json/"))

    with open(os.path.join(dir_name, "../json/", "config.json"), "w") as file:
        file.write(json.dumps(bases))
