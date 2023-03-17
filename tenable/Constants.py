access_key = "c74d99b49b38a853cb1ff4cea5ef83f8eeadf0ddc37849711b730d276c79ba54"
secret_key = "46cbceaa6599b79ee87ffc26ffd59609056db49af35cfe6b62508f6642f4f8e1"

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