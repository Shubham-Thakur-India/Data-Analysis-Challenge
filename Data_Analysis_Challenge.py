#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import warnings
warnings.filterwarnings('ignore')


# In[2]:


raw_data=pd.read_csv('C:\\Users\\admin\\Downloads\\Data Analysis Challenge Data Set.csv')


# In[3]:


raw_data.head()


# In[4]:


print('The dataset is a cross sectional data with ',raw_data.shape[0],'rows and ',raw_data.shape[1],'columns.')
print('Columns are: \n',list(raw_data.columns))


# **Count of null entries:**

# In[5]:


Variable_with_null_variables=[]
for i in raw_data.isnull().sum():
    if i>0:
        Variable_with_null_variables.append(i)
Variable_with_null_variables


# **Initial Numrical Data Description:**

# In[6]:


raw_data.describe()


# **Initial Categorical Data Description:**

# In[7]:


raw_data.describe(include='all').loc['count':'freq',].T.dropna()


# Entry '?' seems to be an error, needs further check.

# **Initial Data Format Check:**

# In[8]:


Variable_type=pd.DataFrame(columns=['Variable','Type'])
for i in raw_data.columns:
    dummy_list=[]
    for j in raw_data[i]:
        dummy_list.append(type(j))
    naa=str(set(dummy_list)).split("'")[1]
    Variable_type=Variable_type.append({'Variable':i,'Type':naa},ignore_index=True)
Variable_type


# formats of few variables are wrong. Further check is needed.

# In[9]:


##Check for variables which contains '?'.

(raw_data=='?').sum()


# # Data Cleaning

# In[10]:


##Dropping variable 'normalized-losses' as it containg 41/205 entries as '?'.
raw_data_NL_removed=raw_data.drop('normalized-losses',axis=1)
raw_data_NL_removed.shape


# In[11]:


##Checking remaining variables.

(raw_data_NL_removed=='?').sum()


# In[12]:


##Removing all entries which contains '?'. Since all remaining '?' are in numerical variables. We have no option but to to remove entries.

cleaned_data=raw_data_NL_removed[raw_data_NL_removed != '?'].dropna()


# In[13]:


##Count of entries in remaining variables.
cleaned_data.describe(include='all').T['count']


# In[14]:


##Correcting variable format ( String to float)

cleaned_data[['bore', 'stroke','horsepower', 'peak-rpm','price']]=cleaned_data[['bore', 'stroke','horsepower', 'peak-rpm','price']].astype(float)


# In[15]:


cleaned_data.columns


# In[16]:


##Converting 'symboling' into a string type object. It will help us analyze categorical data easily.
cleaned_data['symboling']=cleaned_data['symboling'].astype(str)


# In[17]:


##Comparison by variable type

Variable_type_corrected=pd.DataFrame(columns=['Variable','Type'])
for i in cleaned_data.columns:
    dummy_list_2=[]
    for j in cleaned_data[i]:
        dummy_list_2.append(type(j))
    naa=str(set(dummy_list_2)).split("'")[1]
    Variable_type_corrected=Variable_type_corrected.append({'Variable':i,'Type':naa},ignore_index=True)
variable_type_comaprison=Variable_type
variable_type_comaprison=variable_type_comaprison.merge(Variable_type_corrected,on='Variable',how='left',suffixes=('_raw', '_cleaned'))
variable_type_comaprison.iloc[1,2]='variable_dropped'
variable_type_comaprison


# In[18]:


## Checking variable details of Categorical Variables:

categorical_variables=list(cleaned_data.describe(include='all').loc['count':'freq',].T.dropna().T.columns)
quantitave_variables=list(cleaned_data.describe().columns)
for i in categorical_variables:
    print(i,list(set(cleaned_data[i])))


# **No error or wrong entry detected (spelling error etc)** 

# # Data Analysis
# **We will be performing analysis on the cleaned dataset.**

# In[19]:


cleaned_data.describe().T


# **Data Summary Categorical Variables:**

# In[20]:


cleaned_data.describe(include='all').loc['count':'freq',].T.dropna()


# Top occurrences and frequency are shown above.
# 
# Gas fueled vehicle are vastly available (90%). Diesel type are hardly there(10%).
# 
# Most vehicle have aspiration='std'.(81.86%), while only 18.14% are 'turbo'.
# 
# Almost all vehicles have engine in front (98.44%).
# 
# Engine type 'ehc' is vastly available (73%). Breakup of rest needs analysis.
# 
# Vehicle with 4 cylinders is vastly available (73%). Breakup of rest needs analysis.
# 
# Rest categories needs further analysis.

# In[21]:


sns.pairplot(cleaned_data[quantitave_variables])


# There seems to be a positive linear relationship between 'city-mpg' and 'highway-mpg'.
# 
# Most vehicle have compression ratio less than 10.
# 'Wheelbase' seems to have linear positive relationship with 'length','wheelbase','curb-weight','width'.
# 
# 'Wheelbase' seems to have linear positive relationship with 'length' and 'width'.
# 'Wheelbase' seems to have negative relationship with 'city-mpg' and 'highway-mpg'.
# 
# 'Price' seems to have negative relationship with 'city-mpg' and 'highway-mpg'.
# 

# In[22]:


