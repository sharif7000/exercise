import requests
import pandas as pd 
import time
import urllib3
import json

access_key = "c74d99b49b38a853cb1ff4cea5ef83f8eeadf0ddc37849711b730d276c79ba54"
secret_key = "46cbceaa6599b79ee87ffc26ffd59609056db49af35cfe6b62508f6642f4f8e1"
SCAN_ID = "15"

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#url = f"https://localhost:8834/scans/{scan_id}/export"
url = f"https://localhost:8834/"
headers = {
    "x-apikeys": f"accessKey={access_key};secretKey={secret_key}",
    "content-type": "application/json"
}
headersDownload = {
    "x-apikeys": f"accessKey={access_key};secretKey={secret_key}"
}
# get folder_id
folderurl = url+"folders"
folderresponse = requests.get(folderurl,headers=headers,verify=False).json()
for folder in folderresponse["folders"]:
    if folder['name'] == 'My Scans':
        folder_id = folder['id']

# get _scan_id
scan_url= url+"scans/"
scan_query_param = {"folder_id" : folder_id}
scan_response = requests.get(scan_url, scan_query_param, headers=headers, verify=False).json()
print(scan_response)
for scan in scan_response["scans"]:
    if scan["name"] == 'auth test':
        SCAN_ID = scan["id"]
        print(SCAN_ID)

response_url= f"{scan_url}{SCAN_ID}/export"
print(response_url)

# Define the request body as a dictionary
body = {
    "format": "csv",
    "template_id": "",
    "reportContents": {
        "csvColumns": {
            "id": "true",
            "cve": "true",
            "cvss": "true"
        }
    }
}

# Convert the dictionary to a JSON string
json_data = json.dumps(body)
response = requests.post(response_url, headers=headers, data=json_data, verify=False).json()
EXPORT_ID = response["file"]
print(EXPORT_ID)

donwload_url = "https://localhost:8834//scans/15/export/591316015/download"

SCAN_ID = "15"
EXPORT_STATUS_URL = f"https://localhost:8834/scans/{SCAN_ID}/export/{EXPORT_ID}/status"
EXPORT_DOWNLOAD_URL = f"https://localhost:8834/scans/{SCAN_ID}/export/{EXPORT_ID}/download"
CSV_FILENAME = "export.csv"

time.sleep(10)

# Make initial request to check export status
export_status = ""
while export_status != "ready":
    response = requests.get(EXPORT_STATUS_URL,verify=False, headers=headers)
    response_json = response.json()
    export_status = response_json["status"]
    print(f"Export status: {export_status}")
    if export_status != "ready":
        time.sleep(10)


print(EXPORT_DOWNLOAD_URL)
# Once the export is ready, download the CSV file
response = requests.get(EXPORT_DOWNLOAD_URL,verify=False, headers=headersDownload)
with open(CSV_FILENAME, "wb") as f:
    f.write(response.content)
    print(f"File saved as {CSV_FILENAME}")

