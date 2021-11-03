import os

from db import Db
from template import (
    redis_template_float,
    redis_template_bot,
    redis_template_top,
    redis_template_top_redundant,
    redis_template_port,
    redis_template_hash,
)


def generate_board(board, ip) -> str:
    count = 0
    res, port_dec = "", ""
    ports = []

    if len(ip.split(",")) > 1:
        for i, ip in enumerate(ip.split(",")):
            port_dec += redis_template_port.safe_substitute(PORT_NO=i, PORT_IP=ip)
            ports.append('"L{}"'.format(i))

        res += redis_template_top_redundant.safe_substitute(
            PORT_DECLARATIONS=port_dec, PORTS=",".join(ports)
        )
    else:
        res += redis_template_top.safe_substitute(IP_ADDR=ip)

    for device in board:
        if device["Type"] == "hash_put" or device["Type"] == "hash":
            res += redis_template_hash.safe_substitute(
                DESCRIPTION=device["Location"],
                RECORD_NAME=device["PV"],
                SCANRATE=device["Scanrate"].replace("0.", "."),
                PREC=device["Precision"],
                EGU=device["Unit"],
                REDIS_KEY=device["Key"].split(":")[0],
                REDIS_HASH=device["Key"].split(":")[1],
                TYPE=device["Type"],
                HIGH=device["HIGH"],
                HIHI=device["HIHI"],
                LOW=device["LOW"],
                LOLO=device["LOLO"],
            )
        else:
            res += redis_template_float.safe_substitute(
                DESCRIPTION=device["Location"],
                RECORD_NAME=device["PV"],
                SCANRATE=device["Scanrate"].replace("0.", "."),
                PREC=device["Precision"],
                EGU=device["Unit"],
                REDIS_KEY=device["Key"],
                TYPE=device["Type"],
                HIGH=device["HIGH"],
                HIHI=device["HIHI"],
                LOW=device["LOW"],
                LOLO=device["LOLO"],
            )

        count += 1

    res += redis_template_bot
    return res


def generate(boards):
    dir_name = os.path.dirname(os.path.abspath(__file__))

    cmd_key = "Redis-"

    for board in boards:
        res = generate_board(boards[board], board)

        if not os.path.exists(os.path.join(dir_name, "../cmd/")):
            os.makedirs(os.path.join(dir_name, "../cmd/"))

        if len(board.split(",")) > 1:
            board = board.split(",")[0]
        cmd_path = os.path.join(dir_name, "../cmd/" + cmd_key + board + ".cmd")
        with open(cmd_path, "w+") as file:
            file.write(res)

        os.chmod(cmd_path, 0o774)


if __name__ == "__main__":
    db = Db("./spreadsheet/Redes e Beaglebones.xlsx", "PVs Redis")
    generate(db.data)
