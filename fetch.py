import sys
import os
import argparse
import requests
import pandas as pd

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

def get_data(url, token, device, key, start, stop):
    p = pd.DataFrame()

    # You have to request data backwards in time ...
    while start < stop:
        data = get_data_chunk(url, token, device, key, start, stop, 10000)

        if key not in data:
            break;

        #print(f"{key}: Loaded {len(data[key])} points")

        t = pd.DataFrame.from_records(data[key])
        t.set_index('ts', inplace=True)
        t.rename(columns={'value': key}, inplace=True)
        p = p.append(t)

        # Update "new" stop time
        stop = data[key][-1]['ts'] - 1

    return p


parser = argparse.ArgumentParser(description="Fetch DEVICE data from ThingsBoard")
parser.add_argument('url', type=str, help='Base URL to ThingsBoard API')
parser.add_argument('--username', '-u', type=str, required=True, help='ThingsBoard username')
parser.add_argument('--password', '-p', type=str, required=True, help='ThingsBoard password')
parser.add_argument('--device', '-d', type=str, required=True, action='append', help='ThingsBoard device id to fetch data of')
parser.add_argument('--key', '-k', type=str, action='append', help='ThingsBoard device key to fetch')
parser.add_argument('--start', type=int, default=0, help='Start time as milisecond UNIX timestamp')
parser.add_argument('--stop', type=int, default=sys.maxsize, help='Stop time as milisecond UNIX timestamp')

args = parser.parse_args()

token = login(args.url, args.username, args.password);

# fetch data
for device in args.device:
    keys = args.key if args.key else get_keys(args.url, token, device)

    print(f"Downloading DEVICE: {device} data");

    p = pd.DataFrame()
    for key in keys:
        print(f"info: Pulling {key}...");
        p = pd.concat([p, get_data(args.url, token, device, key, args.start, args.stop)], axis=1)

    p.to_csv(f"./data-{device}.csv")
