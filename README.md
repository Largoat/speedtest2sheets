# speedtest2sheets
Run a speedtest and log the results to a Google Sheet. There is also Discord Alerting available if the speed is below a minimum which is set by the user

# Installation
## Script Requirements
```
pip install -r requirements.txt
```

## Speedtest CLI
You'll need to download and install the [Speedtest CLI](https://www.speedtest.net/apps/cli)

## Generate client_secret.json
To generate the `client_secret.json` file you can follow [This Guide](https://medium.com/craftsmenltd/from-csv-to-google-sheet-using-python-ef097cb014f9). Copy the json file generated in to the same directory as the script

# Settings
`JSON_CLIENT_SECRET`: Default: `client_secret.json` - Location of the `client_secret.json` file to allow access to Sheets

`SHEET_NAME`: Default: `SpeedTests` - Name of the Google Sheet to upload results to

`CSV_FILE`: Default: `speedtest.csv` - CSV File generated by the Speedtest CLI

`SERVER_ID`: Default: `40788` (Zen London) - Server ID of the sever to run the speed test against. [Instructions on how to find Server ID](https://www.dcmembers.com/skwire/how-to-find-a-speedtest-net-server-id/)

`MIN_DOWNLOAD_MB`: Default: `450` - Minimum speed in Mb. Below this value will trigger an alert. Set to `0` to disable

`MIN_UPLOAD_MB`: Default: `450` - Minimum speed in Mb. Below this value will trigger an alert. Set to `0` to disable

`ENABLE_DISCORD_ALERTS`: Default: `False` - Enable or Disable Discord Alerts to alert when speeds are below set value. Requires a valid Webhook

`DISCORD_WEBHOOK`: Default: `""` - Disrcord Webhook
