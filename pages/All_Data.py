from cmath import nan
import psycopg2
import pandas as pd
import streamlit as st
import datetime 
from rembg import remove
from PIL import Image as PILImage
import requests
from io import BytesIO
import json
from categories import *
from abo5s3 import *


conn=psycopg2.connect("postgresql://hkmuctkbhmlhsr:59563300aab6c650f8bbc9cc4153df6a42054b71e9be00dda420f40bbbf791b2@ec2-54-76-43-89.eu-west-1.compute.amazonaws.com:5432/dd8a5bspvhrk8c") 
curr=conn.cursor()


#loading the data
sql = "SELECT * FROM master_product_table"
dat = pd.read_sql_query(sql,conn)

st.write(dat)
