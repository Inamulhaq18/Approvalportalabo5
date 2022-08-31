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

#initialize the database connection
conn=psycopg2.connect("postgresql://hkmuctkbhmlhsr:59563300aab6c650f8bbc9cc4153df6a42054b71e9be00dda420f40bbbf791b2@ec2-54-76-43-89.eu-west-1.compute.amazonaws.com:5432/dd8a5bspvhrk8c") 
curr=conn.cursor()

def imageprocessapi(links):
    session = requests.Session()
    session.trust_env = False
    links=links
    url="https://abo5imageapi.herokuapp.com/processBG?rurl="
    url=url+links
    response = session.get(url)
    print(response.content)

#loading the data
sql = "SELECT * FROM master_product_table"
dat = pd.read_sql_query(sql,conn)
pfa=dat.copy()
st.title("Product Approval Portal - Auto 👍")
pfa=pfa[pfa["Product_id"]==643]
pfa=pfa[pfa["Product_approval_status"]==0]
pfa=pfa.sort_values(by="Product_id")
iterrow=(pfa.iloc[[0]])#taking 535th element of the filtered row
st.write(iterrow)
product_id=(((iterrow["Product_id"]).values)[0])
st.write("Product ID : "+str(product_id))
productname_en=(((iterrow["Product_Name_en"]).values)[0])
productname_ar=(((iterrow["Product_Name_ar"]).values)[0])
productdes_en=(((iterrow["Product_describtion_en"]).values)[0])
productdes_ar=(((iterrow["Product_describtion_ar"]).values)[0])

variety=(((iterrow["variety"].values[0])))
tags=(((iterrow["Tags"]).values)[0])



col1, col2 = st.columns(2)


with col1:
        #numeber of products unapproved
    productname_en_ = st.text_input('Product Name English', productname_en)
    cat=(((iterrow["Product_Category"]).values)[0])
    if cat in list(categories1.keys()):
        catslist=list(categories1.keys())
        catindex=catslist.index(cat)
        category_ = st.selectbox(
        'Select a category',
        catslist,index=catindex)
    else:
        category_ = st.selectbox(
        'Select a category',
        categories1.keys())

with col2:

        #name_ar
    price=(((iterrow["Product_price"]).values)[0])
    price_ = st.number_input('Price', value=price)
        
    #Select Sub category||||||||||||||||||||||||||||||||||||||||||||||||||||||||| Need to configure this part
    if cat in categories1.keys():
        subcat=(((iterrow["Product_subcategory"]).values)[0])
        if subcat in categories1[cat]:
            subcatslist=categories1[cat]
            subcatindex=subcatslist.index(subcat)
            categorysub_ = st.selectbox(
            'Select a SubCategory',
            catslist,index=subcatindex)
    else:
            categorysub_ = st.selectbox('Select a sub category',
            categories1[category_])
    #price

    


##loading images and displaying them
productdes_en_ = st.text_area('Product Describtion English', productdes_en)
product_imagesR=(((iterrow["Product_image_R_url"]).values)[0])
if product_imagesR != "NA" and product_imagesR != "" :
    product_imagesR=product_imagesR.replace(" ","").split(",")
    rawimage=list(range(1,len(product_imagesR)+1))
    st.image(product_imagesR,width=100,caption=list(range(1,len(product_imagesR)+1)))

else:
    st.write("No images uploaded")

if iterrow["Product_image_P_url"].values[0]=="":
    #api
    ################################################################FIX THIS $##########################################
    imageprocessapi(str("https://abo5.s3.eu-central-1.amazonaws.com/2022-06-20122612494683.jpeg, https://abo5.s3.eu-central-1.amazonaws.com/2022-06-20122614533780.jpeg, https://abo5.s3.eu-central-1.amazonaws.com/2022-06-20122615195637.jpeg, https://abo5.s3.eu-central-1.amazonaws.com/2022-06-20122615843712.jpeg"))
    st.success("Wait for 15 sec and press R")
else:
    
    imagesrembg=(((iterrow["Product_image_P_url"]).values)[0]).split(',')


listofrembg=[]
for i in range(1,len(imagesrembg)+1):
    listofrembg.append("R"+str(i))
st.image(imagesrembg,width=100,caption=listofrembg)

#Update the data
product_id=str(product_id)
price_=str(price_)

#BG removed
# re 
#      st.image(remove(img),width=400,caption="Product Image")
Varient = (iterrow["variety"].values[0])

varient=Varient
lst=list(range(1,len(product_imagesR)+1))
lst=lst+listofrembg

#Upload new photos 
def update_raw_image(links,pid):
    sql_select_query = """UPDATE master_product_table SET "Product_image_R_url" = %s, WHERE "Product_id" = %s
                        """
    
    curr.execute(sql_select_query, (links,pid,))
    conn.commit()
    
