#!/usr/bin/env python
# coding: utf-8

# # Importing Libraries

# In[145]:


import pandas as pd
import datetime
from datetime import date, timedelta
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
pio.templates.default = "plotly_white"


# A/B testing is used for experimenting on a new marketing strategy, a new design or even a new game. To make an experiment, two different strategy is tried on two seperate group. One group is called test group and the experimental version is shown to them. Then, the remaining users are called control group and they see the default vesion. 
# 
# According to the results, the better performing version is selected. To decide which version performed better, data analysis can be used to determine.

# # Data Preprocessing

# In[146]:


control_group = pd.read_csv("control_group.csv", sep = ";")
test_group = pd.read_csv("test_group.csv", sep = ";")


# In[147]:


control_group.head()


# In[148]:


test_group.head()


# As it is seen from the dataframes, the column names are a little bit confusing. They will be replaced with a clearer headings.

# In[149]:


control_group.columns = ["Campaign Name", "Date", "Amount Spent", 
                        "Number of Impressions", "Reach", "Website Clicks", 
                        "Searches Received", "Content Viewed", "Added to Cart",
                        "Purchases"]

test_group.columns = ["Campaign Name", "Date", "Amount Spent", 
                        "Number of Impressions", "Reach", "Website Clicks", 
                        "Searches Received", "Content Viewed", "Added to Cart",
                        "Purchases"]


# In[150]:


control_group.head(10)


# In[151]:


control_group.describe()


# In[152]:


test_group.head(10)


# In[153]:


test_group.describe()


# The number of tests for both control group and test group are hopefully equal. Let's check the emty values.

# In[154]:


control_group.isnull().sum()


# In[155]:


test_group.isnull().sum()


# In[156]:


control_group[control_group.isna().any(axis=1)]


# One row value is missing in our control group dataframe. We can drop it as its effect will not be too much on the whole data. However, we should delete the corresponding row from the test data to compare both accurately.

# In[157]:


control_group.dropna(how='any', inplace=True)


# In[158]:


control_group.describe()


# Let's locate the corresponding row from the test data and delete it.

# In[159]:


test_group.loc[test_group['Date'] == '5.08.2019']


# In[160]:


test_group = test_group.drop(4)


# In[161]:


test_group.describe()


# It is time to merge the two campaigns to compare the results easily.

# In[162]:


ab_data = control_group.merge(test_group, 
                             how="outer").sort_values(["Date"])
ab_data = ab_data.reset_index(drop=True)
ab_data.head(10)


# In[163]:


ab_data["Campaign Name"].value_counts()


# Great, now in our A/B test data, there are 29 test cases for a control group and test group.

# # Data Visualization

# In[164]:


figure = px.scatter(data_frame = ab_data, 
                    x="Amount Spent", 
                    y="Number of Impressions",
                    size="Number of Impressions", 
                    color= "Campaign Name", 
                    trendline="ols")
figure.show("notebook")


# Control campaign worked better for the number of impression per amount spent during the campaign.

# In[165]:


label = ["Amount Spent in Control Campaign", 
         "Amount Spent in Test Campaign"]
counts = [sum(control_group["Amount Spent"]), 
          sum(test_group["Amount Spent"])]
colors = ['green','royalblue']
fig = go.Figure(data=[go.Pie(labels=label, values=counts)])
fig.update_layout(title_text='Control Vs Test: Amount Spent')
fig.update_traces(hoverinfo='label+percent', textinfo='value', 
                  textfont_size=30,
                  marker=dict(colors=colors, 
                              line=dict(color='black', width=3)))
fig.show("notebook")


# More amount of money spent for the test campaign. Thus, we expect more results from the test campaign.

# In[166]:


label = ["Total Searches from Control Campaign", 
         "Total Searches from Test Campaign"]
counts = [sum(control_group["Searches Received"]), 
          sum(test_group["Searches Received"])]
colors = ['green','royalblue']
fig = go.Figure(data=[go.Pie(labels=label, values=counts)])
fig.update_layout(title_text='Control Vs Test: Searches')
fig.update_traces(hoverinfo='label+percent', textinfo='value', 
                  textfont_size=30,
                  marker=dict(colors=colors, 
                              line=dict(color='black', width=3)))
fig.show("notebook")


