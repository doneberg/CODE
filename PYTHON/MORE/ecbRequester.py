import sdmx
import pandas as pd

ecb = sdmx.Client("ECB")

def get_available_dataflows(client):
    dataflow_message = client.dataflow()
    dataflows_df = sdmx.to_pandas(dataflow_message.dataflow)
    dataflows_df.name = f"{client.source.id} Dataflows"
    return dataflows_df

dataflows = get_available_dataflows(ecb)
dataflows

"""
Outputs a Series with the dataflow's id as the index
and its name as the value:

AME                                                AMECO
BKN                                 Banknotes statistics
BLS                       Bank Lending Survey Statistics
BNT        Shipments of Euro Banknotes Statistics (ESCB)
BOP    Euro Area Balance of Payments and Internationa...
                             ...
SUR                                      Opinion Surveys
TGB                                      Target Balances
TRD                                       External Trade
WTS                                        Trade weights
YC                   Financial market data - yield curve
Name: ECB Available Dataflows, Length: 80, dtype: object
"""
def get_dataflow_metadata(client, dataflow_id):
    dataflow_message = ecb.dataflow(dataflow_id)
    return (
        dataflow_message.dataflow[dataflow_id].structure,
        dataflow_message.constraint[f"{dataflow_id}_CONSTRAINTS"].data_content_region[0],
        dataflow_message.dataflow[dataflow_id].name
    )

yc_data_structure_definition, yc_constraints, yc_name = get_dataflow_metadata(ecb, 'YC')
yc_data_structure_definition

"""
Output:

<DataStructureDefinition ECB:ECB_FMD2(1.0): Financial market data (not related to foreign exchange)>
"""

def get_dataflow_dimensions(data_structure_definition, dataflow_name):
    dimensions = data_structure_definition.dimensions
    return pd.Series({
        dimension.id: dimension.concept_identity.name
        for dimension in dimensions
    }, name=f"'{dataflow_name}' Dimensions")

yc_dimensions = get_dataflow_dimensions(yc_data_structure_definition, yc_name)
yc_dimensions

"""
Outputs a Series with the dimension's id as the index
and its name as the value:

FREQ                                         Frequency
REF_AREA                                Reference area
CURRENCY                                      Currency
PROVIDER_FM                  Financial market provider
INSTRUMENT_FM              Financial market instrument
PROVIDER_FM_ID    Financial market provider identifier
DATA_TYPE_FM                Financial market data type
TIME_PERIOD                       Time period or range
Name: 'Financial market data - yield curve' Dimensions,
dtype: object
"""
def get_code_description(code, dimension):
    codelist = dimension.local_representation.enumerated
    return codelist[code].name

def get_constraint_codes(constraints, dimension):
    try:
        codes = constraints.member[dimension.id].values
    except:
        return pd.Series(name=f"'{dimension.id}' Codes", dtype='object')

    codes_with_description = {
        code.value: get_code_description(code.value, dimension)
        for code in codes
    }
    return pd.Series(codes_with_description, name=f"'{dimension.id}' Codes")


def get_constraints_with_codes(data_structure_definition, constraints):
    dimensions = data_structure_definition.dimensions
    return [
        get_constraint_codes(constraints, dimension)
        for dimension in dimensions
    ]


yc_constraints_with_codes = get_constraints_with_codes(yc_data_structure_definition, yc_constraints)
yc_constraints_with_codes

"""
Outputs a list of Series.
The Series' index is set to the code's id and
its value to the code's name.
The Series' name itself is set to the dimension's id:

[
 B    Daily - businessweek
 Name: 'FREQ' Codes, dtype: object,

 U2    Euro area (changing composition)
 Name: 'REF_AREA' Codes, dtype: object,

 EUR    Euro
 Name: 'CURRENCY' Codes, dtype: object,

 4F    ECB
 Name: 'PROVIDER_FM' Codes, dtype: object,

 G_N_W    Government bond, nominal, all issuers whose ra...
 G_N_A    Government bond, nominal, all issuers whose ra...
 G_N_C    Government bond, nominal, all issuers all rati...
 Name: 'INSTRUMENT_FM' Codes, dtype: object,
 ...
]
"""
def parse_series_key(series_key):
    result = {value.id: value.value for value in series_key.values.values()}
    return result

def get_dataflow_series_keys(client, dataflow_id, dataflow_name):
    data_message = client.series_keys('YC')
    series_keys = [parse_series_key(series_key) for series_key in list(data_message)]
    df = pd.DataFrame.from_records(series_keys)
    df.name = f"'{dataflow_name}' Series Keys"
    return df

series_keys = get_dataflow_series_keys(ecb, 'YC', yc_name)
series_keys

"""
Output:

FREQ REF_AREA CURRENCY PROVIDER_FM INSTRUMENT_FM PROVIDER_FM_ID DATA_TYPE_FM
0 B U2 EUR 4F G_N_C SV_C_YM SR_25Y5M
1 B U2 EUR 4F G_N_C SV_C_YM SR_25Y6M
2 B U2 EUR 4F G_N_C SV_C_YM SR_25Y7M
3 B U2 EUR 4F G_N_C SV_C_YM SR_25Y8M
4 B U2 EUR 4F G_N_C SV_C_YM SR_25Y9M
... ... ... ... ... ... ... ...
2160 B U2 EUR 4F G_N_A SV_C_YM IF_5Y6M
2161 B U2 EUR 4F G_N_A SV_C_YM IF_5Y7M
2162 B U2 EUR 4F G_N_A SV_C_YM IF_5Y8M
2163 B U2 EUR 4F G_N_A SV_C_YM IF_5Y9M
2164 B U2 EUR 4F G_N_A SV_C_YM IF_6M
2165 rows × 7 columns
"""
series_keys[series_keys.DATA_TYPE_FM == 'SR_10Y']

"""
Output:

FREQ REF_AREA CURRENCY PROVIDER_FM INSTRUMENT_FM PROVIDER_FM_ID DATA_TYPE_FM
579 B U2 EUR 4F G_N_C SV_C_YM SR_10Y
1655 B U2 EUR 4F G_N_A SV_C_YM SR_10Y
"""