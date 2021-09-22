#!/usr/bin/env /bin/bash

set -e

#source_username= ... provide on command line ...
#source_password= ... provide on command line ...
source_url=http://oats2.ecn.purdue.edu:10000
#source_device_id= ... provide on command line ....  976ea430-be6f-11eb-b635-0b6b16c15ea2

sink_url=https://things-pro.ag.purdue.edu:8080
#sink_device_token= ... provide on command line .... aFmrTHVRtzFHgrbqBhZx

pipenv run transfer --username $source_username --password $source_password --url $source_url --device $source_device_id --post_url $sink_url --device_token $sink_device_token --key lw_dr --type int 
pipenv run transfer --username $source_username --password $source_password --url $source_url --device $source_device_id --post_url $sink_url --device_token $sink_device_token --key lw_data 
pipenv run transfer --username $source_username --password $source_password --url $source_url --device $source_device_id --post_url $sink_url --device_token $sink_device_token --key lw_battery_level --type float
pipenv run transfer --username $source_username --password $source_password --url $source_url --device $source_device_id --post_url $sink_url --device_token $sink_device_token --key lw_external_power --type bool
pipenv run transfer --username $source_username --password $source_password --url $source_url --device $source_device_id --post_url $sink_url --device_token $sink_device_token --key lw_fcnt --type int
pipenv run transfer --username $source_username --password $source_password --url $source_url --device $source_device_id --post_url $sink_url --device_token $sink_device_token --key lw_fport --type int
pipenv run transfer --username $source_username --password $source_password --url $source_url --device $source_device_id --post_url $sink_url --device_token $sink_device_token --key lw_rssi --type int
pipenv run transfer --username $source_username --password $source_password --url $source_url --device $source_device_id --post_url $sink_url --device_token $sink_device_token --key lw_snr --type float
pipenv run transfer --username $source_username --password $source_password --url $source_url --device $source_device_id --post_url $sink_url --device_token $sink_device_token --key lw_snr_margin --type int

pipenv run transfer --username $source_username --password $source_password --url $source_url --device $source_device_id --post_url $sink_url --device_token $sink_device_token --key ambient_temp_c --type float
pipenv run transfer --username $source_username --password $source_password --url $source_url --device $source_device_id --post_url $sink_url --device_token $sink_device_token --key light_intensity --type float
pipenv run transfer --username $source_username --password $source_password --url $source_url --device $source_device_id --post_url $sink_url --device_token $sink_device_token --key relative_humidity --type float
pipenv run transfer --username $source_username --password $source_password --url $source_url --device $source_device_id --post_url $sink_url --device_token $sink_device_token --key soil_temp1_c --type float
pipenv run transfer --username $source_username --password $source_password --url $source_url --device $source_device_id --post_url $sink_url --device_token $sink_device_token --key soil_temp2_c --type float
pipenv run transfer --username $source_username --password $source_password --url $source_url --device $source_device_id --post_url $sink_url --device_token $sink_device_token --key watermark1_pa --type float
pipenv run transfer --username $source_username --password $source_password --url $source_url --device $source_device_id --post_url $sink_url --device_token $sink_device_token --key watermark2_pa --type float
pipenv run transfer --username $source_username --password $source_password --url $source_url --device $source_device_id --post_url $sink_url --device_token $sink_device_token --key battery_voltage --type float


