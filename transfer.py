import sys
import argparse
import requests
import json

def login(url, username, password):
    # Log into ThingsBoard
    return requests.post(f"{url}/api/auth/login", json={
        "username": username,
        "password": password
    }).json()['token']

def get_keys(url, token, device):
    return requests.get(f"{url}/api/plugins/telemetry/DEVICE/{device}/keys/timeseries",
                 headers={
                     'content-type': 'application/json',
                     'x-authorization': f"bearer {token}"
                 }).json()

def get_data_chunk(url, token, device, key, start, stop, limit):
    return requests.get(f"{url}/api/plugins/telemetry/DEVICE/{device}/values/timeseries",
             headers={
                 'content-type': 'application/json',
                 'x-authorization': f"bearer {token}"
             },
            params= {
                'keys': key,
                'startTs': start,
                'endTs': stop,
                'limit': limit,
                'agg': 'NONE'
            }).json()

def post_data_chunk(url, device_token, data):
   return requests.post(f"{url}/api/v1/{device_token}/telemetry", data = json.dumps(data))

parser = argparse.ArgumentParser(description="Fetch DEVICE data from ThingsBoard")
parser.add_argument('--url', type=str, help='Base URL of source ThingsBoard API')
parser.add_argument('--post_url', type=str, help='Base URL of sink ThingsBoard API')
parser.add_argument('--device_token', type=str, help='Target device token in sink ThingsBoard')
parser.add_argument('--username', '-u', type=str, required=True, help='ThingsBoard username')
parser.add_argument('--password', '-p', type=str, required=True, help='ThingsBoard password')
parser.add_argument('--device', '-d', type=str, required=True, action='append', help='ThingsBoard device id to fetch data of')
parser.add_argument('--key', '-k', type=str, required=True, help='ThingsBoard device key to fetch')
parser.add_argument('--type', '-t', type=str, required=False, help='Type of dataitem (float, int)')
parser.add_argument('--start', type=int, default=0, help='Start time as milisecond UNIX timestamp')
parser.add_argument('--stop', type=int, default=sys.maxsize, help='Stop time as milisecond UNIX timestamp')
parser.add_argument('--new_start', type=int, default=None, help='Time to make the new series artificially start as milisecond UNIX timestamp')

args = parser.parse_args()

token = login(args.url, args.username, args.password);

# fetch data
for device in args.device:
    key = args.key
    start = args.start
    stop = args.stop
    new_start = args.new_start if args.new_start != None else args.start

    type = lambda x: x
    if args.type == "int":
        type = int
    elif args.type == "float":
        type = float
    elif args.type == "bool":
        type = lambda x: True if x.lower() == 'true' else False

    print(f"Downloading DEVICE: {device}, KEY: {key}");

    ts_diff = new_start - start

    # You have to request data backwards in time ...
    while start < stop:
        data = get_data_chunk(args.url, token, device, key, start, stop, 50000)

        if key not in data:
            break;

        # Update "new" stop time
        stop = data[key][-1]['ts'] - 1

        print(f"{key}: Loaded {len(data[key])} points")
        data = list(map(lambda x: { 'ts': x['ts'] + ts_diff, 'values': { key: type(x['value']) } }, data[key]))

        print(post_data_chunk(args.post_url, args.device_token, data))
