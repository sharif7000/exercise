start_date = input("Please enter date in (YYYY-MM-DD) format: ") or '2022-01-01'
end_date = input("Please enter date in (YYYY-MM-DD) format: ") or '2022-12-31'
cpeName = input("Please enter CPE name : ") or "cpe:2.3:o:redhat:enterprise_linux:8.0"
BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"