uploaded_files=st.file_uploader("Upload a file", type=["png", "jpg", "jpeg"], accept_multiple_files=True) 
images=[]
if len(uploaded_files)>0:
    st.button("Upload"):
         for uploaded_file in uploaded_files:
            bytes_data = uploaded_file.read()
            name=save_uploadedfile(uploaded_file)
            #st.write(name)
            #upload R to s3

            s3.Bucket('abo5').upload_file(Filename=name, Key=name)
            urllist.append(url+name)
         links = ", ".join(urllist)
         links = old+", "+links
         update_raw_images(links,product_id)          



if varient!= None:
    with st.expander("Varient", expanded=True):
        if len (product_imagesR)>0:
            options=["Select","size", "color", "design"]
            typev2=st.selectbox("Select varient type", ["Select","size", "color", "design"],key="v2",index=options.index(variety["type"]))
            varient={"type":typev2}
            
            if typev2 == "size":
                selectedlistsize=[]
                if Varient["data"]:
                    selectedlistsize=Varient["data"]
                datav2=st.multiselect("Select size", ["S", "M", "L", "XL", "XXL", "XXXL", "XXXXL","others1","others2","others3","others4"],key="v2",default=selectedlistsize)
                #st.write(datav2[0])
    #            varient["data"]=datav2
                if "S" in datav2:
                    defaultfors=[]
                    if Varient["S_img"]:
                        defaultfors=Varient["S_img"]
                    s_image=st.multiselect("Select Images for S", lst,key="v2q",default=defaultfors)
                    varient["S_img"]=s_image

                if "M" in datav2:
                    defaultforM=[]
                    if Varient["M_img"]:
                        defaultforM=Varient["M_img"]
                    m_image=st.multiselect("Select Images for M", lst,key="v2q",default=defaultforM)
                    varient["M_img"]=m_image

                if "L" in datav2:
                    defaultforL=[]
                    if Varient["L_img"]:
                        defaultforL=Varient["L_img"]
                    l_image=st.multiselect("Select Images for L", lst,key="v2q",default=defaultforL)    
                    varient["L_img"]=l_image
                if "XL" in datav2:
                    defaultforXL=[]
                    if Varient["XL_img"]:
                        defaultforXL=Varient["XL_img"]
                    xl_image=st.multiselect("Select Images for XL", lst,key="v2q",default=defaultforXL)          
                    varient["XL_img"]=xl_image
                if "XXL" in datav2:
                    defaultforXXL=[]
                    if Varient["XXL_img"]:
                        defaultforXXL=Varient["XXL_img"]
                    xxl_image=st.multiselect("Select Images for XXL", lst,key="v2q",default=defaultforXXL)      
                    varient["XXL_img"]=xxl_image

                if "XXXL" in datav2:
                    defaultforXXXL=[]
                    if Varient["XXXL_img"]:
                        defaultforXXXL=Varient["XXXL_img"]
                    xxxl_image=st.multiselect("Select Images for XXXL", lst,key="v2q",default=defaultforXXXL)     
                    varient["XXXL_img"]=xxxl_image
                if "XXXXL" in datav2:
                    defaultforXXXXL=[]
                    if Varient["XXXXL_img"]:
                        defaultforXXXXL=Varient["XXXXL_img"]
                    xxxxl_image=st.multiselect("Select Images for XXXXL", lst,key="v2q",default=defaultforXXXXL)     
                    varient["XXXXL_img"]=xxxxl_image
                if "others1" in datav2:
                    others1_size_name=st.text_input("Enter name for others1 : ")
                    others1_size_image=st.multiselect("Select Images for others1", lst,key="v2q") 
                    others1={"others1_img":others1_size_image,"others1_name":others1_size_name}
                    varient["others1"]=others1
            
                if "others2" in datav2:
                    others2_size_name=st.text_input("Enter name for others2 : ")
                    others2_size_image=st.multiselect("Select Images for others2", lst,key="v2q")
                    others2={"others2_img":others2_size_image,"others2_name":others2_size_name}
                    varient["others2"]=others2

                if "others3" in datav2:
                    others3_size_name=st.text_input("Enter name for others3 : ")
                    others3_size_image=st.multiselect("Select Images for others3", lst,key="v2q") 
                    others3={"others3_img":others3_size_image,"others3_name":others3_size_name}
                    varient["others3"]=others3

                if "others4" in datav2:
                    others4_size_name=st.text_input("Enter name for others4 : ")
                    others4_size_image=st.multiselect("Select Images size others4", lst,key="v2q")
                    others4={"others4_img":others4_size_image,"others4_name":others4_size_name}
                    varient["others4"]=others4
                    
    #        st.write((Varient["data"]))

            if typev2 == "color":
                selectedlistcolor=[]
                if Varient["data"] and Varient["type"]=="color":
                    selectedlistcolor=Varient["data"]
                datav2=st.multiselect("Select color", ["red", "blue", "green", "yellow", "black", "white","transparent",
                                    "Translucent","Multicolor", "others1","others2","others3","others4"],key="v2",default=selectedlistcolor)
                varient["data"]=datav2
                
                if "red" in datav2:
                    img_red_list=[]
                    if "red" in Varient["data"]:
                        img_red_list=Varient["red_img"]
                    red_image=st.multiselect("Select Images for red", lst,key="v2q",default=img_red_list)
                    varient["red_img"]=red_image

                if "blue" in datav2:
                    img_blue_list=[]
                    if "blue" in Varient["data"]:
                        img_blue_list=Varient["blue_img"]
                    blue_image=st.multiselect("Select Images for blue", lst,key="v2q",default=img_blue_list)
                    varient["blue_img"]=blue_image

                if "green" in datav2:
                    img_green_list=[]
                    if "green" in Varient["data"]:
                        img_green_list=Varient["green_img"]
                    green_image=st.multiselect("Select Images for green", lst,key="v2q",default=img_green_list)  
                    varient["green_img"]=green_image  

                if "yellow" in datav2:
                    img_yellow_list=[]
                    if "yellow" in Varient["data"]:
                        img_yellow_list=Varient["yellow_img"]
                    yellow_image=st.multiselect("Select Images for yellow", lst,key="v2q",default=img_yellow_list)
                    varient["yellow_img"]=yellow_image       

                if "black" in datav2:
                    img_black_list=[]
                    if "black" in Varient["data"]:
                        img_black_list=Varient["black_img"]                
                    black_image=st.multiselect("Select Images for black", lst,key="v2q",default=img_black_list)      
                    varient["black_img"]=black_image
                if "white" in datav2:
                    img_white_list=[]
                    if "white" in Varient["data"]:
                        img_white_list=Varient["white_img"]               
                    white_image=st.multiselect("Select Images for white", lst,key="v2q",default=img_white_list)     
                    varient["white_img"]=white_image
                if "transparent" in datav2:
                    img_transparent_list=[]
                    if "transparent" in Varient["data"]:
                        img_transparent_list=Varient["transparent_img"] 
                    transparent_image=st.multiselect("Select Images for transparent", lst,key="v2q",default=img_transparent_list)     
                    varient["transparent_img"]=transparent_image
                if "Translucent" in datav2:
                    img_translucent_list=[]
                    if "Translucent" in Varient["data"]:
                        img_translucent_list=Varient["Translucent_img"] 
                    translucent_image=st.multiselect("Select Images for Translucent", lst,key="v2q",default=img_translucent_list)  
                    varient["translucent_img"]=translucent_image
                if "Multicolor" in datav2:
                    img_Multicolor_list=[]
                    if "Multicolor" in Varient["data"]:
                        img_Multicolor_list=Varient["multicolor_img"] 
                    multicolor_image=st.multiselect("Select Images for Multicolor", lst,key="v2q",default=img_Multicolor_list)    
                    varient["multicolor_img"]=multicolor_image
                
                if "others1" in datav2:
                    other1_color_name=st.text_input("Enter name for others1 : ")
                    other1_color_image=st.multiselect("Select Images for others1", lst,key="v2q") 
                    otherc1={"otherc1_img":other1_color_image,"otherc1_name":other1_color_name}
                    varient["otherc1"]=otherc1
                
                if "others2" in datav2:
                    other2_color_name=st.text_input("Enter name for others2 : ")
                    other2_color_image=st.multiselect("Select Images for others2", lst,key="v2q") 
                    otherc2={"otherc2_img":other2_color_image,"otherc2_name":other2_color_name}
                    varient["otherc2"]=otherc1

                if "others3" in datav2:
                    other3_color_name=st.text_input("Enter name for others3 : ")
                    other3_color_image=st.multiselect("Select Images for others3", lst,key="v2q") 
                    otherc3={"otherc3_img":other3_color_image,"otherc3_name":other3_color_name}
                    varient["otherc3"]=otherc3
                if "others4" in datav2:
                    other4_color_name=st.text_input("Enter name for others4 : ")
                    other4_color_image=st.multiselect("Select Images size others4", lst,key="v2q") 
                    otherc4={"otherc4_img":other4_color_image,"otherc4_name":other4_color_name}
                    varient["otherc4"]=otherc4
            lstdesign=[]

            if typev2 == "design":
                #checking for design types and appending the list to auto populate 
                lstdesign=[]
                st.write(variety.keys())
                if "otherd1"in variety.keys():
                    lstdesign.append("Design1")
                    design1img=variety
                if "otherd2"in variety.keys():
                    lstdesign.append("Design2")
                if "otherd3"in variety.keys():
                    lstdesign.append("Design3")
                if "otherd4"in variety.keys():
                    lstdesign.append("Design4")
                if "otherd5"in variety.keys():
                    lstdesign.append("Design5")
                # if "1" in variety:
                #     print(varietyR)
                datav2=st.multiselect("Select Design", ["Design1","Design2","Design3","Design4","Design5"],key="v2",default=lstdesign)
                
                if "Design1" in datav2:
                    text=""
                    d1imges=[]   
                    st.write()
                    if variety["type"]=="design"and variety["otherd1"]:
                        text=variety["otherd1"]["otherd1_name"]
                        if variety["otherd1"]["otherd1_img"]:
                            d1imges=variety["otherd1"]["otherd1_img"]
                            st.write(d1imges)
                    other1_design_name=st.text_input("Enter name for Design1 : ",value=text)
                    other1_design_image=st.multiselect("Select Images for Design1",lst,key="v2q",default=d1imges)
                    otherd1={"otherd1_img":other1_design_image,"otherd1_name":other1_design_name}
                    varient["otherd1"]=otherd1
                
                if "Design2" in datav2:
                    text2=""
                    d2imges=[]
                    if variety['type']=="design" and variety["otherd2"]:
                        text2=variety["otherd2"]["otherd2_name"]
                        d2imges=variety["otherd2"]["otherd2_img"]
                    text=""
                    if  variety['type']=="design":
                        text=variety["otherd2"]["otherd2_name"]
                    other2_design_name=st.text_input("Enter name for Design2 : ",value=text2)
                    other2_design_image=st.multiselect("Select Images for Design2", lst,key="v2q",default=d2imges)
                    otherd2={"otherd2_img":other2_design_image,"otherd2_name":other2_design_name}
                    varient["otherd2"]=otherd2

                if "Design3" in datav2:
                    text3=""
                    d3imges=[]
                    if  variety['type']=="design":
                        if variety["otherd3"]:
                            text3=variety["otherd3"]["otherd3_name"]
                            d3imges=variety["otherd3"]["otherd3_img"]

                    other3_design_name=st.text_input("Enter name for Design3 : ",value=text3)
                    other3_design_image=st.multiselect("Select Images for Design3", lst,key="v2q",default=d3imges)
                    otherd3={"otherd3_img":other3_design_image,"otherd3_name":other3_design_name}
                    varient["otherd3"]=otherd3
                
                if "Design4" in datav2:
                    text4=""
                    d4imges=[]
                    if variety["type"]=="design":
                        if variety["otherd4"]:
                            text4=variety["otherd4"]["otherd4_name"]
                            d4imges=variety["otherd4"]["otherd4_img"]
                    other4_design_name=st.text_input("Enter name for Design4 : ",value=text4)
                    other4_design_image=st.multiselect("Select Images for Design4", lst,key="v2q",default=d4imges)
                    otherd4={"otherd4_img":other4_design_image,"otherd4_name":other4_design_name}
                    varient["otherd4"]=otherd4
                
                if "Design5" in datav2:
                    text5=""
                    d5imges=[]
                    if variety["type"]=="design":
                        if variety["otherd5"]:
                            text5=variety["otherd5"]["otherd5_name"]
                            d5imges=variety["otherd5"]["otherd5_img"]
                    other5_design_name=st.text_input("Enter name for Design5 : ",value=text5)               
                    other5_design_image=st.multiselect("Select Images for Design5", lst,key="v2q",default=d5imges)
                    otherd5={"otherd5_img":other5_design_image,"otherd5_name":other5_design_name}
                    varient["otherd5"]=otherd5

