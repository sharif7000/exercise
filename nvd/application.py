import dateutil.parser
import requests
import pandas as pd
import datetime
import variables
import os

# Get start date

tmpStartDate = dateutil.parser.isoparse(variables.start_date)
end_date = dateutil.parser.isoparse(variables.end_date)
if tmpStartDate > end_date:
    print("Please provide end date later than start date")
    exit()
# Initialize end date to +120 days from start date
tmpEndDate = tmpStartDate + datetime.timedelta(days=120)

# If given end date is less than 120 days, correct the end date by assigning the provided
if tmpEndDate > end_date:
    tmpEndDate = end_date
    print(f"Data will be generated for {tmpStartDate} to {end_date}")
else:
    print(f"Data will be generated for {tmpStartDate} to {end_date}")

print("Fetching data in bacthes of 120 days")
data_set = []
while tmpStartDate < dateutil.parser.isoparse(variables.end_date):

    fomrattedStartDate = tmpStartDate.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
    fomrattedEndDate = tmpEndDate.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
    print("Fetching data from ", fomrattedStartDate, " To ", fomrattedEndDate)
    query_params = {"cpeName": variables.cpeName,
                    "pubStartDate": fomrattedStartDate, "pubEndDate": fomrattedEndDate}
    response = requests.get(variables.BASE_URL, params=query_params).json()

    results = response['vulnerabilities']
    print("Received data with size ", len(results))
    for result in results:
        cve_id = result['cve']['id']
        cisa_vuln_name = ''
        try:
            cisa_vuln_name = result['cve']['cisaVulnerabilityName']
        except KeyError:
            pass
        is_exploited = False
        for reference in result['cve']['references']:
            if 'tags' in reference and 'Exploit' in reference['tags']:
                is_exploited = True
                break
        cvss_base_score = None
        cvss_metric_v31 = result['cve']['metrics'].get('cvssMetricV31', [])
        if cvss_metric_v31:
            cvss_base_score = cvss_metric_v31[0]['cvssData']['baseScore']
        else:
            cvss_metric_v2 = result['cve']['metrics'].get('cvssMetricV2', [])
            if cvss_metric_v2:
                cvss_base_score = cvss_metric_v2[0]['cvssData']['baseScore']
        vuln_description = result['cve']['descriptions'][0]['value'][:400]

        tmpData = {"CVE ID": cve_id, "CISA Vulnerability Name": cisa_vuln_name, "Exploited": is_exploited,
                   "CVSS Base Score": cvss_base_score, "Vulnerability Description": vuln_description}
        data_set.append(tmpData)

    tmpStartDate = tmpEndDate
    tmpEndDate = tmpStartDate + datetime.timedelta(days=120)
    if tmpEndDate > dateutil.parser.isoparse(variables.end_date):
        tmpEndDate = dateutil.parser.isoparse(variables.end_date)


# Add to CSV file
file_path = os.getcwd()
file_name= "CVE_data"
df = pd.json_normalize(data_set)
df.to_csv(f"{file_name}.csv", index=False)

print(f"{file_name} saved at : {file_path}")