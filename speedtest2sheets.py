import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import subprocess
import pandas as pd
import csv
from pathlib import Path
from discord_webhook import DiscordWebhook

logf = open("st2s.log", "w")

try:
    #####################################
    ######         SETTINGS         #####
    #####################################

    JSON_CLIENT_SECRET = "client_secret.json"
    SHEET_NAME = "SpeedTests"
    CSV_FILE = "speedtest.csv"
    SERVER_ID = "40788" # Zen London
    MIN_DOWNLOAD_MB = 450 # Set to 0 to disable
    MIN_UPLOAD_MB = 450 # Set to 0 to disable
    ENABLE_DISCORD_ALERTS = False
    DISCORD_WEBHOOK = ""

    #####################################
    #####           SCRIPT          #####
    #####################################

    # Get current Date and Time
    now = datetime.now()
    current_dt = now.strftime("%m/%d/%Y %H:%M:%S")

    # Checking if script has been ran before (This will include headers in the CSV if it has)
    path_to_file = './hasran'
    path = Path(path_to_file)
    first_run = not path.is_file()
    path.touch()

    # Run the speed test
    print("Running speedtest...")
    subprocess.call("/usr/bin/speedtest --server-id={} --output-header --format=csv > {}".format(SERVER_ID, CSV_FILE), shell=True)

    # Add Date/Time
    print("Appending Date/Time to CSV")
    df = pd.read_csv(CSV_FILE)
    date_string = now.strftime("%m/%d/%Y, %H:%M:%S")
    df["date"] = date_string
    downloadbytes = df["download bytes"]
    uploadbytes = df["upload bytes"]
    downloadMb = downloadbytes / 1000000
    uploadMb = uploadbytes / 1000000
    df["Download Mb"] = downloadMb
    df["Upload Mb"] = uploadMb
    df.to_csv(CSV_FILE, index=False, header=first_run)

    # Check speeds
    speed_check_message = ""
    print("Checking speeds...")
    if (float(downloadMb) < float(MIN_DOWNLOAD_MB)):
        speed_check_message = "Download speed is lower than minimum value ({}): {:.2f}".format(MIN_DOWNLOAD_MB, float(downloadMb))
    if (float(uploadMb) < float(MIN_UPLOAD_MB)):
        speed_check_message = speed_check_message + "\nUpload speed is lower than minimum value ({}): {:.2f}".format(MIN_UPLOAD_MB, float(uploadMb))

    if speed_check_message:
        print(speed_check_message)
        # Discord Alerting
        if ENABLE_DISCORD_ALERTS:
            webhook = DiscordWebhook(url=DISCORD_WEBHOOK, content=speed_check_message)
            response = webhook.execute()

    # Sheets stuff
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_CLIENT_SECRET, scope)
    client = gspread.authorize(credentials)

    spreadsheet = client.open(SHEET_NAME)

    # Append the sheet
    print("Uploading to sheets...")
    spreadsheet = client.open(SHEET_NAME)
    worksheet = spreadsheet.worksheet(SHEET_NAME)
    content = list(csv.reader(open(CSV_FILE)))
    worksheet.append_rows(content, value_input_option="USER_ENTERED")

    print("Done")
except Exception as e:     # most generic exception you can catch
    logf.write("Error: {0}\n".format(str(e)))
