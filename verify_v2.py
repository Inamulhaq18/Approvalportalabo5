import psycopg2
import pandas as pd
import streamlit as st
import datetime 
from rembg import remove
from PIL import Image as PILImage
import requests
from io import BytesIO


#initialize the database connection
conn=psycopg2.connect("postgresql://hkmuctkbhmlhsr:59563300aab6c650f8bbc9cc4153df6a42054b71e9be00dda420f40bbbf791b2@ec2-54-76-43-89.eu-west-1.compute.amazonaws.com:5432/dd8a5bspvhrk8c") 
curr=conn.cursor()

#loading the data
sql = "SELECT * FROM master_product_table"
dat = pd.read_sql_query(sql,conn)
pfa=dat.copy()
st.title("Product Approval Portal - Auto")

pfa=pfa[pfa["Product_live_status"]==0]
pfa.reset_index(inplace=True)

iterrow=(pfa.iloc[[538]])
st.write(iterrow)
product_id=(((iterrow["Product_id"]).values)[0])

productname_en=(((iterrow["Product_Name_en"]).values)[0])
productname_ar=(((iterrow["Product_Name_ar"]).values)[0])
productdes_en=(((iterrow["Product_describtion_en"]).values)[0])
productdes_ar=(((iterrow["Product_describtion_ar"]).values)[0])
typev2=(((iterrow["variety"].values[0]))["type"])
tags=(((iterrow["Tags"]).values)[0])



col1, col2, col3 = st.columns(3)


with col1:
        #numeber of products unapproved
        productname_ar_ = st.text_input('Product Name Arabic', productname_ar)
        productdes_en_ = st.text_area('Product Describtion English', productdes_en)
        tags=st.text_area('Tags', productdes_en)


with col2:

        #name_ar
        productname_en_ = st.text_input('Product Name English', productname_en)        #desc_ar    
        productdes_ar_ = st.text_area('Product Describtion Arabic', productdes_ar)
        price=(((iterrow["Product_price"]).values)[0])
        price_ = st.number_input('Price', value=price)
        

with col3:
    cat=(((iterrow["Product_Category"]).values)[0])
    catslist=['Occasions & Holidays', 'Household Gears', 'Antiques & Gifts','Cleaning & Plastics',
        'Personal Care','Stationery & School Supplies','Accessories','MISCELLANEOUS','CLOTHES',
        'Food','NA','Kitchen',"CatFood"]
    catindex=catslist.index(cat)
    category_ = st.selectbox(
    'Select a category',
    catslist,index=catindex)

    #Select Sub category||||||||||||||||||||||||||||||||||||||||||||||||||||||||| Need to configure this part
    subcat=(((iterrow["Product_subcategory"]).values)[0])
    subcatslist=['Occasions & Holidays', 'Household Gears', 'Antiques & Gifts','Cleaning & Plastics',
        'Personal Care','Stationery & School Supplies','Accessories','MISCELLANEOUS','CLOTHES',
        'Food','NA','Kitchen',"CatFood"]
    subcatindex=catslist.index(cat)
    categorysub_ = st.selectbox(
    'Select a SubCategory',
    catslist,index=subcatindex)
    #price

    


##loading images and displaying them
product_imagesR=(((iterrow["Product_image_R_url"]).values)[0])
if product_imagesR != "NA":
    product_imagesR=product_imagesR.replace(" ","").split(",")
    rawimage=list(range(1,len(product_imagesR)+1))
    st.image(product_imagesR,width=100,caption=list(range(1,len(product_imagesR)+1)))
else:
    st.write("No images uploaded")
whitebg = PILImage.open(r"bgimage.png")
imagesrembg=[]
for url in product_imagesR:
    whitebg = PILImage.open(r"bgimage.png")
    #remove background from images url
    response = requests.get(url)
    img = PILImage.open(BytesIO(response.content))
    #BG Removal
    #st.image(img2)
    basewidth=500
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))

    img = img.resize((basewidth, hsize), PILImage.ANTIALIAS)
    maxsize=int(max(img.size)*1.1)
    whitebg=(whitebg.resize((maxsize,maxsize),PILImage.ANTIALIAS))
    img=remove(img)
    img=img.rotate(270,expand=True)
    img = img.crop(img.getbbox())
    img_w, img_h = img.size
    bg_w, bg_h = whitebg.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    whitebg.paste(img, offset, mask = img)
    imagesrembg.append(whitebg)
cap=[]
for i in range (0,len(imagesrembg)):
    st.write(i)
    cap.append("R"+str(i+1))

st.image(imagesrembg,width=150,caption=cap)
st.write(cap)
st.write(rawimage)

    

    
#Update the data
product_id=str(product_id)
price_=str(price_)

#BG removed
# response = requests.get("https://abo5.s3.eu-central-1.amazonaws.com/2022-05-29132730354760.jpeg")
# img = Image.open(BytesIO(response.content))
# with st.expander("BG removed", expanded=False):
#      st.image(remove(img),width=400,caption="Product Image")
Varient = (iterrow["variety"].values[0])

