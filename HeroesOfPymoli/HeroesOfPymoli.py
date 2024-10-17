#!/usr/bin/env python
# coding: utf-8

# In[408]:

import os
print("Current working directory before")
print(os.getcwd())


import pandas as pd


resource_file_path = "Resources/purchase_data.csv"
# Check the encoding
with open(resource_file_path) as f:
    print(f)


df = pd.read_csv(resource_file_path)
# Preview data
df.head()


# Check if data needs to be cleaned
df.count()


# ### Player Count
# - Display the total number of players

# Count total number of players
total_players = len(df.groupby("SN"))
print(f"Total Players: \n{total_players}")


# ### Purchasing Analysis (Total)
# - Run basic calculations to obtain number of unique items, average price, etc.
# - Create a summary data frame to hold the results
# - Optional: give the displayed data cleaner formatting
# - Display the summary data frame


# Number of Unique Items
unique_items_number = len(df["Item Name"].unique())

# Average Purchase Price
average_purchase_price = round(df["Price"].mean(),2)

# Total Number of Purchases
total_number_purchases = len(df["Purchase ID"])

# Total Revenue
total_revenue = df["Price"].sum()

purchasing_analysis = pd.DataFrame({
    "Number of Unique Items":[unique_items_number],
    "Average Price":[f"${average_purchase_price}"],
    "Number of Purchases":[total_number_purchases],
    "Total Revenue":[f"${total_revenue}"]
})
print(purchasing_analysis)


# ### Gender Demographics
# - Percentage and Count of Male Players
# - Percentage and Count of Female Players
# - Percentage and Count of Other / Non-Disclosed

gender = ["Female", "Male", "Other / Non-Disclosed"]

# Create function to count players by gender, argument specifies the gender
def count_players_by_gender(val):
    if val in [gender[0], gender[1]]:
        gender_df = df.loc[df['Gender'] == val]
    else: gender_df = df.loc[(df['Gender'] != gender[0])&(df['Gender'] != gender[1])
]
# Using groupby allows not to count the same person several times
    gender_players_count = len(gender_df.groupby("SN"))
    return gender_players_count

# Create Lists to store Gender Demographics related data
gender_count = [count_players_by_gender(val) for val in gender]

gender_percentage = [round(val/total_players*100, 2) for val in gender_count]

# Create DataFrame 
gender_demographics = pd.DataFrame({
    "Total Count":gender_count,
    "Percentage of Players":gender_percentage},
    index = gender)

gender_demographics["Percentage of Players"] = gender_demographics["Percentage of Players"].map("{}%".format)
print(gender_demographics)


# ### Purchasing Analysis (Gender)
# - Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender
# - Create a summary data frame to hold the results
# - Optional: give the displayed data cleaner formatting
# - Display the summary data frame



# The below each broken by gender
# Define function to calculate count by gender
def count_by_gender(val):
    purchase_count_by_gender = df[["Gender", "Purchase ID"]].groupby(["Gender"]).count()
    return purchase_count_by_gender['Purchase ID'][val]

# Purchase Count
purchase_count = [count_by_gender(val) for val in gender]

# Average Purchase Price
purchase_price_by_gender = df[["Gender", "Price"]].groupby(["Gender"]).sum()

average_purchase = [
    round(purchase_price_by_gender['Price'][val]/purchase_count[gender.index(val)],2) for val in gender]

# Total Purchase Value
total_purchase = purchase_price_by_gender["Price"]

# Average Purchase Total per Person by Gender
# At first apply groupby by both columns - Gender and SN to find out the total purchase sum by each player
purchase_per_person = df[["Gender", "SN", "Price"]].groupby(["Gender", "SN"]).sum()

# Then use group by only by Gender to find the average purshase total per person by gender
average_purchase_per_person = round(purchase_per_person.groupby("Gender").mean(), 2)

avg_total = average_purchase_per_person["Price"]

# Create summary DataFrame
purchasing_analysis = pd.DataFrame({
    "Purchase Count": purchase_count,
    "Average Purchase Price": average_purchase,
    "Total Purchase Value": total_purchase,
    "Avg Total Purchase per Person": avg_total},
    index = gender
)
# Format table
purchasing_analysis["Average Purchase Price"] = purchasing_analysis["Average Purchase Price"].map("${:.2f}".format)
purchasing_analysis["Total Purchase Value"] = purchasing_analysis["Total Purchase Value"].map("${:.2f}".format)
purchasing_analysis["Avg Total Purchase per Person"] = purchasing_analysis["Avg Total Purchase per Person"].map("${:.2f}".format)

