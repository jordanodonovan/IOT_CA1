# IOT_CA1

To run this system, you must at first setup the flows.json file using Node-RED.

Next you must establish an MQTT connection to AWS IoTCore which will then use the Rule Engine to store that data in a DynamoDB database and use SNS to send email alerts if a value(s) goes above/below a specific treshold. 

Once the database is receiving a stream of data, Python can be used with Boto3 to query the data, before Pandas is used to clean and preprocess it. 

Once the data is ready to be displayed, it will enter a loop in which every five seconds the graphs will automatically update with the most recent data. 

"streamlit run CA1.py" must be run in a command prompt to activate the Streamlit instance.
