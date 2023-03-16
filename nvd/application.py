import dateutil.parser
import requests
import pandas as pd
import datetime
import variables

date = variables.date
cpeName = variables.cpeName
#date = '2022-01-01'
tmpStartDate = dateutil.parser.isoparse(date)
print(tmpStartDate)
tmpEndDate = tmpStartDate + datetime.timedelta(days=120)
#cpeName = "cpe:2.3:o:redhat:enterprise_linux:8.0"

print("Start of process")
data_set = []
while tmpStartDate < datetime.datetime.now():
    #print("Fetching data from " , tmpStartDate ," To " , tmpEndDate)
    fomrattedStartDate = tmpStartDate.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
    fomrattedEndDate = tmpEndDate.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
    ## CALL API
    base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    query_params = {"cpeName": cpeName, "pubStartDate": fomrattedStartDate, "pubEndDate": fomrattedEndDate}
    response = requests.get(base_url, params=query_params).json()

    results = response['vulnerabilities']

   
    for result in results:
            cve_id = result['cve']['id']
            cisa_vuln_name = ''
            try:
                cisa_vuln_name = result['cve']['cisaVulnerabilityName']
            except KeyError:
                print()
            is_exploited = False
            for reference in result['cve']['references']:
                if 'tags' in reference and 'Exploit' in reference['tags']:
                    is_exploited = True
                    break
            cvss_base_score = None
            cvss_metric_v31 = result['cve']['metrics'].get('cvssMetricV31', [])
            #print(cvss_metric_v31)
            if cvss_metric_v31:
                cvss_base_score = cvss_metric_v31[0]['cvssData']['baseScore']
            else:
                cvss_metric_v2 = result['cve']['metrics'].get('cvssMetricV2', [])
                if cvss_metric_v2:
                    cvss_base_score = cvss_metric_v2[0]['cvssData']['baseScore']
            vuln_description = result['cve']['descriptions'][0]['value'][:400]

            
            tmpData = {"CVE ID": cve_id, "CISA Vulnerability Name": cisa_vuln_name, "Exploited": is_exploited, "CVSS Base Score": cvss_base_score, "Vulnerability Description": vuln_description}

            #print(tmpData)
            data_set.append(tmpData)

    
            #Print extracted information
            # print(f"CVE ID: {cve_id}")
            # print(f"CISA Vulnerability Name: {cisa_vuln_name}")
            # print(f"Exploited: {is_exploited}")
            # print(f"CVSS Base Score: {cvss_base_score}")
            # print(f"Vulnerability Description: {vuln_description}")
    
    



    #print(data_set)        
    tmpStartDate = tmpEndDate
    tmpEndDate = tmpStartDate + datetime.timedelta(days=120)


#print(data_set)
# Add to CSV file
df = pd.json_normalize(data_set)
df.to_csv("CVE_data_new.csv", index=False)
print("End of process")
