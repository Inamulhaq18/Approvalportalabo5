import boto3
from botocore.exceptions import ClientError
from botocore.exceptions import NoCredentialsError
import requests
import mimetypes
import s3fs
import os
import streamlit as st
import datetime





os.environ["AWS_DEFAULT_REGION"] = 'us-east-2'
os.environ["AWS_ACCESS_KEY_ID"] = 'AKIARLFEN3ZYTWBVYNX7'
os.environ["AWS_SECRET_ACCESS_KEY"] = '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'


s3 = boto3.client('s3')
s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-2',
    aws_access_key_id='AKIARLFEN3ZYTWBVYNX7',
    aws_secret_access_key='+RFrd0HVcFt4AcSbJ+Pkur/1aa88WA6URySQii6Y'
)

def save_uploadedfile(uploadedfile):
     name=str(datetime.datetime.now())
     name=name.replace(".","")
     name=name.replace(":","")
     name=name.replace(" ","")

     typeimage=((uploadedfile.type).replace("image/",""))
     name=name+"."+str(typeimage)
     st.write((name))
     with open(os.path.join(os.getcwd(),name),"wb") as f:
         f.write(uploadedfile.getbuffer())
     return(name)
