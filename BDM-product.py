import streamlit as st
from pymongo import MongoClient
import pandas as pd
from streamlit_tags import st_tags

st.set_page_config(page_title='Product Recommender System Based on Trends')

hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

st.markdown(hide_table_row_index, unsafe_allow_html=True)

def stars (num):
    if num >= 4.5:
        star = '⭐⭐⭐⭐⭐'
    elif (num >= 4) and (num < 4.5):
        star = '⭐⭐⭐⭐'
    elif (num >= 3) and (num < 4):
        star = '⭐⭐⭐'    
    elif (num >= 2) and (num < 3):
        star =  '⭐⭐'
    else:
        star = '⭐'
    return star

st.subheader("Product Recommender System Based on Trends")

client = MongoClient('link here')
db = client['streamlit']
# Create a collection
collection = db['recommended_product']
data = list(collection.find({}))
# data = pd.DataFrame(data)
# data = data.dropna()

with st.sidebar:
    number_items_shown = st.slider("How many suggested product you want to see", 1, len(data))
    try:
        client = MongoClient('mongodb://setyourownmongodb')
        trends = client['streamlit']['trending_item']
        trends = list(trends.find({}))
        trends = pd.DataFrame(trends)
        trends.reset_index(drop=True)
        del trends['_id']
        trends = trends.rename(columns={'Keywords': 'Trends'})
        list_of_trends = trends.iloc[[-1]]['Trends'].values[0]
        final_trends = pd.DataFrame({'Trends': list_of_trends})
        st.table(final_trends)
    except:
            st.write("The trends is not avaliable yet")
            
                

    
st.write(number_items_shown)

for index, row in enumerate(data):
    if index > number_items_shown - 1:
        break

    try:
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.image(row['product_image_link'])
            with col2:
                st.header(f"[{row['product_name']}]({row['product_link']})")
                st.write(f"{row['product_main_category']} - {row['product_sub_category']}")
                st.write(f"Original price is ₹{row['product_actual_price']}")
                off_price = (1- (float(row['product_discount_price'])/ float(row['product_actual_price']))) * 100
                st.write(f"The new discount price is ₹{row['product_discount_price']} **({round(off_price,2)}%)**")
                st.write(f"{stars(float(row['product_ratings']))} ({row['product_ratings']}) - ({row['product_num_of_ratings']} rates)")    
    except:
        pass