print(purchasing_analysis)


# ### Age Demographics
# - Establish bins for ages
# - Categorize the existing players using the age bins. Hint: use pd.cut()
# - Calculate the numbers and percentages by age group
# - Create a summary data frame to hold the results
# - Optional: round the percentage column to two decimal points
# - Display Age Demographics Table



# The below each broken into bins of 4 years (i.e. &lt;10, 10-14, 15-19, etc.)
# Define min and max age of players to use it to form bins
min_age = df["Age"].min()
max_age = df["Age"].max()

# Create bins to categorize players by age, set the last bin[8] explicitly to the max age
bins = [x for x in range(min_age-3, max_age, 5)]
bins[8] = max_age

# Create bins labels
bins_labels = ["<10", "10-14", "15-19", "20-24", "25-29",
               "30-34)", "35-39", "40+"]

# Create DataFrame from the df with sorted values by Age to add the binning to
all_players_by_age_bins = df.sort_values(by = "Age")

# Add Column Age Group to categorize players by Age
all_players_by_age_bins["Age Group"] = pd.cut(all_players_by_age_bins["Age"], bins, labels = bins_labels)

# Change the values from categorical to string not to have NaN values while using groupby
all_players_by_age_bins["Age Group"] = all_players_by_age_bins["Age Group"].astype("str")

# Calculate the number of unique players in each age group. First Group By by both Age Group and SN to get unique
# players in each group, then group by Age Group to count unique players

total_players_by_age_bins = all_players_by_age_bins[["Age Group", "SN"]].groupby(
    ["Age Group", "SN"], sort = False)["SN"].count().groupby("Age Group").count()

# Create a list that holds percentage of players in total number of players by age group 
percentage_players_by_age = [f"{round(x/total_players*100,2)}%" for x in total_players_by_age_bins]

# Create a summary DataFrame
age_demographics = pd.DataFrame({
    "Total Count":total_players_by_age_bins,
    "Percentage of Players":percentage_players_by_age},
    index = bins_labels)
print(age_demographics)


# ### Purchasing Analysis (Age)
# - Bin the purchase_data data frame by age
# - Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. in the table below
# - Create a summary data frame to hold the results
# - Optional: give the displayed data cleaner formatting
# - Display the summary data frame


# Purchase Count
purchase_count_by_age_bins = all_players_by_age_bins[["Age Group", "Purchase ID"]].groupby(
    ["Age Group"], sort = False)["Purchase ID"].count()

# Average Purchase Price
average_price_by_age_bins = round(all_players_by_age_bins[["Age Group", "Price"]].groupby(
    "Age Group", sort = False)["Price"].mean(), 2)

# Total Purchase Value
total_value_by_age_bins = round(all_players_by_age_bins[["Age Group", "Price"]].groupby(
    "Age Group", sort = False)["Price"].sum(), 2)

# Average Purchase Total per Person by Age Group
total_by_age_bins = all_players_by_age_bins.groupby(
    ["SN", "Age Group"], sort = False).sum()

average_total_by_age_bins = round(total_by_age_bins.groupby(
"Age Group", sort = False)["Price"].mean(),2)

# Summary DataFrame for Purchasing Analysis (Age)
purchasing_analysis_by_age = pd.DataFrame({
    "Purchase Count": purchase_count_by_age_bins,
    "Average Purchase Price": average_price_by_age_bins,
    "Total Purchase Value": total_value_by_age_bins,
    "Avg Total Purchase per Person": average_total_by_age_bins},
index = bins_labels)

# Format summary table
purchasing_analysis_by_age["Average Purchase Price"] = purchasing_analysis_by_age["Average Purchase Price"].map("${:.2f}".format)
purchasing_analysis_by_age["Total Purchase Value"] = purchasing_analysis_by_age["Total Purchase Value"].map("${:.2f}".format)
purchasing_analysis_by_age["Avg Total Purchase per Person"] = purchasing_analysis_by_age["Avg Total Purchase per Person"].map("${:.2f}".format)

