import pandas as pd
import requests
import json

API_key = "88e9531c9bc34674bdcb7b78191cf65c" # we define a string variable "API_key" with our API key / hållplatser och stationer

#API_key  # we output the content of the variable to check if it is correct

url = 'http://api.sl.se/api2/LineData.json?key=' + API_key + '&model=site'  # definition of the request url and store it in the variable "url"

r = requests.get(url)  # send the request to the API

data = r.json()  # format the response to json format

stationData = pd.DataFrame.from_dict(data['ResponseData']['Result']) # select the information tagged with ResponseData and Result in the data variable
#print(stationData.head() ) # output the first 5 rows of the dataframe named stationData


# 	SiteId	SiteName	StopAreaNumber	LastModifiedUtcDateTime	ExistsFromDate
#5495	2009506	Sollentuna station	5061	2012-03-26 23:55:32.900	2012-06-23 00:00:00.000

API_key_2 = "c9cfa66e7fac4d97820dbbc199a9741d" # we define a string variable "API_key" with our API key for realtime departure data

siteid=str(2009506)

timewindow = str(10)  # define the timewindow variable
#timewindow  # output the variable

url_2 = "http://api.sl.se/api2/realtimedeparturesv4.json?key=" + API_key_2 + "&siteid=" + siteid + "&timewindow=" + timewindow
# create the url variable for the second API call
#print(url_2)

r_2 = requests.get(url_2)  # request the data from the API using the url
data_2 = r_2.json()  # format the data in json

ptågdata = pd.DataFrame.from_dict(data_2['ResponseData']['Trains'])  # store all the bus data in a dataframe
#print(ptågdata.head())

filtered_df = ptågdata[ptågdata['JourneyDirection'] == 1]
filtered_columns_values = filtered_df[['LineNumber','Destination','DisplayTime']].to_dict(orient='records')

  

# Check if there are any results
if not filtered_df.empty:
    # Create a string to store the formatted output
    output_string = "Next trains are:\n"
    
    # Iterate over the rows in the filtered DataFrame
    for index, row in filtered_df.iterrows():
        output_string += f"{row['LineNumber']} {row['Destination']} in {row['DisplayTime']}\n"

    # Remove the trailing "and" and print the final output
    print(output_string[:-4])   
else:
    print("No records found for the specified condition.")
