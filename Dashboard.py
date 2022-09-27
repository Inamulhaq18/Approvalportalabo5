import psycopg2
from st_aggrid import AgGrid
import pandas as pd
import streamlit as st
import datetime 
from rembg import remove
from PIL import Image
import requests
from io import BytesIO


#initialize the database connection
conn=psycopg2.connect("postgresql://hkmuctkbhmlhsr:59563300aab6c650f8bbc9cc4153df6a42054b71e9be00dda420f40bbbf791b2@ec2-54-76-43-89.eu-west-1.compute.amazonaws.com:5432/dd8a5bspvhrk8c") 
curr=conn.cursor()

#loading the data
sql = "SELECT * FROM master_product_table"
dat = pd.read_sql_query(sql,conn)
pfa=dat.copy()
st.title("Dashboard")

pfa=pfa[pfa["Product_live_status"]==0]
pfa.reset_index(inplace=True)
conn.close()


col1, col2, col3 = st.columns(3)


with col1:
        #numeber of products unapproved
        st.write("Products UnApproved")
        st.error(len(dat[dat["Product_live_status"]==0]))

        

with col2:
        #number of products approved
        st.write("Products Approved")
        st.success(len(dat[dat["Product_approval_status"]==1]))
        #name_ar

        

with col3:
    st.write("Products uploaded today")
    #reading the data from the database
    data_today=dat[["Product_Entry_Timestamp","Product_live_status","user"]]

    #counting the number of products uploaded today
    data_today["Product_Entry_Timestamp"]=pd.to_datetime(data_today['Product_Entry_Timestamp'])
    data_today["Product_Entry_Timestamp"]=data_today["Product_Entry_Timestamp"].dt.date
    today=data_today[data_today["Product_Entry_Timestamp"] == datetime.datetime.today().date()]
    st.success(len(data_today[data_today["Product_Entry_Timestamp"] == datetime.datetime.today().date()]))

abeer_count=(len(today[today["user"]=="Abeer"]))
mannar_count=(len(today[today["user"]=="Mannar"]))
waleed_count=(len(today[today["user"]=="Waleed"]))
sami_count=(len(today[today["user"]=="Sami"]))

with col1:
        st.header("Abeer")
        #numeber of products unapproved
        st.write("Products Uploaded Today")
        st.success(abeer_count)

        st.header("Waleed")
        #numeber of products unapproved
        st.write("Products Uploaded Today")
        st.success(waleed_count)
        st.header("Sami")
        #numeber of products unapproved
        st.write("Products Uploaded Today")
        st.success(sami_count)