print(purchasing_analysis_by_age)


# ### Top Spenders
# - Run basic calculations to obtain the results in the table below
# - Create a summary data frame to hold the results
# - Sort the total purchase value column in descending order
# - Optional: give the displayed data cleaner formatting
# - Display a preview of the summary data frame

# In[418]:


# Identify the top 5 spenders in the game by total purchase value, then list (in a table):
# SN
# Purchase Count
# Average Purchase Price
# Total Purchase Value

# Find Purchase count and total purchase price for each player
top_spenders = df.groupby("SN").agg({
    "Purchase ID": "count",
    "Price": "sum"}).sort_values(by=["Price"], ascending=False)
print(top_spenders)

# Find Average Purchase Price per player
top_spenders["Average Purchase Price"] = round(df.groupby("SN")["Price"].mean(), 2)
print(top_spenders)

top_spenders = top_spenders.rename(columns = {
    "Price": "Total Purchase Value",
    "Purchase ID": "Purchase Count"
})

# Format table to have right columns order and include $ sign for purshases values
top_spenders_format = top_spenders[["Purchase Count", "Average Purchase Price", "Total Purchase Value"]]
top_spenders_format["Average Purchase Price"]=top_spenders_format["Average Purchase Price"].map("${:.2f}".format)
top_spenders_format["Total Purchase Value"]=top_spenders_format["Total Purchase Value"].map("${:.2f}".format)

print("Top spenders:")
print(top_spenders_format.head())


# ### Most Popular Items
# - Retrieve the Item ID, Item Name, and Item Price columns
# - Group by Item ID and Item Name. Perform calculations to obtain purchase count, average item price, and total purchase value
# - Create a summary data frame to hold the results
# - Sort the purchase count column in descending order
# - Optional: give the displayed data cleaner formatting
# - Display a preview of the summary data frame



# Identify the 5 most popular items by purchase count, then list (in a table):
# Item ID
# Item Name
# Purchase Count
# Item Price
# Total Purchase Value


# Define Purchase count and average price for each item
top_items = df.groupby(["Item ID", "'Item Name'"]).agg({
    "Purchase ID": "count",
    "Price": "mean"
})
print (top_items)

# Add column to DF to show the total purchase value for each item
top_items["Total Purchase Value"] = df.groupby(["Item ID", "Item Name"])["Price"].sum()

# Create summary DataFrame sorted by Purchase Count to identify the most popular items
top_items = top_items.rename(columns = {"Purchase ID": "Purchase Count","Price": "Item Price"})
top_items = top_items.sort_values(by = ["Purchase Count"], ascending = False)

# Format table
# Create new DataFrame - top_items_format as we will use top_items table later 
top_items_format = top_items[["Purchase Count", "Item Price", "Total Purchase Value"]]
top_items_format["Total Purchase Value"] = top_items_format["Total Purchase Value"].map("${:.2f}".format)
top_items_format["Item Price"] = top_items_format["Item Price"].map("${:.2f}".format)

print("The most popular items:")
print(top_items_format.head())


# ### Most Profitable Items
# - Sort the above table by total purchase value in descending order
# - Optional: give the displayed data cleaner formatting
# - Display a preview of the data frame


# Identify the 5 most profitable items by total purchase value, then list (in a table):
# Item ID
# Item Name
# Purchase Count
# Item Price
# Total Purchase Value

# To find the most profitable items sort top_items DataFrame by Total Purchase Value
profit_items = top_items.sort_values(by = ["Total Purchase Value"], ascending=False)

# Format table
profit_items["Total Purchase Value"] = profit_items["Total Purchase Value"].map("${:.2f}".format)
profit_items["Item Price"] = profit_items["Item Price"].map("${:.2f}".format)

print("The most profitable items:")
profit_items.head(20)


# ### Analysis of the fantasy game Heroes of Pymoli
# - Players of Male gender constitute the majority of all players: 84.03%.
# - Purchases made by Male gender players make the majority of the total revenue: 1967.64 USD out of 2379.77 USD.
# - The majority of all Players fall into 20-24 years age category: 44.79%.
# - Players in 20-24 age category are also the most active purchasers: 1114.06 USD.
# - The most profitable items (4.23 USD: 4.61 USD) are not the most expensive ones (4.93 USD : 4.99 USD).





