if varient!= None:
    with st.expander("Varient", expanded=True):
        if len (product_imagesR)>0:
            options=["Select","size", "color", "design"]
            st.write(variety)
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
