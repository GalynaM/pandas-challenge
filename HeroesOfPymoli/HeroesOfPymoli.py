#!/usr/bin/env python
# coding: utf-8

# In[195]:


import pandas as pd


# In[196]:


resource_file_path = "Resources/purchase_data.csv"
# Check the encoding
with open(resource_file_path) as f:
    print(f)


# In[265]:


df = pd.read_csv(resource_file_path)
print(df.loc[df["SN"] == "Adairialis76"])
df.head()


# In[282]:


#Check if data needs to be cleaned
df.count()


# In[ ]:


# Count total number of players

grouped_by_players = df.groupby("SN")
players_number = len(grouped_by_players)
print(f"Total number of players: {players_number}")


# In[250]:


### Purchasing Analysis (Total)
# * Number of Unique Items
unique_items = df["Item Name"].unique()
unique_items_number = len(unique_items)
print(f"Number of Unique Items: {unique_items_number}")


# In[251]:


# * Average Purchase Price
average_purchase_price = round(df["Price"].mean(),2)
print(f"Average Purchase Price: ${average_purchase_price}")

# * Total Number of Purchases
total_number_purchases = len(df["Purchase ID"])
print(f"Total Number of Purchases: {total_number_purchases}")

# * Total Revenue
total_revenue = df["Price"].sum()
print(f"Total_revenue: ${total_revenue}")


# In[315]:


### Gender Demographics

# Create function whith argument that should specify gender from Capital letter
def print_count_players_by_gender(gender):
    if gender in ["Female", "Male"]:
        gender_df = df.loc[df['Gender'] == gender]
    else: gender_df = df.loc[(df['Gender'] != "Female")&(df['Gender'] != "Male")
]
    gender_players_count = len(gender_df.groupby("SN"))
    gender_players_percentage = round(gender_players_count/players_number*100, 2)
    print(f"Percentage and Count of {gender} Players: {gender_players_percentage}% ({gender_players_count})")

def count_players_by_gender(gender):
    if gender in ["Female", "Male"]:
        gender_df = df.loc[df['Gender'] == gender]
    else: gender_df = df.loc[(df['Gender'] != "Female")&(df['Gender'] != "Male")
]
    gender_players_count = len(gender_df.groupby("SN"))
    gender_players_percentage = round(gender_players_count/players_number*100, 2)
    return gender_players_count

# Call the function with different parameters
# * Percentage and Count of Male Players
print_count_players_by_gender("Male")

# * Percentage and Count of Female Players
print_count_players_by_gender("Female")

# * Percentage and Count of Other / Non-Disclosed
print_count_players_by_gender("Non-Disclosed gender")


# In[328]:


### Purchasing Analysis (Gender)
# * The below each broken by gender
#   * Purchase Count
purchase_count_by_gender = df[["Gender", "Purchase ID"]].groupby(["Gender"]).count()

male_purchases = purchase_count_by_gender['Purchase ID'][1]
female_purchases = purchase_count_by_gender['Purchase ID'][0]
otherGender_purchases = purchase_count_by_gender['Purchase ID'][2]

print(f"\nPurchase Count By Gender:\nMale: {male_purchases}\nFemale: {female_purchases}\nNon-Disclosed Gender: {otherGender_purchases}")

#   * Average Purchase Price
purchase_price_by_gender = df[["Gender", "Price"]].groupby(["Gender"]).sum()

male_average_purchase = round(purchase_price_by_gender['Price'][1]/count_players_by_gender("Male"),2)
female_average_purchase = round(purchase_price_by_gender['Price'][0]/count_players_by_gender("Female"),2)
otherGender_average_purchase = round(purchase_price_by_gender['Price'][2]/count_players_by_gender("Other"),2)

print(f"\nAverage Purchase Price By Gender:\nMale: {male_average_purchase}\nFemale: {female_average_purchase}\nNon-Disclosed Gender: {otherGender_average_purchase}")

#   * Total Purchase Value
print(f"\nTotal Purchase Value: {purchase_price_by_gender}")

#   * Average Purchase Total per Person by Gender
purchase_per_person = df[["Gender", "SN", "Purchase ID"]].groupby(["Gender", "SN"]).count()
# purchase_per_person = purchase_per_person["Purchase ID"].mean()
purchase_per_person


# In[ ]:




