# Fetch data from ThingsBoard

This is a simple script to fetch the data for a DEVICE from ThingsBoard and
merge all of the columns into one, easier to use CSV.

The code appears to work, but is a quick hack. PRs are very welcome.

You either need to install the dependencies using you system's package manager or,
if you have `pipenv`, then run `pipenv install` first.

## How to use

```bash
python3 fetch.py --help
```
Note: I test use `pipenv`, so I typically test with something like `pipenv run
fetch ...` rather then `python3 fetch.py`. It should fine with plain python3 as
long as you have all the required packages installed.

## Typical usage

### Fetch everything for a device

```bash
python3 fetch.py http://<your-tb-host> -u tenant@thingsboard.org -p admin -d 7ade2600-81a8-11eb-99a7-5d4c029b39e1
```

Where `7ade2600-81a8-11eb-99a7-5d4c029b39e1` is the ThingsBoard device ID.

### Fetch everything for multiple devices

```bash
python3 fetch.py http://<your-tb-host> -u tenant@thingsboard.org -p admin -d 7ade2600-81a8-11eb-99a7-5d4c029b39e1 -d 2f93c420-81bc-11eb-bbac-ff6c20e0c920 -d 50739480-be5d-11eb-b635-0b6b16c15ea2
```

Note you can have many `-d`/`--device` flags.

### Fetch only certain device keys (columns)

```bash
python3 fetch.py http://<your-tb-host> -u tenant@thingsboard.org -p admin -d 7ade2600-81a8-11eb-99a7-5d4c029b39e1 -k lw_dr -k lw_rssi -k soil_moisture_gwc
```

### Fetch for a date range
```bash
python3 fetch.py http://<your-tb-host> -u tenant@thingsboard.org -p admin -d 7ade2600-81a8-11eb-99a7-5d4c029b39e1 --start 1626721170000 --stop 1626723170000
```

Note `--start`/`--stop` are millisecond UNIX timestamps.

