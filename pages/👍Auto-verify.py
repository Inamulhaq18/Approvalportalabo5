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
import urllib.request



def skip(product_id):
        sql_select_queryskip = """UPDATE master_product_table SET "Product_approval_status"= %s WHERE "Product_id" = %s"""
        status=str("8")
        curr.execute(sql_select_queryskip, (status,str(product_id),))
        conn.commit()
#initialize the database connection

conn=psycopg2.connect("postgresql://hkmuctkbhmlhsr:59563300aab6c650f8bbc9cc4153df6a42054b71e9be00dda420f40bbbf791b2@ec2-54-76-43-89.eu-west-1.compute.amazonaws.com:5432/dd8a5bspvhrk8c") 
curr=conn.cursor()
url="https://abo5.s3.eu-central-1.amazonaws.com/"
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
pfa=pfa[pfa["Product_id"]>687]


pfa=pfa[pfa["Product_approval_status"]==0]
if pfa.shape[0] ==0:
        "No New Product Available to approve 😔"
if pfa.shape[0] !=0:
        pfa=pfa.sort_values(by="Product_id")
        iterrow=(pfa.iloc[[0]])#taking 535th element of the filtered row
        product_id=(((iterrow["Product_id"]).values)[0])
        st.write(product_id)
        if st.button("Skip if you see an error"):
            skip(product_id)
        st.write(iterrow.shape[0])
        st.write("Product ID : "+str(product_id))
        productname_en=(((iterrow["Product_Name_en"]).values)[0])
        productname_ar=(((iterrow["Product_Name_ar"]).values)[0])
        productdes_en=(((iterrow["Product_describtion_en"]).values)[0])
        productdes_ar=(((iterrow["Product_describtion_ar"]).values)[0])
        tags=(((iterrow["Tags"]).values)[0])
        productdes_en=productdes_en+tags
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
                    'Select a SubCategory',subcatslist,index=subcatindex)
            else:
                    categorysub_ = st.selectbox('Select a sub category',
                    categories1[category_])
            #price




        ##loading images and displaying them
        productdes_en_ = st.text_area('Product Describtion English', productdes_en+tags)
        product_imagesR=(((iterrow["Product_image_R_url"]).values)[0])
        product_rimage=product_imagesR
        if product_imagesR != "NA" and product_imagesR != "" :
            product_imagesR=product_imagesR.replace(" ","").split(",")
            rawimage=list(range(1,len(product_imagesR)+1))
            st.image(product_imagesR,width=100,caption=list(range(1,len(product_imagesR)+1)))

        else:
            st.error("No images uploaded,  skipping")
            skip(product_id)
            if st.button("Skip"):
                    sql_select_queryskip = """UPDATE master_product_table SET "Product_approval_status"= %s WHERE "Product_id" = %s"""
                    status=str("8")
                    curr.execute(sql_select_queryskip, (status,str(product_id),))
                    conn.commit()

        if iterrow["Product_image_P_url"].values[0]=="":
            #api
            imageprocessapi(str(product_rimage))
            st.success("Wait for 15 sec and press R")
        else:

            imagesrembg=(((iterrow["Product_image_P_url"]).values)[0]).split(',')

        if len(iterrow["Product_image_P_url"].values[0])!=0:
                listofrembg=[]
                for i in range(1,len(imagesrembg)+1):
                    listofrembg.append("R"+str(i))

                removed=[]
                for image in imagesrembg:
                    removed.append(image.strip())
                st.image(removed,width=100,caption=listofrembg)
                lst=list(range(1,len(product_imagesR)+1))
                lst=lst+listofrembg

        #Update the data
        product_id=str(product_id)
        price_=str(price_)


        Varient = (iterrow["variety"].values[0])

        varient=Varient



        #Upload new photos 
        def update_raw_image(links,pid):
            sql_select_query = """UPDATE master_product_table SET "Product_image_R_url" = %s WHERE "Product_id" = %s"""

            curr.execute(sql_select_query, (links,pid,))
            conn.commit()

        uploaded_files=st.file_uploader("Upload a file", type=["png", "jpg", "jpeg"], accept_multiple_files=True) 
        images=[]
        urllist=[]
        if len(uploaded_files)>0:
           if st.button("Upload"):
                 for uploaded_file in uploaded_files:
                    bytes_data = uploaded_file.read()
                    name=save_uploadedfile(uploaded_file)
                    #st.write(name)
                    #upload R to s3

                    s3.Bucket('abo5').upload_file(Filename=name, Key=name)
                    urllist.append(url+name)
                 links = ", ".join(urllist)
                 links = product_rimage+", "+links
                 update_raw_image(links,product_id)        

        def upload_img(img):
                name=str(datetime.datetime.now())
                name=name.replace(".","")
                name=name.replace(":","")
                name=name.replace(" ","")
                name=name+"."+"png"
                s3.Bucket('abo5').upload_file(Filename=img, Key=name)
                urllist.append(url+name)
                links = ", ".join(urllist)
                links = product_rimage+", "+links
                update_raw_image(links,product_id)


        with st.expander('rotate images',expanded=False):
               rotatethese = st.multiselect('Select images that are to be rotated',lst)
               direction = st.selectbox("Select the direction to rotate",["Right","Left"])
               if st.button("Process"):
                if rotatethese!="":
                        with st.spinner("Processing your images 😊"):
                         for item in rotatethese:
                             if "R" in str(item):
                                item=item.replace("R","")
                                item=int(item)
                                st.write(item)
                                Product_image_P_url=iterrow["Product_image_P_url"].values[0].split(",")
                                image_to_process=Product_image_P_url[item-1]
                                image_to_process=image_to_process.strip()
                                urllib.request.urlretrieve(image_to_process, "temp.png")
                                img = PILImage.open("temp.png")
                                with PILImage.open("temp.png") as im:
                                        if direction=="Left":
                                            im=im.rotate(90)
                                        if direction=="Right":
                                            im=im.rotate(-90)
                                        im.save('temp.png')
                                        upload_img('temp.png')
                             else:
                                Product_image_P_url=iterrow["Product_image_P_url"].values[0].split(",")
                                image_to_process=Product_image_P_url[item-1]
                                image_to_process=image_to_process.strip()
                                urllib.request.urlretrieve(image_to_process, "temp.png")
                                img = PILImage.open("temp.png")
                                with PILImage.open("temp.png") as im:
                                        if direction=="Left":
                                            im=im.rotate(90)
                                        if direction=="Right":
                                            im=im.rotate(-90)
                                        st.image(im)
                                        im.save('temp.png')
                                        upload_img('temp.png')
                if rotatethese=="":
                        st.write("Please select images to process")


        imgsource=st.multiselect("Final Images",lst,key="finalimages")
        if varient!= None:
            with st.expander("Varient", expanded=True):
                if len (product_imagesR)>0:
                    options=["Select","size", "color", "design"]
                    typev2=st.selectbox("Select varient type", ["Select","size", "color", "design"],key="v02",index=options.index(variety["type"]))
                    varient={"type":typev2}

                    if typev2 == "size":
                        selectedlistsize=[]
                        if "data" in  Varient:
                            selectedlistsize=Varient["data"]
                        datav2=st.multiselect("Select size", ["S", "M", "L", "XL", "XXL", "XXXL", "XXXXL","others1","others2","others3","others4"],key="v002",default=selectedlistsize)
                        #st.write(datav2[0])
            #           varient["data"]=datav2
                        if "S" in datav2:
                            defaultfors=[]
                            if "S_img" in Varient:
                                defaultfors=Varient["S_img"]
                            s_image=st.multiselect("Select Images for S", lst,key="v02q",default=defaultfors)
                            varient["S_img"]=s_image

                        if "M" in datav2:
                            defaultforM=[]
                            if "M_img" in Varient:
                                defaultforM=Varient["M_img"]
                            m_image=st.multiselect("Select Images for M", lst,key="v20q3",default=defaultforM)
                            varient["M_img"]=m_image

                        if "L" in datav2:
                            defaultforL=[]
                            if "L_img" in Varient:
                                defaultforL=Varient["L_img"]
                            l_image=st.multiselect("Select Images for L", lst,key="v2q20",default=defaultforL)    
                            varient["L_img"]=l_image
                        if "XL" in datav2:
                            defaultforXL=[]
                            if "XL_img" in Varient:
                                defaultforXL=Varient["XL_img"]
                            xl_image=st.multiselect("Select Images for XL", lst,key="v2q1",default=defaultforXL)          
                            varient["XL_img"]=xl_image
                        if "XXL" in datav2:
                            defaultforXXL=[]
                            if "XXL_img" in Varient:
                                defaultforXXL=Varient["XXL_img"]
                            xxl_image=st.multiselect("Select Images for XXL", lst,key="v2q4",default=defaultforXXL)      
                            varient["XXL_img"]=xxl_image

                        if "XXXL" in datav2:
                            defaultforXXXL=[]
                            if "XXXL_img" in Varient:
                                defaultforXXXL=Varient["XXXL_img"]
                            xxxl_image=st.multiselect("Select Images for XXXL", lst,key="v2q5",default=defaultforXXXL)     
                            varient["XXXL_img"]=xxxl_image
                        if "XXXXL" in datav2:
                            defaultforXXXXL=[]
                            if "XXXXL_img" in Varient:
                                defaultforXXXXL=Varient["XXXXL_img"]
                            xxxxl_image=st.multiselect("Select Images for XXXXL", lst,key="v2q6",default=defaultforXXXXL)     
                            varient["XXXXL_img"]=xxxxl_image
                        if "others1" in datav2:
                            others1_size_name=st.text_input("Enter name for others1 : ")
                            others1_size_image=st.multiselect("Select Images for others1", lst,key="v2q7") 
                            others1={"others1_img":others1_size_image,"others1_name":others1_size_name}
                            varient["others1"]=others1

                        if "others2" in datav2:
                            others2_size_name=st.text_input("Enter name for others2 : ")
                            others2_size_image=st.multiselect("Select Images for others2", lst,key="v2q8")
                            others2={"others2_img":others2_size_image,"others2_name":others2_size_name}
                            varient["others2"]=others2

                        if "others3" in datav2:
                            others3_size_name=st.text_input("Enter name for others3 : ")
                            others3_size_image=st.multiselect("Select Images for others3", lst,key="v2q9") 
                            others3={"others3_img":others3_size_image,"others3_name":others3_size_name}
                            varient["others3"]=others3

                        if "others4" in datav2:
                            others4_size_name=st.text_input("Enter name for others4 : ")
                            others4_size_image=st.multiselect("Select Images size others4", lst,key="v2q10")
                            others4={"others4_img":others4_size_image,"others4_name":others4_size_name}
                            varient["others4"]=others4

            #        st.write((Varient["data"]))

                    if typev2 == "color":
                        selectedlistcolor=[]
                        if "data" in Varient and Varient["type"]=="color":
                            selectedlistcolor=Varient["data"]
                        datav2=st.multiselect("Select color", ["red", "blue", "green", "yellow", "black", "white","transparent",
                                            "Translucent","Multicolor", "others1","others2","others3","others4"],key="v2",default=selectedlistcolor)
                        varient["data"]=datav2

                        if "red" in datav2:
                            img_red_list=[]
                            if "data" in Varient:
                             if "red" in Varient["data"]:
                                img_red_list=Varient["red_img"]
                            red_image=st.multiselect("Select Images for red", lst,key="v2qas",default=img_red_list)
                            varient["red_img"]=red_image

                        if "blue" in datav2:
                            img_blue_list=[]
                            if "data" in Varient:
                             if "blue" in Varient["data"]:
                                img_blue_list=Varient["blue_img"]
                            blue_image=st.multiselect("Select Images for blue", lst,key="v2qasas",default=img_blue_list)
                            varient["blue_img"]=blue_image

                        if "green" in datav2:
                            img_green_list=[]
                            if "data" in Varient:
                             if "green" in Varient["data"]:
                                img_green_list=Varient["green_img"]
                            green_image=st.multiselect("Select Images for green", lst,key="vasa2q",default=img_green_list)  
                            varient["green_img"]=green_image  

                        if "yellow" in datav2:
                            img_yellow_list=[]
                            if "data" in Varient:
                               if "yellow" in Varient["data"]:
                                img_yellow_list=Varient["yellow_img"]
                            yellow_image=st.multiselect("Select Images for yellow", lst,key="v4as5642q",default=img_yellow_list)
                            varient["yellow_img"]=yellow_image       

                        if "black" in datav2:
                            img_black_list=[]
                            if "data" in Varient:
                              if "black" in Varient["data"]:
                                img_black_list=Varient["black_img"]                
                            black_image=st.multiselect("Select Images for black", lst,key="v2assaq",default=img_black_list)      
                            varient["black_img"]=black_image
                        if "white" in datav2:
                            img_white_list=[]
                            if "data" in Varient:
                             if "white" in Varient["data"]:
                                img_white_list=Varient["white_img"]               
                            white_image=st.multiselect("Select Images for white", lst,key="vdasdas2q",default=img_white_list)     
                            varient["white_img"]=white_image
                        if "transparent" in datav2:
                            img_transparent_list=[]
                            if "data" in Varient:
                             if "transparent" in Varient["data"]:
                                img_transparent_list=Varient["transparent_img"] 
                            transparent_image=st.multiselect("Select Images for transparent", lst,key="v2asdasq",default=img_transparent_list)     
                            varient["transparent_img"]=transparent_image
                        if "Translucent" in datav2:
                            img_translucent_list=[]
                            if "data" in Varient:
                             if "Translucent" in Varient["data"]:
                                img_translucent_list=Varient["Translucent_img"] 
                            translucent_image=st.multiselect("Select Images for Translucent", lst,key="v2dasdasdq",default=img_translucent_list)  
                            varient["translucent_img"]=translucent_image
                        if "Multicolor" in datav2:
                            img_Multicolor_list=[]
                            if "data" in Varient:
                             if "Multicolor" in Varient["data"]:
                                img_Multicolor_list=Varient["multicolor_img"] 
                            multicolor_image=st.multiselect("Select Images for Multicolor", lst,key="v2fasfasq",default=img_Multicolor_list)    
                            varient["multicolor_img"]=multicolor_image

                        if "others1" in datav2:
                            other1_color_name=st.text_input("Enter name for others1 : ")
                            other1_color_image=st.multiselect("Select Images for others1", lst,key="v2gwrdsfxzcq") 
                            otherc1={"otherc1_img":other1_color_image,"otherc1_name":other1_color_name}
                            varient["otherc1"]=otherc1

                        if "others2" in datav2:
                            other2_color_name=st.text_input("Enter name for others2 : ")
                            other2_color_image=st.multiselect("Select Images for others2", lst,key="vgasfdvc2q") 
                            otherc2={"otherc2_img":other2_color_image,"otherc2_name":other2_color_name}
                            varient["otherc2"]=otherc1

                        if "others3" in datav2:
                            other3_color_name=st.text_input("Enter name for others3 : ")
                            other3_color_image=st.multiselect("Select Images for others3", lst,key="v2sdfsdq") 
                            otherc3={"otherc3_img":other3_color_image,"otherc3_name":other3_color_name}
                            varient["otherc3"]=otherc3
                        if "others4" in datav2:
                            other4_color_name=st.text_input("Enter name for others4 : ")
                            other4_color_image=st.multiselect("Select Images size others4", lst,key="v2sdfsdfq") 
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
                            other1_design_image=st.multiselect("Select Images for Design1",lst,key="vsdfsdf2q",default=d1imges)
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
                            other2_design_image=st.multiselect("Select Images for Design2", lst,key="v2sdfcadzfq",default=d2imges)
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
                            other3_design_image=st.multiselect("Select Images for Design3", lst,key="v123122q",default=d3imges)
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
                            other4_design_image=st.multiselect("Select Images for Design4", lst,key="vwrdvsxc2q",default=d4imges)
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
                            other5_design_image=st.multiselect("Select Images for Design5", lst,key="v2wrdsvgzxcq",default=d5imges)
                            otherd5={"otherd5_img":other5_design_image,"otherd5_name":other5_design_name}
                            varient["otherd5"]=otherd5

        varient['imgsource']=imgsource
        varient=json.dumps(varient)
        status=0
        if st.checkbox("Mark as Approved", value=False):
            status=1
        else:
            status=2
        st.write(status)

        if st.button("Update"):
          if len(imgsource)!=0:
                    print("Updating")
                    live_timestamp=str(datetime.datetime.now())
                    sql_select_query = """UPDATE master_product_table SET "Product_Name_en" = %s,
                                        "Product_describtion_en" = %s, "Product_Category" = %s, "Product_subcategory" = %s, 
                                        "Product_price" = %s, "Product_approval_status"= %s, "Product_live_TimeStamp"=%s,"variety"=%s WHERE "Product_id" = %s
                                        """
                    print(status)
                    curr.execute(sql_select_query, (productname_en_,productdes_en_,category_,categorysub_, price_,status,live_timestamp,varient,product_id,))
                    conn.commit()


                    st.success("Updated")
                    st.experimental_rerun()
          if len(imgsource)==0 :
                st.write("Upload Final Image 🥴")





            # print("Table After updating record ")
            # sql_select_query = """select * from master_product_table where "Product_id" = %s"""
            # cur.execute(sql_select_query, (product_id,))
            # record = cur.fetchone()
            # st.write(record)
            # st.write(dat[dat["Product_live_status"]==0].iloc[[71]])




        conn = None
