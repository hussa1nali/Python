import pandas as pd
import json
import requests
import numpy as np
from pandas import json_normalize  # Import json_normalize from the correct module

url = "https://realty-in-au.p.rapidapi.com/properties/list"

querystring = {"channel":"buy","searchLocation":"Willetton, WA 6155","searchLocationSubtext":"Region","type":"region","page":"1","pageSize":"30","sortType":"relevance","surroundingSuburbs":"true","ex-under-contract":"false"}

headers = {
    "X-RapidAPI-Key": "db5ad576ddmsh6a06fb52f495a97p161174jsnd62ba1e007f8",
    "X-RapidAPI-Host": "realty-in-au.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

# Uncomment the line below if you want to print the JSON response
# jprint(response.json())

# Load the JSON data into a Pandas DataFrame
data = response.json()
tiered_results = data['tieredResults']
results = []
for tier in tiered_results:
    results.extend(tier['results'])

# Flatten the nested dictionaries in the 'generalFeatures' column
df = json_normalize(results, sep='_')

