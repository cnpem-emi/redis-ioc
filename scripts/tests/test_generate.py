from generate import generate_board
from template import redis_template_top, redis_template_bot
from copy import deepcopy

valid = [
    {
        "ENABLE": "True",
        "IP": "127.0.0.1",
        "Hostname": "BBB",
        "Rack": "-",
        "ADDR": "-",
        "Key": "sensor",
        "PV": "PV",
        "Precision": "3",
        "Unit": "C",
        "Type": "float",
        "Scanrate": "1",
        "Location": "loc",
        "LOLO": "",
        "LOW": "",
        "HIGH": "",
        "HIHI": "",
    }
]


def test_valid_float():
    assert generate_board(valid, "10.128.118.141") == (
        redis_template_top.safe_substitute(IP_ADDR="10.128.118.141")
        + '\ndbLoadRecords("database/float.db", "DESCRIPTION=loc, REDIS_KEY=sensor, PREC=3, PORT=redisPort, RECORD_NAME=PV, SCANRATE=1, EGU=C, HIHI_VAL=, HI_VAL=, LOLO_VAL=, LO_VAL=")'
        + redis_template_bot
    )


def test_valid_float_scanrate():
    valid_scanrate = deepcopy(valid)
    valid_scanrate[0]["Scanrate"] = ".1"
    assert generate_board(valid_scanrate, "10.128.118.141") == (
        redis_template_top.safe_substitute(IP_ADDR="10.128.118.141")
        + '\ndbLoadRecords("database/float.db", "DESCRIPTION=loc, REDIS_KEY=sensor, PREC=3, PORT=redisPort, RECORD_NAME=PV, SCANRATE=.1, EGU=C, HIHI_VAL=, HI_VAL=, LOLO_VAL=, LO_VAL=")'
        + redis_template_bot
    )


def test_valid_float_scanrate_replace():
    valid_scanrate = deepcopy(valid)
    valid_scanrate[0]["Scanrate"] = "0.1"
    assert generate_board(valid_scanrate, "10.128.118.141") == (
        redis_template_top.safe_substitute(IP_ADDR="10.128.118.141")
        + '\ndbLoadRecords("database/float.db", "DESCRIPTION=loc, REDIS_KEY=sensor, PREC=3, PORT=redisPort, RECORD_NAME=PV, SCANRATE=.1, EGU=C, HIHI_VAL=, HI_VAL=, LOLO_VAL=, LO_VAL=")'
        + redis_template_bot
    )


def test_valid_hash():
    valid_hash = deepcopy(valid)
    valid_hash[0]["Type"] = "hash"
    valid_hash[0]["Key"] = "key|hash"
    assert generate_board(valid_hash, "10.128.118.141") == (
        redis_template_top.safe_substitute(IP_ADDR="10.128.118.141")
        + '\ndbLoadRecords("database/hash.db", "DESCRIPTION=loc, REDIS_KEY=key, PREC=3, PORT=redisPort, RECORD_NAME=PV, SCANRATE=1, EGU=C, HIHI_VAL=, HI_VAL=, LOLO_VAL=, LO_VAL=, REDIS_HASH=hash")'
        + redis_template_bot
    )


def test_valid_pub():
    valid_hash = deepcopy(valid)
    valid_hash[0]["Type"] = "array_put"
    valid_hash[0]["Pub"] = "pub"
    assert generate_board(valid_hash, "10.128.118.141") == (
        redis_template_top.safe_substitute(IP_ADDR="10.128.118.141")
        + '\ndbLoadRecords("database/array_put.db", "DESCRIPTION=loc, REDIS_KEY=sensor, PREC=3, PORT=redisPort, RECORD_NAME=PV, SCANRATE=1, EGU=C, HIHI_VAL=, HI_VAL=, LOLO_VAL=, LO_VAL=, PUB_KEY=pub")'
        + redis_template_bot
    )
