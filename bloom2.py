import requests
import streamlit as st
API_URL = "https://api-inference.huggingface.co/models/bigscience/bloom"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()


Productname=st.text_input("Product Name","")
keywords=st.text_input("Keywords","")
text="""
Product Description for "White and Gold Knives":
Beautiful and functional, these cutlery sets are perfect for every kitchen. The knives are designed to have a beautiful look, but are also strong and durable. With a range of different colors, you can find the perfect set for your kitchen. The sets come with an assortment of kitchen knives, including a chef knife, bread knife, and carving knife. The sets also come with a sheath for safe storage. These knives are dishwasher safe.

Product Description for "Paper Plates":
Paper plates are often used for take-out or in situations where disposable plates are needed. Paper plates are durable and can be reused. They are environmentally friendly, as they can be recycled or composted. They are also lightweight and don't break easily. Paper plates are great for parties and family gatherings.

Product Description for "Big Broom":
The Big Broom is the perfect household item for anyone with a lot of floors to sweep. It's lightweight and durable, making it easy to sweep and maintain your floors. The handle is long enough to get under couches and other furniture, and the bristles are durable enough to clean deep down in cracks and crevices.

Product Description for "Men's Wallet":
Sleek and lightweight, this is the perfect wallet for the man on the go. With enough room for your ID, credit cards, and cash, this wallet is perfect for a night out on the town.

Product Description for "Cleaning Towel":
The place where you and your family can unwind and relax. But it can be difficult to keep up with the day-to-day cleaning. Keep your home looking fresh and clean with the Cleaning Towel. This is a towel that has been infused with the power of microfiber. This technology makes it possible for the towel to clean your home from top to bottom without any extra effort on your part. The towel can clean floors, countertops, windows, mirrors, and more. The towel is also durable and will last for years.

Product Description for {}:
""".format(Productname)

output = query({
            "inputs": text,
            "parameters": {"max_new_tokens": 100,
                        "min_length":100,
                        "return_full_text": False,
                        "repetition_penalty":0.00,


                        }
    })

st.write((output[0]["generated_text"]).replace(text,""))