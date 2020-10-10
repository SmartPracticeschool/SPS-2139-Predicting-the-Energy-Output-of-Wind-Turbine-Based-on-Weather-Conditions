import os
import io
import boto3
import json
import csv

# grab environment variables
ENDPOINT_NAME = "xgboost-2020-10-04-16-09-44-580"
runtime= boto3.client('runtime.sagemaker')

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    
    data = json.loads(json.dumps(event))
    payload = data['data']
    print(payload)
    