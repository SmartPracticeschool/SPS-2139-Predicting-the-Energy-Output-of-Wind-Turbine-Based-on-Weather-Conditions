import boto3,os, sagemaker
from sagemaker import get_execution_role
import numpy as np                                
import pandas as pd                                
from sagemaker.amazon.amazon_estimator import get_image_uri
from sagemaker.session import s3_input,Session
import os
from sagemaker.predictor import csv_serializer 

s3 = boto3.resource('s3')
bucket_name = "turboset"
data_key = "TurboSET.csv"
data_location = "s3://{}/{}".format(bucket_name,data_key)

role = get_execution_role()

my_region = boto3.session.Session().region_name

model_data=pd.read_csv(data_location)

model_data["Date/Time"] = pd.to_datetime(model_data["Date/Time"])

model_data.set_index("Date/Time",inplace=True)

train_data , test_data = np.split(model_data.sample(frac=1, random_state=1729), [int(0.7 * len(model_data))])
print(train_data.shape, test_data.shape)

prefix = 'sagemaker/DEMO-xgboost-dm'
output_path='s3://{}/{}/output'.format(bucket_name,prefix)
print(output_path)

pd.concat([train_data['LV ActivePower (kW)'], train_data.drop(['LV ActivePower (kW)'], axis=1)], axis=1).to_csv('Turbo_Train.csv', index=False, header=False)

pd.concat([train_data['LV ActivePower (kW)'], train_data.drop(['LV ActivePower (kW)'], axis=1)], axis=1).to_csv('Turbo_Test.csv', index=False, header=False)

boto3.Session().resource('s3').Bucket(bucket_name).Object(os.path.join(prefix,'Test/Turbo_Test.csv')).upload_file('Turbo_Test.csv')
s3_input_Test = sagemaker.s3_input(s3_data="s3://{}/{}/Test/Turbo_Test".format(bucket_name,prefix),content_type="csv")

containers = {'us-west-2': '433757028032.dkr.ecr.us-west-2.amazonaws.com/xgboost:latest',
              'us-east-1': '811284229777.dkr.ecr.us-east-1.amazonaws.com/xgboost:latest',
              'us-east-2': '825641698319.dkr.ecr.us-east-2.amazonaws.com/xgboost:latest',
              'eu-west-1': '685385470294.dkr.ecr.eu-west-1.amazonaws.com/xgboost:latest'}

sess = sagemaker.Session()
xgb = sagemaker.estimator.Estimator(containers[my_region],
                                    role, train_instance_count=1,
                                    train_instance_type='ml.m5.large',
                                    output_path=output_path,
                                    sagemaker_session=sess)

xgb.set_hyperparameters(objective='reg:linear',num_round=100)

xgb.fit({'train':s3_input_Train})

xgb_predictor = xgb.deploy(initial_instance_count=1,instance_type='ml.m5.large')




