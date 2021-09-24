from string import Template

redis_template_port = Template(
    """drvAsynIPPortConfigure("L${PORT_NO}", "${PORT_IP}:6379")
asynSetOption("L${PORT_NO}", -1, "disconnectOnReadTimeout", "Y")
"""
)

redis_template_top_redundant = Template(
    """#!/opt/epics-R3.15.8/modules/asyn-failover-0.1.1/bin/linux-x86_64/asynFailoverApp

epicsEnvSet("STREAMDEVICE", "/opt/epics-R3.15.8/modules/StreamDevice-2.8.18")
epicsEnvSet("IOC", "/opt/redis-ioc")
epicsEnvSet("STREAM_PROTOCOL_PATH", "$(IOC)/protocol")
epicsEnvSet("AVAILABLE", "0")

dbLoadDatabase "/opt/epics-R3.15.8/modules/asyn-failover-0.1.1/dbd/asynFailoverApp.dbd"
asynFailoverApp_registerRecordDeviceDriver pdbbase

${PORT_DECLARATIONS}

asynFailoverConfig("redisPort", ${PORTS}) 

cd ${IOC}
"""
)

redis_template_top = Template(
    """#!/opt/epics-R3.15.8/modules/StreamDevice-2.8.18/bin/linux-x86_64/streamApp

epicsEnvSet("STREAMDEVICE", "/opt/epics-R3.15.8/modules/StreamDevice-2.8.18")
epicsEnvSet("IOC", "/opt/redis-ioc")
epicsEnvSet("STREAM_PROTOCOL_PATH", "$(IOC)/protocol")

dbLoadDatabase("$(STREAMDEVICE)/dbd/streamApp.dbd")
streamApp_registerRecordDeviceDriver(pdbbase)
drvAsynIPPortConfigure("redisPort", "${IP_ADDR}:6379")

cd ${IOC}
"""
)

redis_template_float = Template(
    """
dbLoadRecords("database/${TYPE}.db", "DESCRIPTION=$DESCRIPTION, REDIS_KEY=$REDIS_KEY, PREC=$PREC, PORT=redisPort, RECORD_NAME=$RECORD_NAME, SCANRATE=$SCANRATE, EGU=$EGU, HIHI_VAL=$HIHI, HI_VAL=$HIGH, LOLO_VAL=$LOLO, LO_VAL=$LOW")"""
)

redis_template_hash = Template(
    """
dbLoadRecords("database/${TYPE}.db", "DESCRIPTION=$DESCRIPTION, REDIS_KEY=$REDIS_KEY, REDIS_HASH=$REDIS_HASH, PREC=$PREC, PORT=redisPort, RECORD_NAME=$RECORD_NAME, SCANRATE=$SCANRATE, EGU=$EGU, HIHI_VAL=$HIHI, HI_VAL=$HIGH, LOLO_VAL=$LOLO, LO_VAL=$LOW")"""
)

redis_template_bot = """

iocInit
"""
