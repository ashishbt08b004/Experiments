
# coding: utf-8

# In[9]:


import pandas as pd
import os
os.chdir('D:/OneDrive - NOAH DATA PVT LTD/New Volume/Personal/ADAlytix')
data=pd.read_csv('DallasData.csv')
#data.head()


# In[91]:


#zip_groups=data.groupby('zip')['zip'].count().sort_values(ascending=False)
zip_groups=data.groupby('zip')['zip'].count()
zip_groups1=zip_groups[zip_groups.values>10].sort_values(ascending=False)
zip_groups2=zip_groups.nlargest(10)
#zip_groups2


# In[10]:


# Filtering zips which has substantial number of customers
def filter_zip(data,min_cust_num,large_zip):
    zip_groups=data.groupby('zip')['zip'].count()
    zip_groups1=zip_groups[zip_groups.values>min_cust_num].sort_values(ascending=False)
    zip_groups2=zip_groups.nlargest(10)
    return zip_groups1,zip_groups2
#filter_zip(data,15,20)   


# In[11]:


# Concatenating all the 4 cities data
Dallas_data=pd.read_csv('DallasData.csv')
SaltLake_data=pd.read_csv('SaltLakeData.csv')
Washington_data=pd.read_csv('WashingtonDCData.csv')
Houston_data=pd.read_csv('HoustonData.csv')
data_tot=pd.concat([Dallas_data,SaltLake_data,Washington_data,Houston_data],axis=0)


# In[14]:


# Creating correct tenure (days active) for inactive customers
t=data_tot['services_completed'].values.tolist()
def tenure_inactive(t): #t should be a list
    b=[(i/5)*365 if i<=5 else 365+((i-5)/4)*365 for i in t]
    return b
data_tot['days_active_tenure']=tenure_inactive(data_tot['services_completed'].values.tolist())


# In[16]:


data_tot['tot_rev']=((data_tot['active_status']*data_tot['days_old']+(1-data_tot['active_status'])*data_tot['days_active_tenure'])/365)*(data_tot['avg_contract_value'])


# In[17]:


data_tot['new_tenure']=data_tot['active_status']*data_tot['days_old']+(1-data_tot['active_status'])*data_tot['days_active_tenure']


# In[18]:


# Data Cleaning: Removing Nulls with forward fill inside each zip group
data_mod=data_tot.groupby('zip')
data_clean=pd.DataFrame()
for name,data_group in data_mod:
    data_group1=data_group.fillna(method='ffill')
    data_clean=pd.concat([data_clean,data_group1],axis=0)
data_clean.to_csv('data_clean.csv')       
    


# In[20]:


# Averaging variables of interest for each zip. To be used for heatmap as-well-as modeling.
varlist=['new_tenure', 'avg_contract_value', 'distance_in_miles', 'population_current', 'gender_male',	'age_median', 'race_white',	'crime_overall', 'households_total', 'households_value', 'households_yearbuilt', 'households_occupancy_owned',	'income_average',	'income_median', 'costs_overall']
data_avg=data_clean.groupby('zip')[varlist].mean()
data_final=data_avg.dropna(axis=0, how='any')
data_final.to_csv('data_final.csv') 

