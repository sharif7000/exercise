import requests
import time
import urllib3
import json
import Constants
import os
import datetime

# Initilize global variables
SCAN_ID = ""

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# get folder_id
folderurl = f"{Constants.BASE_URL}/folders"
folderresponse = requests.get(
    folderurl, headers=Constants.headers, verify=False).json()
for folder in folderresponse["folders"]:
    if folder['name'] == 'My Scans':
        folder_id = folder['id']

# get _scan_id
scan_url = Constants.BASE_URL + "/scans"
scan_query_param = {"folder_id": folder_id}
print("Calling URL ", scan_url)
scan_response = requests.get(
    scan_url, scan_query_param, headers=Constants.headers, verify=False).json()

for scan in scan_response["scans"]:
    if scan["name"] == 'auth test':
        SCAN_ID = scan["id"]

GENERATE_EXPORT_URL = f"{scan_url}/{SCAN_ID}/export"
print("Calling URL ", GENERATE_EXPORT_URL)

json_data = json.dumps(Constants.body)
response = requests.post(GENERATE_EXPORT_URL, headers=Constants.headers,
                         data=json_data, verify=False).json()
EXPORT_ID = response["file"]

EXPORT_STATUS_URL = f"{Constants.BASE_URL}/scans/{SCAN_ID}/export/{EXPORT_ID}/status"
EXPORT_DOWNLOAD_URL = f"{Constants.BASE_URL}/scans/{SCAN_ID}/export/{EXPORT_ID}/download"


print("Sleeping for 5 seconds to let the app generate export file")
time.sleep(5)

# Make initial request to check export status
export_status = ""
print("Checking if status is ready")
while export_status != "ready":
    response = requests.get(
        EXPORT_STATUS_URL, verify=False, headers=Constants.headers)
    response_json = response.json()
    export_status = response_json["status"]
    print(f"Export status: {export_status}")
    if export_status != "ready":
        time.sleep(5)


print("Calling URL ", EXPORT_DOWNLOAD_URL)
# Once the export is ready, download the CSV file
file_response = requests.get(EXPORT_DOWNLOAD_URL, verify=False,
                             headers=Constants.headersAuth)

timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
file_name_timestamp = f"{Constants.CSV_FILENAME}_{SCAN_ID}_{timestamp_str}.csv"
with open(file_name_timestamp, "wb") as f:
    f.write(file_response.content)
    abs_csv_path = os.path.abspath(f.name)
    print(f"File saved as {abs_csv_path}")

