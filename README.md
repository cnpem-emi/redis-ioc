# Redis IOC

A StreamDevice based EPICS IOC that interfaces with Redis databases.

## Utilization
Change the IOC table sync URL in the Makefile or swap out the table in `scripts/spreadsheet`.

Each row represents a different PV, and you can configure it through columns.

Then, run `generate.py`. A `cmd` folder will be generated.

### Necessary Parameters:
- Enabled: `True` enables the PV, `False` disables it.
- IP: Redis server IP (must use port 6379). This IOC also supports redundancy, which must be enabled by setting multiple IPs, separated by commas (,).
- Key: Redis key
- PV: PV name
- Precision: Digits of decimal precision (only applies to float-related fields)
- Unit: EGU
- Scanrate: Scanrate. Follows default StreamDevice values.
- Type: Data type (float, float_put, int, int_put, string, string_put, array, array_put, hash, hash_put)
    - Variables with the `put` suffix allow for `caput` commands
    - Since Redis returns a string for most, this only affects how Redis' response is processed

### Optional Parameters: 
- Rack: Doesn't affect the IOC
- ADDR: Doesn't affect the IOC
- Location: Passed over to `DESC` field
- HIHI/HIGH/LOW/LOLO: Alarm values
- Pub: Only used for array/list types, determines the subscription name for one or more PVs (a PUBLISH event is fired on each caput)

## Supported data types

| Data Type | Get | Put |
|-----------|-----|-----|
| Float | ✓ | ✓ |
| Int | ✓ | ✓ |
| String | ✓ | ✓ |
| Array/List | ✓ | ✓ |
| Hash | ✓ | ✓ |
| Bitmaps | * | * |
| Sorted Sets | | |
| Streams | | |

## Logs

Located in `/opt/redis-ioc/log`