varient=json.dumps(varient)
st.write(varient)
if st.checkbox("Mark as Approved", value=False):
    status=1
else:
    status=2


if st.button("Update"):

    st.write(productname_ar_)
    
    print("Updating")
    live_timestamp=str(datetime.datetime.now())
    sql_select_query = """UPDATE master_product_table SET "Product_Name_en" = %s, "Product_Name_ar" = %s,
                        "Product_describtion_en" = %s, "Product_describtion_ar" = %s, "Product_Category" = %s,
                        "Product_subcategory" = %s, "Product_price" = %s, "Product_approval_status"= %s, "Product_live_TimeStamp"=%s,"Tags"=%s,"variety"=%s WHERE "Product_id" = %s
                        """
    
    curr.execute(sql_select_query, (productname_en_,productname_ar_,productdes_en_,productdes_ar_,category_,categorysub_, price_,status,live_timestamp,tags,varient,product_id,))
    conn.commit()

    
    st.success("Updated")
    st.experimental_rerun()




    
    # print("Table After updating record ")
    # sql_select_query = """select * from master_product_table where "Product_id" = %s"""
    # cur.execute(sql_select_query, (product_id,))
    # record = cur.fetchone()
    # st.write(record)
    # st.write(dat[dat["Product_live_status"]==0].iloc[[71]])




conn = None

