import requests
import streamlit as st
API_URL = "https://api-inference.huggingface.co/models/bigscience/bloom"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()


Productname=st.text_input("Product Name","")
keywords=st.text_input("Keywords","")
text="""Product Description for "White and Gold Knives" using the keywords "Kitchen", "White and Gold","Dishwasher Safe" :
Beautiful and functional, these cutlery sets are perfect for every kitchen. The knives are designed to have a beautiful look, but are also strong and durable. With a range of different colors, you can find the perfect set for your kitchen. The sets come with an assortment of kitchen knives, including a chef knife, bread knife, and carving knife. The sets also come with a sheath for safe storage. These knives are dishwasher safe.

Product Description for "Pizza Cutter wooden axe handle" using the keywords "axe handle shape", and "Pizza":
A wooden pizza cutter shaped like an axe. The pizza cutter is an attractive way to make a delicious pie. The shape of the pizza cutter makes it easy to cut even the most crusty pizza. A wooden pizza cutter shaped like an axe. The pizza cutter is an attractive way to make a delicious pie. The shape of the pizza cutter makes it easy to cut even the most crusty pizza.
 
Product Description for "Paper Plates" using the keywords "Disposable", "Durable" and "take-out":
Paper plates are often used for take-out or in situations where disposable plates are needed. Paper plates are durable and can be reused. They are environmentally friendly, as they can be recycled or composted. They are also lightweight and don't break easily. Paper plates are great for parties and family gatherings.

Product Description for {} using the keywords {} :
""".format(Productname,keywords)
#if Productname!="" and keywords!="":
    #st.write(text)
output = query({
            "inputs": text,
            "parameters": {"max_new_tokens": 100,
                        "min_length":100,
                        "return_full_text": False,

                        }
    })

st.write((output[0]["generated_text"]).replace(text,""))