access_key = input("Please provide access_key : ")
secret_key = input("Please provide secret_key : ")

# Base URL
BASE_URL = f"https://localhost:8834"

# Body for creating export
json = {
    "format": "csv",
    "template_id": "",
    "reportContents": {
                    "vulnerabilitySections" :{
        
                                        "id": True,
                                        "cve": True,
                                        "cvss": True,
                                        "cvss3_base_score" : True,
                                        "cvss2_base_score" : True
                                    }
    }
}

#Header for authentication for JSON request 
headers = {
    "x-apikeys": f"accessKey={access_key};secretKey={secret_key}",
    "content-type": "application/json"
}
#Header for authentication
headersAuth = {
    "x-apikeys": f"accessKey={access_key};secretKey={secret_key}"
}

CSV_FILENAME = "export"