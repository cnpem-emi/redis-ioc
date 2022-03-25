# Redis IOC

A StreamDevice based EPICS IOC that interfaces with Redis databases.

## Utilization
Change the IOC table sync URL in the Makefile or swap out the table in `scripts/spreadsheet`.

Each row represents a different PV, and you can configure it through columns.

### Necessary Parameters:
- Enabled: `True` enables the PV, `False` disables it.
- IP: Redis server IP (must use port 6379). This IOC also supports redundancy, which must be enabled by setting multiple IPs, separated by commas (,).
- Key: Redis key
- PV: PV name
- Precision: Digits of decimal precision (only applies to float-related fields)
- Unit: EGU
- Scanrate: Scanrate. Follows default StreamDevice values.
- Type: Tipo de variável (float, float_put, int, int_put, string, string_put, array, array_put, hash, hash_put)
    - Variables with the `put` suffix allow for `caput` commands

### Optional Parameters: 
- Rack: Doesn't affect the IOC
- ADDR: Doesn't affect the IOC
- Location: Passed over to `DESC` field
- HIHI/HIGH/LOW/LOLO: Alarm values

## Logs

Located in `/opt/redis-ioc/log`