# Test campaign got more searches.

# In[167]:


label = ["Website Clicks from Control Campaign", 
         "Website Clicks from Test Campaign"]
counts = [sum(control_group["Website Clicks"]), 
          sum(test_group["Website Clicks"])]
colors = ['green','royalblue']
fig = go.Figure(data=[go.Pie(labels=label, values=counts)])
fig.update_layout(title_text='Control Vs Test: Website Clicks')
fig.update_traces(hoverinfo='label+percent', textinfo='value', 
                  textfont_size=30,
                  marker=dict(colors=colors, 
                              line=dict(color='black', width=3)))
fig.show("notebook")


# Test campaign got more website click.

# In[168]:


label = ["Content Viewed from Control Campaign", 
         "Content Viewed from Test Campaign"]
counts = [sum(control_group["Content Viewed"]), 
          sum(test_group["Content Viewed"])]
colors = ['green','royalblue']
fig = go.Figure(data=[go.Pie(labels=label, values=counts)])
fig.update_layout(title_text='Control Vs Test: Content Viewed')
fig.update_traces(hoverinfo='label+percent', textinfo='value', 
                  textfont_size=30,
                  marker=dict(colors=colors, 
                              line=dict(color='black', width=3)))
fig.show("notebook")


# Control campaign resulted in more content viewed by customers.

# In[169]:


label = ["Products Added to Cart from Control Campaign", 
         "Products Added to Cart from Test Campaign"]
counts = [sum(control_group["Added to Cart"]), 
          sum(test_group["Added to Cart"])]
colors = ['green','royalblue']
fig = go.Figure(data=[go.Pie(labels=label, values=counts)])
fig.update_layout(title_text='Control Vs Test: Added to Cart')
fig.update_traces(hoverinfo='label+percent', textinfo='value', 
                  textfont_size=30,
                  marker=dict(colors=colors, 
                              line=dict(color='black', width=3)))
fig.show("notebook")


# Customers which are in control group added more products to their charts.

# In[170]:


label = ["Purchases Made by Control Campaign", 
         "Purchases Made by Test Campaign"]
counts = [sum(control_group["Purchases"]), 
          sum(test_group["Purchases"])]
colors = ['green','royalblue']
fig = go.Figure(data=[go.Pie(labels=label, values=counts)])
fig.update_layout(title_text='Control Vs Test: Purchases')
fig.update_traces(hoverinfo='label+percent', textinfo='value', 
                  textfont_size=30,
                  marker=dict(colors=colors, 
                              line=dict(color='black', width=3)))
fig.show("notebook")


# Customers in control group purchased sligtly more than customers in test group, eventhough, customers in the control group added way more products to their chart.

# In[171]:


figure = px.scatter(data_frame = ab_data, 
                    x="Website Clicks", 
                    y="Content Viewed",
                    size="Content Viewed", 
                    color= "Campaign Name", 
                    trendline="ols")
figure.show("notebook")


# Control campaign contributed to more content views per website clicks.

# In[172]:


figure = px.scatter(data_frame = ab_data, 
                    x="Content Viewed", 
                    y="Added to Cart",
                    size="Added to Cart", 
                    color= "Campaign Name", 
                    trendline="ols")
figure.show("notebook")


# Customers in test group added more products to their charts respect to the content views.

# In[173]:


figure = px.scatter(data_frame = ab_data, 
                    x="Added to Cart", 
                    y="Purchases",
                    size="Purchases", 
                    color= "Campaign Name", 
                    trendline="ols")
figure.show("notebook")


# Test group bought more products than control group according to the number of products in their carts.

# Let's check how the customers in both group purchase according to the amount spent for the campaigns.

# In[174]:


figure = px.scatter(data_frame = ab_data, 
                    x="Amount Spent", 
                    y="Purchases",
                    size="Purchases", 
                    color= "Campaign Name", 
                    trendline="ols")
figure.show("notebook")


# # Conclusion

# The overall purchase according to amount of money spent on campaigns are similar for both campaigns. Thus, it is hard to say which one is better for revenue increase. However, it can be said that, the control group campaign resulted in more traffic and more interactions while test group campaign resulted in higher conversion rates. For marketing specific product, the test campaign can work better but for increasing brand awareness, the control campaign would be better.