#lets plot heatmap for better understanding
plt.figure(figsize=(15,8))
sns.heatmap(cleaned_data.corr(), annot = True, fmt='.2g',vmin=-1, vmax=1)


# MPG-> The vehicle with more city-mpg will have more highway mpg and vice versa. Lets call it mpg together.
# 
# Incresing any one parameter among  length, width, curb-weight, engine-size, bore and horsepower will greatly reduce MPG.
# 
# Higher the wheelbase, lower the MPG.
# 
# Higher the compression ratio, higher the MPG.
# 
# Higher MPG vehicles are cheaper.
# 
# Price->
# 
# Incresing any one parameter among length, width, curb-weight, engine-size, and horsepower will increase price by significantly.
# 
# Higher the wheelbase, higher the Price.
# 
# Costly vehicle give very less MPG.
# 
# Others->
# 
# Increasing rpm reduces comression ratio and vice versa.

# In[23]:


#Categorical data analysis-
for i in cleaned_data.columns:
    sns.catplot(x=i, kind="count", data=cleaned_data)
    
# We will only analyse the categorical distribution


# Most vehicle are of symbol = 0 followed by symbol = 1, While the safest vehicle with symbol=-2 are least.
# > We can say that safety in most of the vehicle is average.
# Vehicle with gas type fuel is prevalent. 
# 
# Aspiration type std is prevalent.
# 
# Almost all vehicles have an engine in front.
# 
# Ohc engine types are prevalent while rest categories are nearly equal.
# 
# Four-cylinder Vehicles are prominent. while 12 & 3 cylinder vehicles are barely there.
# 
# Most vehicles are fwd wheels driven followed by bwd. 4wd wheels driven vehicle are rarely available.
# 
# Mpfi vehicle is mostly available with 2bbl following suit. Rest lacks behind by a lot with mfi & spfi almost nonexistent.
# 
# The most common maker is Toyota with Nissan in the second position. Mercury vehicles are hardly there.
# 
# Four-door vehicles are more than two-door vehicles.
# 

# In[24]:


sns.catplot(x='make', kind="count",height=5, aspect=3, data=cleaned_data)
plt.xticks(rotation=-90)


# Most common maker is toyota with nissan at second position. Mercury vehicle are hardly there.

# In[25]:


sns.catplot(x='fuel-type',hue='symboling',data=cleaned_data, kind='count')


# In[26]:


plt.figure(figsize=(15,8))
sns.boxplot(x='symboling',y='price',data=cleaned_data)
sns.swarmplot(x="symboling", y="price", data=cleaned_data,palette='dark')


# In[27]:


plt.figure(figsize=(15,8))
sns.boxplot(x='num-of-doors',y='price',data=cleaned_data)
sns.swarmplot(x='num-of-doors', y="price", data=cleaned_data,palette='dark')


# Does not affect price much. Excluding from final file.

# In[28]:


plt.figure(figsize=(15,8))
sns.boxplot(x='make',y='price',data=cleaned_data)
sns.swarmplot(x="make", y="price", data=cleaned_data,palette='dark')
plt.xticks(rotation=-90)


# In[29]:


#for bodytype we will not be considering convertible and hardtop as the observations are too less to make a conclusion.If included might result in biased conclusion.

Major_body_cleaned_data=cleaned_data[cleaned_data != 'convertible']
Major_body_cleaned_data=Major_body_cleaned_data[Major_body_cleaned_data != 'hardtop']
plt.figure(figsize=(15,8))
sns.boxplot(x='body-style',y='price',data=Major_body_cleaned_data)
sns.swarmplot(x="body-style", y="price", data=Major_body_cleaned_data,palette='dark')
plt.xticks(rotation=-90)


# Sedan has higher range of price. In all categories majority of vehichles are in lower price segment with similar price, less models are available as we increase price.

# In[30]:


#for drive-wheels we will not be considering '4wd' as the observations are too less to make a conclusion.If included might result in biased conclusion.

DV_cleaned_data=cleaned_data[cleaned_data != '4wd']
plt.figure(figsize=(8,8))
sns.boxplot(x='drive-wheels',y='price',data=DV_cleaned_data)
sns.swarmplot(x='drive-wheels', y="price", data=DV_cleaned_data,palette='dark')
plt.xticks(rotation=-90)


# Fwd vehicles drive wheels costs less and have lower price range while rws drive wheels vehicles costs more and have higher price range.

# In[31]:


#for fuel-system we will not be considering 'mfi', '1bbl', 'spfi', 'idi', 'spdi' as the observations are too less to make a conclusion. If included might result in biased conclusion.

FS_cleaned_data=cleaned_data
for k in [ 'mfi', '1bbl', 'spfi', 'idi', 'spdi']:
    FS_cleaned_data=FS_cleaned_data[FS_cleaned_data['fuel-system']!=k]
plt.figure(figsize=(8,8))
sns.boxplot(x='fuel-system',y='price',data=FS_cleaned_data)
sns.swarmplot(x='fuel-system', y="price", data=FS_cleaned_data,palette='dark')
plt.xticks(rotation=-90)


# 'mpfi' vehicles have a higher price and have a wide range of price while 2bbl is cheap and saturated around 7500

# In[ ]:




