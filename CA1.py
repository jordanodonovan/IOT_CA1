#########################################################################################################################
#
#   IoT Real Time Analytics CA1
#   Jordan O'Donovan - x19372016@student.ncirl.ie
#   
#########################################################################################################################

import boto3
import streamlit as st
from dynamodb_json import json_util as json
import pandas as pd
import time

# Connecting to AWS (specifically DynamoDB)
client = boto3.client(
    'dynamodb',
    aws_access_key_id='='#################'',
    aws_secret_access_key='#################'
    )


db = boto3.resource(
    'dynamodb',
    aws_access_key_id='='#################'',
    aws_secret_access_key='='#################''
     )
    
table = db.Table('senseHat_table')

# Webpage settings
st.set_page_config(
    page_title="IoT CA1",
    page_icon="✅",
    layout="wide",
    )
st.title("Jordan O'Donovan x19372016 IoT CA1")

# Setting up the charts to be updated automatically
placeholder = st.empty()

# Creating a loop so that the database & charts are updated automatically
for seconds in range(600):

    # Getting the data from DynamoDB
    response = table.scan()
    db_json = json.loads(response['Items'])

    # Converting the JSON into a Pandas DataFrame
    df = pd.DataFrame.from_records([{**item['payload'], **{'time': item['time']}} for item in db_json])

    # Converting time from milliseconds to a yyyy-mm-dd hh:mm:ss format
    df['time'] = pd.to_datetime(df['time'], unit='ms')

    # Changing data types of columns
    df['Temperature'] = df['Temperature'].astype('float')
    df['Latitude'] = df['Latitude'].astype('float')
    df['Longitude'] =df['Longitude'].astype('float')

    df = df.replace('%', '', regex=True)
    df['Humidity'] = df['Humidity'].astype('float')

    # Renaming the longitude and latitude columns as Streamlit is very specific with the column names
    df = df.rename({'Longitude': 'longitude', 'Latitude': 'latitude'}, axis=1)

    # Creating and sorting by the index as time
    df.index = df['time']
    df = df.sort_index()

    # Node-RED updates every five seconds, so there are 720 instances per hour. This dataframe contains the data for the past hour
    df_lasthr = df[-720:]

    # The charts to be updated automatically
    with placeholder.container():

        st.header("Temperature for the past three minutes")
        st.bar_chart(df['Temperature'][-36:])

        st.header("Pressure for the past three minutes")
        st.line_chart(df['Pressure'][-36:])

        st.header("Humidity for the past three minutes")
        st.area_chart(df['Humidity'][-36:])

        
        # Charts for the past hour

        st.header("Temperature over the past hour")
        chart_data = pd.DataFrame({
        'Value': df_lasthr['Temperature'],
        'Average': df_lasthr['Temperature'].mean(),
        'Minimum': df_lasthr['Temperature'].min(),
        'Maximum': df_lasthr['Temperature'].max()
        })
        st.line_chart(chart_data)

        st.header("Humidity over the past hour")
        chart_data = pd.DataFrame({
        'Value': df_lasthr['Humidity'],
        'Average': df_lasthr['Humidity'].mean(),
        'Minimum': df_lasthr['Humidity'].min(),
        'Maximum': df_lasthr['Humidity'].max()
        })
        st.line_chart(chart_data)

        st.header("Pressure over the past hour")
        chart_data = pd.DataFrame({
        'Value': df_lasthr['Pressure'],
        'Average': df_lasthr['Pressure'].mean(),
        'Minimum': df_lasthr['Pressure'].min(),
        'Maximum': df_lasthr['Pressure'].max()
        })
        st.line_chart(chart_data) 

        # Map
        st.header("Where the Raspberry Pi has been recently")
        st.map(df[['latitude', 'longitude']][-20:])

    # Setting it so database is queried every 5 seconds (same as Node-RED)
    time.sleep(5)
