"""
CS230:      Section HB1
Name:       Harshvir Parmar
Data:       Air Bnb
Description:
This program shows you the air bnb properties on  a map in cambridge within your price range and
shows the distribution of properties within a price range as well. There is also a table to view median price
based on neighborhood and a multiselect to view a subset of the data

I pledge that I have completed the programming assignment independently.
I have not copied the code from a student or any source.
I have not given my code to any student.
"""

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


@st.cache
def get_data():
    file = 'data/airbnb_cambridge_listings_20201123.csv'
    return pd.read_csv(file)


def streamlit_sucess(msg):
    messages = {"success": "This visualization was generated using streamlit!",
                "information": "The data for this visualization contains 694 rows and 16 columns",
                "warning": "Streamlit is a very powerful tool"}
    for key, value in messages.items():
        if msg == key in messages:
            if msg == 'success':
                st.success(value)
            elif msg == 'information':
                st.info(value)
            elif msg == 'warning':
                st.warning(value)

def view_subset(defaults, all_cols):
    widget = st.multiselect("Columns", all_cols, default=defaults)
    return st.dataframe(df[widget])


df = get_data()
print(df)


st.image("airbnb.png")
st.title("Final Project")
st.markdown("Cambridge Airbnb data visualized in stream lit")

st.header("Cambridge Airbnb properties in your price range displayed on a map")
user_max = float(st.text_input("Enter the maximum price you would like to pay", "1000"))
user_min = float(st.text_input("Enter the minimum price you would like to pay", "0"))

st.markdown(f"The following map displays the location of all properties priced between {user_min} and {user_max}")
st.map(df.query(f"price>={user_min}&price<={user_max}")[["latitude", "longitude"]].dropna(how="any"))
streamlit_sucess('success')

st.header("What is the distribution of property price?")
st.markdown(
    f"The graph allows you to use the slider on the left to see the distribution of prices within a specific price range")
range = st.sidebar.slider("Price range", float(df.price.min()), 1000., (25., 400.))
list1 = ['price']
df1 = pd.read_csv('data/airbnb_cambridge_listings_20201123.csv', usecols=list1)
fig, ax = plt.subplots()
ax.hist(df1.query(f"price.between{range}"))
plt.xlabel("Price of Properties")
plt.ylabel("Number of Properties")
st.pyplot(fig)
streamlit_sucess('warning')

st.header("What is the median price based on neighborhood")
st.table(df.groupby("neighbourhood").price.median().reset_index() \
         .round(2).sort_values("price", ascending=False) \
         .assign(median_price=lambda x: x.pop("price").apply(lambda y: "%.2f" % y)))

st.subheader("Viewing a Subset of the data")
st.write(f"View the source data how you would like in the table below.")
defaultcols = ["name", "host_name", "neighbourhood", "room_type", "price"]
all_columns = df.columns.tolist()
view_subset(defaultcols, all_columns)
streamlit_sucess('information')

st.header("What is the median and average price based on neighborhood")
df2= df[["neighbourhood","price"]].copy()
df3= df[["neighbourhood","price"]].copy()

df_mean = df2.groupby("neighbourhood").price.mean().reset_index().round(2).sort_values("neighbourhood", ascending=False) \
         .assign(avg_price=lambda x: x.pop("price").apply(lambda y: "%.2f" % y))
df_median = df3.groupby("neighbourhood").price.median().reset_index().round(2).sort_values("neighbourhood", ascending=False) \
         .assign(median_price=lambda x: x.pop("price").apply(lambda y: "%.2f" % y))


frames = [df_median,df_mean]
combined = pd.concat(frames)
st.table(combined)


streamlit_sucess('success')




