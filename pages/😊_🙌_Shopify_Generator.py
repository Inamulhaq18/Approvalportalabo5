from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy import delete
import pandas as pd
import streamlit as st 
import psycopg2


engine = create_engine("postgresql://hkmuctkbhmlhsr:59563300aab6c650f8bbc9cc4153df6a42054b71e9be00dda420f40bbbf791b2@ec2-54-76-43-89.eu-west-1.compute.amazonaws.com:5432/dd8a5bspvhrk8c", echo = False)

#Session for DB
Session=sessionmaker(bind=engine)
session=Session
Base=declarative_base()


shopify=pd.read_csv("shopifytemp.csv")
shopifycolumns=list(shopify.columns)
conn=psycopg2.connect("postgresql://hkmuctkbhmlhsr:59563300aab6c650f8bbc9cc4153df6a42054b71e9be00dda420f40bbbf791b2@ec2-54-76-43-89.eu-west-1.compute.amazonaws.com:5432/dd8a5bspvhrk8c") 
curr=conn.cursor()
# Loading approved data from database
sql = "SELECT * FROM master_product_table"
dat = pd.read_sql_query(sql,conn)
pfa=dat
pfa=pfa[pfa["Product_id"]>500]
pfa=pfa[pfa["Product_approval_status"]==0]
pfa=pfa.sort_values(by="Product_id")

#Number of items 
number_of_items=(pfa[pfa["Product_live_status"]==1]).shape[1]

pfa.dropna(subset=["Product_Name_en"])
pfa=pfa[pfa['Product_Name_en']!=""]
pfa=pfa[pfa['Product_image_P_url']!=""]

shopifycolumnss=pd.DataFrame(columns=shopifycolumns)
list(shopifycolumnss.columns)

pfa=pfa.dropna(subset=['variety'])

def getrowlen(row):
   try:
      rowlen=len((row["variety"]['data']))
   except KeyError as error:
      rowlen=1
   return(rowlen)

def handler(row):
  handler.append(row['Product_Name_en'].replace("","_"))
  return(handler)

def dummyentries(lst,rowlen):
   for i in range(1,rowlen):
     lst.append("")
   return(lst)
handler=[]
Title=[ ]
rowdata={}

dfshopify=pd.DataFrame(columns=shopifycolumns)



#The main program
for index, row in pfa.iterrows():
  rowlen=getrowlen(row)
  
  #handler
  handler=[]
  for i in range(1,rowlen+1):
    handler.append(row['Product_Name_en'].replace(" ","_"))
  
  if len(handler)>3:
   dftemp=pd.DataFrame({'Handle':handler})
  
  #productname
  Title=[]
  Title=[row['Product_Name_en'].strip()]
  dummyentries(Title,rowlen)
  
  #Body (HTML)
  Body=[]
  Body= [row['Product_describtion_en'].strip()]
  dummyentries(Body,rowlen)
  
  #vendor
  vendor_=[]
  vendor_=[row['Retail_outlet']]
  dummyentries(vendor_,rowlen)

  #Customer Product type 
  CPT=[]
  CPT = [row['Product_subcategory'].strip()]
  dummyentries(CPT,rowlen)

  #Tags
  tags=[]
  tags=[str(row['Product_Category'].strip()+", " + row['Product_subcategory'].strip())]
  dummyentries(tags,rowlen) 
  
  #Published
  Published=[]
  Published=["TRUE"]
  dummyentries(Published,rowlen)

  #Option1 Name
  if row["variety"]["type"]=="Select":
    option1=""
  else:
    option1=[row["variety"]["type"]]
  dummyentries(option1,rowlen)

  #Option1 Value
  try:
    option1_val=(row["variety"]["data"])
  
  except KeyError as error:
    option1_val=""
    dummyentries(option1_val,rowlen)

  #'Variant Price',price
  price=[row["Product_price"]]
  for i in range(1,rowlen):
    price.append(row["Product_price"])
  VariantPrice=price
  
  #Image Source 
  imgsrc=[row["variety"]]
  image_link=[]
  try:
    imgsel=[]
    data_=(row["variety"]["data"])
    for adata in data_:
      imgsel.append(row["variety"][adata+"_img"])
    for a in imgsel:
      for imgs in a:
        if "R" in str(imgs):
          imgs=imgs.replace("R","")
          p_img=row["Product_image_P_url"].replace("{","")
          p_img=row["Product_image_P_url"].replace("}","")
          p_img=row["Product_image_P_url"].split(",")
          image_link.append(p_img[int(imgs)+1])
        else:
          R_img=row["Product_image_R_url"].replace("{","")
          R_img=row["Product_image_R_url"].replace("}","")
          R_img=row["Product_image_R_url"].split(",")
          image_link.append(R_img[int(imgs-1)])
  except KeyError as error:
    image_link=row["Product_image_R_url"]


  #imageposition
  imageposition=list(range(1,rowlen+1))

  
  # for h in handler:
  #   a={'Handle': h}
  #   df1=df1.append(a, ignore_index = True)
  dftemp=pd.DataFrame({'Handle':handler,'Title':Title,'Body (HTML)':Body,'Vendor':vendor_,'Custom Product Type':CPT,'Tags':tags,'Option1 Name':option1,'Option1 Value':option1_val,'Published':Published,'Variant Price':price,'Image Position':imageposition,'Image Src':image_link})
  dfshopify=dfshopify.append(dftemp,ignore_index=True)
  dftemp=pd.DataFrame({'Handle':handler})

  print(image_link)
  print(imageposition)
  print(option1)
  print(tags)
  print(Title)
  print(handler)
  print("_______________________________________________________________________________________________________________________________")
st.header("😊 🙌")
st.header("Yay ! '{}'  Products Ready to be uploaded ".format(dfshopify.shape[0]))
st.header("")
st.write(dfshopify)
def convert_df(df):
   return df.to_csv().encode('utf-8')

dfshopify=convert_df(dfshopify)
st.download_button(
   "Press to Download",
   dfshopify,
   "file.csv",
   "text/csv",
)
pids=list(pfa['Product_id'])
pids = ''.join(str(pids))
pids=pids.replace("[","")
pids=pids.replace("]","")
pids=pids.replace("'","")

with engine.connect() as con:

   con.execute('UPDATE master_product_table SET "shopify_status" = 1 WHERE "Product_id" IN ({})'.format(pids))
