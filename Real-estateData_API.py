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

# Define list of columns to drop
columns_to_drop = ['advertising_region', 
                   'prettyUrl',
                   'standard',
                   'midtier', 
                   'featured',
                   'signature',
                   'constructionStatus',
                   'channel',
                   'showAgencyLogo',
                   'isLinkedExternalChildListing', 
                   'listers',
                   'isExternalChildListing',
                   'productDepth', 
                   'images', 
                   'classicProject',
                   'isSoldChannel',
                   'isBuyChannel', 
                   'signatureProject',
                   'isInternalChildListing',
                   'inspectionsAndAuctions',
                   'isRentChannel',
                   'lister_website',
                   'lister_phoneNumber',
                   'lister_name',
                   'lister_mainPhoto_server',
                   'lister_mainPhoto_name',
                   'lister_mainPhoto_uri',
                   'lister_id',
                   'lister_email',
                   'advertising_region',
                   'advertising_priceRange',
                   'calculator_brandingColors_text',
                   'calculator_brandingColors_primary',
                   'calculator_subtitle', 
                   'calculator_title', 
                   #'address_streetAddress', 
                   #'address_locality',
                   #'address_postcode',
                   #'address_suburb', 
                   #'address_postCode',
                   'address_location_latitude',
                   'address_location_longitude',
                   'address_subdivisionCode', 
                   'address_state', 
                   'address_showAddress',
                   'agency_website',
                   'agency_address_streetAddress',
                   'agency_address_postcode',
                   'agency_address_suburb',
                   'agency_address_state', 
                   'agency_phoneNumber',
                   'agency_brandingColors_text', 
                   'agency_brandingColors_primary',
                   #'agency_name',
                   'agency_logo_images',
                   'agency_logo_links_small',
                   'agency_logo_links_hero image', 
                   'agency_logo_links_default',
                   'agency_logo_links_large',
                   'agency_agencyId', 
                   'agency_email',
                   'mainImage_server',
                   'mainImage_name', 
                   'mainImage_uri',
                   'modifiedDate_value'
                   'generalFeatures_bedrooms_type',
                   'generalFeatures_bedrooms_value',
                   'generalFeatures_bathrooms_label', 
                   'generalFeatures_bathrooms_type',
                   'generalFeatures_bathrooms_value',
                   'generalFeatures_parkingSpaces_label',
                   'generalFeatures_parkingSpaces_type',
                   'generalFeatures_parkingSpaces_value',
                   'landSize_displayAppAbbreviated',
                   'landSize_displayApp', 
                   'landSize_unit'
                  ]

# Drop columns from DataFrame
newdf = df.drop(columns_to_drop, axis=1)
