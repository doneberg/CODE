import requests
import datetime
from datetime import date

headers = {'Accept':'application/json'}
protocol = "https"
wsEntryPoint = "data-api.ecb.europa.eu"
serv = "service"
resource = "data"
flowRef = "YC"
key = "B.U2.EUR.4F.G_N_A.SV_C_YM.SR_10Y"
oneDay = datetime.timedelta(days=1) #delta for finding yesterday
yesterday = str(date.today()-oneDay)
today = str(date.today())

parameters = {
   "startPeriod" : yesterday,
   "endPeriod" : today,
    "detail": "full",
    "format": "jsondata",
    "includeHistory": "false",
    "freq": "B",
    "dataflow": "YC",
    "lastNObservations": "1"
}

url = f"{protocol}://{wsEntryPoint}/{serv}/{resource}/{flowRef}/{key}"
4
response = requests.get(url, params=parameters, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(f"Yield Curve Spot Rate for {today}")
    print("\t".join(data[0].keys()))
    
    for item in data:
     print("\t".join(str(value) for value in item.values()))
else:
    print(f"Failed to retrieve data: {response.status_code}, {response.reason}")
