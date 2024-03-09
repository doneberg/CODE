import requests
import pandas as pd

base_url = 'https://data-api.ecb.europa.eu/data/'
dataflow_id = 'YC.B.U2.EUR.4F.G_N_A'  # Replace with the correct dataflow ID
data_format = 'jsondata'

endpoint = f"{base_url}{dataflow_id}.{data_format}"

response = requests.get(endpoint)

if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data['dataSets'][0]['series']['0:0:0:0']['observations'])
    df.rename(columns=df.iloc[0], inplace=True)
    df.drop(df.index[0], inplace=True)
    df['time'] = pd.to_datetime(df['time']) 

    yield_curve_values = df['value']
    print(yield_curve_values)
else:
    print("Request failed. Status code:", response.status_code)