with st.expander("Varient", expanded=True):
    if len (uploaded_files)>0:

        typev2=st.selectbox("Select varient type", ["Select","size", "color", "design"],key="v2")
        varient={"type":typev2}
        if typev2 == "size":

            datav2=st.multiselect("Select size", ["S", "M", "L", "XL", "XXL", "XXXL", "XXXXL","others1","others2","others3","others4"],key="v2")
            #st.write(datav2[0])
            varient["data"]=datav2
            if "S" in datav2:
                s_image=st.multiselect("Select Images for S", lst,key="v2q")
                varient["S_img"]=s_image

            if "M" in datav2:
                m_image=st.multiselect("Select Images for M", lst,key="v2q")
                varient["M_img"]=m_image

            if "L" in datav2:
                l_image=st.multiselect("Select Images for L", lst,key="v2q")    
                varient["L_img"]=l_image
            if "XL" in datav2:
                xl_image=st.multiselect("Select Images for XL", lst,key="v2q")          
                varient["XL_img"]=xl_image
            if "XXL" in datav2:
                xxl_image=st.multiselect("Select Images for XXL", lst,key="v2q")      
                varient["XXL_img"]=xxl_image
            if "XXXL" in datav2:
                xxxl_image=st.multiselect("Select Images for XXXL", lst,key="v2q")     
                varient["XXXL_img"]=xxxl_image
            if "XXXXL" in datav2:
                xxxxl_image=st.multiselect("Select Images for XXXXL", lst,key="v2q")     
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
                

        if typev2 == "color":
            
            datav2=st.multiselect("Select color", ["red", "blue", "green", "yellow", "black", "white","transparent",
                                "Translucent","Multicolor", "others1","others2","others3","others4"],key="v2")
            varient["data"]=datav2
            if "red" in datav2:
                red_image=st.multiselect("Select Images for red", lst,key="v2q")
                varient["red_img"]=red_image

            if "blue" in datav2:
                blue_image=st.multiselect("Select Images for blue", lst,key="v2q")
                varient["blue_img"]=blue_image

            if "green" in datav2:
                green_image=st.multiselect("Select Images for green", lst,key="v2q")  
                varient["green_img"]=green_image  

            if "yellow" in datav2:
                yellow_image=st.multiselect("Select Images for yellow", lst,key="v2q")
                varient["yellow_img"]=yellow_image       

            if "black" in datav2:
                black_image=st.multiselect("Select Images for black", lst,key="v2q")      
                varient["black_img"]=black_image
            if "white" in datav2:
                white_image=st.multiselect("Select Images for white", lst,key="v2q")     
                varient["white_img"]=white_image
            if "transparent" in datav2:
                transparent_image=st.multiselect("Select Images for transparent", lst,key="v2q")     
                varient["transparent_img"]=transparent_image
            if "Translucent" in datav2:
                translucent_image=st.multiselect("Select Images for Translucent", lst,key="v2q")  
                varient["translucent_img"]=translucent_image
            if "Multicolor" in datav2:
                multicolor_image=st.multiselect("Select Images for Multicolor", lst,key="v2q")    
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

        if typev2 == "design":
            datav2=st.multiselect("Select Design", ["Design1","Design2","Design3","Design4","Design5"],key="v2")
            if "Design1" in datav2:
                other1_design_name=st.text_input("Enter name for Design1 : ")
                other1_design_image=st.multiselect("Select Images for Design1", lst,key="v2q")
                otherd1={"otherd1_img":other1_design_image,"otherd1_name":other1_design_name}
                varient["otherd1"]=otherd1
            if "Design2" in datav2:
                other2_design_name=st.text_input("Enter name for Design2 : ")
                other2_design_image=st.multiselect("Select Images for Design2", lst,key="v2q")
                otherd2={"otherd2_img":other2_design_image,"otherd2_name":other2_design_name}
                varient["otherd2"]=otherd2
            if "Design3" in datav2:
                other3_design_name=st.text_input("Enter name for Design3 : ")
                other3_design_image=st.multiselect("Select Images for Design3", lst,key="v2q")
                otherd3={"otherd3_img":other3_design_image,"otherd3_name":other3_design_name}
                varient["otherd3"]=otherd3
            if "Design4" in datav2:
                other4_design_name=st.text_input("Enter name for Design4 : ")
                other4_design_image=st.multiselect("Select Images for Design4", lst,key="v2q")
                otherd4={"otherd4_img":other4_design_image,"otherd4_name":other4_design_name}
                varient["otherd4"]=otherd4
            if "Design5" in datav2:
                other5_design_name=st.text_input("Enter name for Design5 : ")               
                other5_design_image=st.multiselect("Select Images for Design5", lst,key="v2q")
                otherd5={"otherd5_img":other5_design_image,"otherd5_name":other5_design_name}
                varient["otherd5"]=otherd5





if st.button("Update"):

    st.write(productname_ar_)
    
    print("Updating")
    live_timestamp=str(datetime.datetime.now())
    sql_select_query = """UPDATE master_product_table SET "Product_Name_en" = %s, "Product_Name_ar" = %s,
                        "Product_describtion_en" = %s, "Product_describtion_ar" = %s, "Product_Category" = %s,
                        "Product_subcategory" = %s, "Product_price" = %s, "Product_live_status"= 1, "Product_live_TimeStamp"=%s WHERE "Product_id" = %s
                        """
    
    curr.execute(sql_select_query, (productname_en_,productname_ar_,productdes_en_,productdes_ar_,category_,categorysub_,
                                price_,live_timestamp,product_id,))
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

