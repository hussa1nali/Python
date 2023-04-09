import pandas as pd
import json
import requests
import numpy as np
from pandas import json_normalize  # Import json_normalize from the correct module

url = "https://realty-in-au.p.rapidapi.com/properties/list"

querystring = {"channel":"buy",
               "searchLocation":"Willetton, WA 6155",
               "searchLocationSubtext":"Region",
               "type":"region",
               "page":"1",
               "pageSize":"30",
               "sortType":"relevance",
               "surroundingSuburbs":"False",
               "ex-under-contract":"true"}

headers = {
    "X-RapidAPI-Key": "db5ad576ddmsh6a06fb52f495a97p161174jsnd62ba1e007f8",
    "X-RapidAPI-Host": "realty-in-au.p.rapidapi.com"
}

results = []
for page in range(1, 10):  # change 6 to the maximum number of pages you want to retrieve
    querystring['page'] = str(page)  # update the page parameter
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    tiered_results = data['tieredResults']
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
                   #'agency_email',
                   'mainImage_server',
                   'mainImage_name', 
                   'mainImage_uri',
                   'modifiedDate_value',
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
                   'landSize_unit',
                   'landSize_display',
                   'propertyFeatures',
                   'status_label',
                   'description',
                   'title',
                   'nextInspectionTime_endTimeDisplay',
                   'nextInspectionTime_startTime',
                   'nextInspectionTime_endTime',
                   'nextInspectionTime_auction',
                   'address_locality',
                   'address_postcode',
                   'builderProfile_hasDesignsOnPage',
                   'agencyListingId',
                   'generalFeatures_bedrooms_label'


                  ]

# Drop columns from DataFrame
newdf = df.drop(columns_to_drop, axis=1)
# Rename columns
# create a dictionary to map the old column names to new ones
new_names = {
    'features_general_bedrooms': 'Bedrooms',
    'features_general_bathrooms': 'Bathrooms',
    'features_general_parkingSpaces': 'Garage',
    'landSize_value': 'Land_size',
    'price_display': 'Price',
    'address_streetAddress': 'Address',
    'address_suburb': 'Suburb',
    'address_postCode': 'Post_code',
    'status_type': 'Status',
    'nextInspectionTime_dateDisplay': 'Next_Inspection_Date',
    'nextInspectionTime_startTimeDisplay': 'Next_Inspection_Time'
}
# rename the columns using the dictionary
newdf = newdf.rename(columns=new_names)

## -------------this code below is to fix the sale price
import re


# define a regular expression pattern to match numbers
pattern = r'\d{1,3}(?:,\d{3})*\.?\d*'

# define a function to extract the number from the text
# define a function to extract the number from the text
def extract_number(text):
    # check if text contains "million"
    if 'million' in text.lower():
        # find the first number between the dollar sign and "million"
        match = re.search(r'\$(%s)\s*million' % pattern, text, re.IGNORECASE)
        if match:
            # extract the matched string
            number_str = match.group(1)
            # remove commas and convert to float
            number = float(number_str.replace(',', ''))
            # multiply by 1,000,000 and round to nearest integer
            number = round(number * 1000000)
        else:
            number = None
    # check if text contains "k" or "ks"
    elif 'k' in text.lower():
        # check if text starts with "k" or "ks"
        if text.lower().startswith(('k', 'ks')):
            # assume the number is 1 and multiply by 1000
            number = 1000
        else:
            # remove any non-digit characters and convert to integer
            number_str = re.sub(r'[^\d]', '', text)
            if number_str.strip():  # check if number_str is not empty or only whitespace
                if len(number_str) <= 3:
                    number = int(number_str) * 1000
                else:
                    number = int(number_str)
            else:
                number = None
    else:
        # find the first number in the text using the pattern
        match = re.search(pattern, text)
        if match:
            # extract the matched string
            number_str = match.group(0)
            # remove commas and convert to float
            if ',' in number_str:
                number_str = number_str.replace(',', '')
            number = float(number_str)
            # round to nearest integer
            number = round(number)
        else:
            number = None
    return number




# apply the function to the Price column to create a new column with the extracted numbers
newdf['Price_Num'] = newdf['Price'].apply(extract_number)

# print the output column to the console
#print(newdf['Price_Num'])


#the colde below is to analyse prices
import matplotlib.pyplot as plt
import seaborn as sns
# replace missing or invalid values in the Land_size column with zero
newdf['Land_size'] = pd.to_numeric(newdf['Land_size'], errors='coerce').fillna(0)

# create a pivot table with the median price for each combination of propertyType, Bedrooms, and Land_size
pivot_table = newdf.pivot_table(values='Price_Num', index=['propertyType', 'Bedrooms'], columns='Land_size', aggfunc='median')
# Generate a color palette with 5 colors for the 5 land size levels
palette = sns.color_palette("coolwarm", n_colors=5)

# sort the pivot table by the 'Bedrooms' column in descending order
pivot_table = pivot_table.sort_values(by='Bedrooms', ascending=False)

# Create the heatmap with the color palette
sns.heatmap(pivot_table, annot=False, fmt='.0f', cmap=palette, cbar_kws={'label': '{Price} (m)'})

# set the title of the plot
plt.title('Median Price by House Type, Bedrooms, and Land Size')

# show the plot
plt.show()

newdf.to_csv('Data.csv')
pivot_table.to_csv('Pivot.csv')

