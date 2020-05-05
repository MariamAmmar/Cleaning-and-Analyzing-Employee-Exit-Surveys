#!/usr/bin/env python
# coding: utf-8

# **Cleaning and Analyzing Employee Exit Survey Data**
# Which types of Employees are the most dissatisfied?
# 
# This project uses two data sets: one from the Department of Education, Training and Employment (DETE) and the other from the Technical and Further Education (TAFE) institute in Queensland. The purpose of this project is to clean and arrange the data in a way that asnwers the following questions: Are employees that worked for shorter (and longer) periods of time resigning due to some kind of dissatisfaction? Are younger (and older) employees resigning due to some kind of dissatisfaction?
# 

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import numpy as np

dete_survey = pd.read_csv("dete_survey.csv")
tafe_survey = pd.read_csv("tafe_survey.csv")

dete_survey.info()


# In[2]:


tafe_survey.info()


# In[3]:


missing_d = dete_survey.isnull().sum()

missing_t = tafe_survey.isnull().sum()

print(missing_d)
print(missing_t)



# In[4]:


dete_survey.head()


# As we can see above, there are many missing values in both data sets. Most of these values are irrelevent and should be removed. In addition, column names should be changed to aggregate columns from both datasets. 
# 

# In[5]:


dete_survey = pd.read_csv("dete_survey.csv", na_values = "Not Stated")


# In[6]:


dete_survey_updated = dete_survey.drop(dete_survey.columns[28:49], axis = 1)


# In[7]:


dete_survey_updated.head()


# In[8]:


tafe_survey_updated = tafe_survey.drop(tafe_survey.columns[17:66], axis=1)


# These columns were deleted since the data that they contained do not serve the purposes of the missions in this project. 

# In[9]:


dete_survey_updated.columns=dete_survey_updated.columns.str.replace(" ","_").str.strip().str.lower()


# In[10]:


dete_survey_updated.columns


# In[11]:


new_columns = {'Record ID': 'id', 'CESSATION YEAR': 'cease_date', 'Reason for ceasing employment': 'separationtype', 'Gender. What is your Gender?': 'gender', 'CurrentAge. Current Age': 'age',
       'Employment Type. Employment Type': 'employment_status',
       'Classification. Classification': 'position',
       'LengthofServiceOverall. Overall Length of Service at Institute (in years)': 'institute_service',
       'LengthofServiceCurrent. Length of Service at current workplace (in years)': 'role_service'}

tafe_survey_updated = tafe_survey_updated.rename(new_columns, axis = 1)

tafe_survey_updated.columns


# In[12]:


tafe_survey_updated.head()


# Changes where made to relevent column names in order to make working with the data easier. 

# In[13]:


dete_survey_updated["separationtype"].value_counts()


# In[14]:


tafe_survey_updated["separationtype"].value_counts()


# In[15]:


dete_survey_updated["separationtype"] = dete_survey_updated["separationtype"].str.split("-").str[0] 


# In[16]:


dete_survey_updated["separationtype"].value_counts()


# In[17]:


dete_resignations = dete_survey_updated[dete_survey_updated["separationtype"] == "Resignation"].copy()


# In[18]:


tafe_resignations = tafe_survey_updated[tafe_survey_updated['separationtype'] == 'Resignation'].copy()


# In[19]:


dete_resignations.head()

dete_resignations.info()


# In[20]:


dete_resignations.info()


# In the last several lines of code, data from only the resigned employees was filtered since we are interested in finding the reasons as to why people resigned and are not interested in those who retired, were laid off, etc. The DataFrame.copy() method was used to avoid a SettingWithCopy Warning.

# In[21]:


dete_resignations['cease_date'].value_counts()


# In[22]:


dete_resignations['cease_date'] = dete_resignations['cease_date'].str.split('/').str[-1]
dete_resignations['cease_date'] = dete_resignations['cease_date'].astype("float")

dete_resignations['cease_date'].value_counts().sort_index()


# In[23]:


dete_resignations['dete_start_date'].value_counts().sort_index()


# In[24]:


tafe_resignations["cease_date"].value_counts().sort_index()


# In[25]:


box = sns.boxplot(x=dete_resignations["cease_date"])                       



# The years in both dataframes don't completely align. The tafe_survey_updated dataframe contains some cease dates in 2009, but the dete_survey_updated dataframe does not. The tafe_survey_updated dataframe also contains many more cease dates in 2010 than the dete_survey_updaed dataframe. Since the analysis isn't focused on the dates, this will be left as is.

# In[26]:


tafe_resignations["institute_service"].value_counts()


# In[27]:


dete_resignations.columns


# Although there is a column that specifies the duration of workers in tafe_resignations, there isn't one in dete_resignations, so it must be created. 

# In[28]:


dete_resignations["institute_service"] = dete_resignations["cease_date"]- dete_resignations["dete_start_date"]


# In[29]:


dete_resignations["institute_service"].value_counts()


# In[30]:


tafe_resignations["Contributing Factors. Dissatisfaction"].value_counts()


# In[31]:


def update_vals(x):
    if x=="-":
        return False 

    elif pd.isnull(x):
        return np.nan
    
    else:
        return True 



# In[32]:


tafe_resignations["dissatisfied"] = tafe_resignations[['Contributing Factors. Dissatisfaction', 'Contributing Factors. Job Dissatisfaction']].applymap(update_vals).any(1, skipna=False)


# In[33]:


dete_resignations['dissatisfied'] = dete_resignations[['job_dissatisfaction',
       'dissatisfaction_with_the_department', 'physical_work_environment',
       'lack_of_recognition', 'lack_of_job_security', 'work_location',
       'employment_conditions', 'work_life_balance',
       'workload']].any(1, skipna=False)


# In[34]:


tafe_resignations_up = tafe_resignations.copy()
dete_resignations_up = dete_resignations.copy()


# In[35]:


dete_resignations_up['dissatisfied'].head()

tafe_resignations_up["dissatisfied"].head()



# These changes were made in order to identify employees that resigned due to dissatisfaction. The previous columns were chosen as reasons for resignation due to dissatisfaction. 
# 
# If the employee indicated any of the factors above caused them to resign, they are marked  as dissatisfied in a new column titled "dissatisfied" in both dataframes. The new dissatisfied columns  contain just the following values:
# 
# True: indicates a person resigned because they were dissatisfied in some way
# 
# False: indicates a person resigned because of a reason other than dissatisfaction with the job
# 
# NaN: indicates the value is missing

# In[36]:


dete_resignations_up["institute"] = "DETE"
tafe_resignations_up["institute"] = "TAFE"

combined = pd.concat([dete_resignations_up, tafe_resignations_up], ignore_index=True)

combined.columns


# In[37]:


combined_updated = combined.dropna(thresh = 500, axis ="columns").copy()


# In[38]:


combined_updated.head(10)


# The TAFE and DETE data frames have been merged since they have both been cleaned. In addition, columns that have null values greater than 500 were elimnated. 

# In[39]:


combined_updated['institute_service_up'] = combined_updated['institute_service'].astype('str').str.extract(r'(\d+)')
combined_updated['institute_service_up'] = combined_updated['institute_service_up'].astype('float')

combined_updated["institute_service_up"].value_counts().sort_index()


# In[40]:


def transform_service(x):
    if x >= 11:
        return "Veteran"
    elif 7 <= x < 11:
        return "Established"
    elif 3 <= x < 7:
        return "Experienced"
    elif pd.isnull(x):
        return np.nan
    else:
        return "New"        


# In[41]:


combined_updated['service_cat'] = combined_updated['institute_service_up'].apply(transform_service)

combined_updated["service_cat"].value_counts(dropna=False)



# This data was categorized in the following groups since different employees are looking for different things from their companies depending on how long they have been employed with the organization. This is based on BussinessWire article "Age is Just a Number: Engage Employees by Career Stage, Too".
# 

# In[42]:


combined_updated["dissatisfied"].value_counts(dropna=False)


# In[43]:


combined_updated["dissatisfied"] = combined_updated["dissatisfied"].fillna(False)

combined_updated["dissatisfied"].value_counts(dropna=False)


# In[44]:


dis_pct = combined_updated.pivot_table(index='service_cat', values='dissatisfied')

dis_pct.head()

get_ipython().magic('matplotlib inline')
dis_pct.plot(kind='bar', rot=30)


# It seems that new workers (employees of 0-3 years) are the least dissatisfied while established workers (employees of 7-10 years) are the most. This could be due to the possibility that new workers find the work initially intriguing and fail to run in to several issues while established workers may fear getting stuck or lack work/life balance after they have faced the initial obstacles upon entering the organization. Further analysis must be done. 

# In[45]:


combined_updated.isnull().sum()


# In[46]:


combined_updated.head()


# In[47]:


combined_updated["institute_service_up"].astype(float).mean()


# The mean of the values in the "institute_service" column is 7.3 years. It must be decided whether this mean is representative of the series in order to decide whether or not the missing values (a total of 88 in this column) can be replaced using this mean. 

# In[48]:


combined_updated["institute_service_up"]= combined_updated["institute_service_up"].astype(float)


# In[49]:


len(combined_updated["institute_service_up"])


# There are 88 values out of only 651 missing which makes a significant amount of values (13.5%) missing. To simply remove these would result in a reduction of a large percentage of the data and therefore making the series less representative of the population. 

# In[50]:


combined_updated["institute_service_up"].value_counts().sort_index()


# There are a select few outliers such as 41 years and above which coule have skewed the mean of the series. As can be ovserved above, the majority of values lie in the less than 7 years category.  

# The four categories that were used are as follows:
# 
#     Greater than 10 years = Veteran
#     7-11 years = Established
#     3-6 years = Experienced
#     Less than 2 years = New
#     
# Although the mean of 7 fits into the "Etablished" category, we will fill in the missing values with a number that correlates with the "Experienced" category. Not only does this account for the fact that the mean is on the lower end of the spectrum for the "Established" category, but it would also help balance out the outliers that skew the mean upward. In addition, according to Forbes article title "True Or False? 'Employees Today Only Stay One Or Two Years'", the average employee stays at the same company for 4.6 years. 
# 
# The mean of 4.6 will be used to replace the missing values in the series. 
#     

# In[51]:


combined_updated["institute_service_up"] = combined_updated["institute_service_up"].fillna(4.6)


# In[52]:


combined_updated["institute_service_up"].value_counts(dropna = False)


# In[53]:


combined_updated['service_cat'] = combined_updated['institute_service_up'].apply(transform_service)
combined_updated['service_cat'].value_counts(dropna = False)


# In[54]:


dis_pct_2 = combined_updated.pivot_table(index='service_cat', values='dissatisfied')

get_ipython().magic('matplotlib inline')
dis_pct.plot(kind='bar', rot=30)


# The Established group remains the most dissatisfied. 

# In[55]:


combined_updated["age"].value_counts().sort_index()


# In[56]:



def clean_col(col):
    col = col.replace("-"," ")
    col = col.strip()
    return col 

combined_updated["age"] = combined_updated["age"].astype(str)
combined_updated["age"] = combined_updated["age"].apply(clean_col)




# In[57]:


combined_updated["age_cleaned"] = combined_updated["age"].str.split(" ").str.get(0)
combined_updated["age_cleaned"].value_counts().sort_index()


# In[58]:


def sort_age(x):
    if 50 <= x <= 61:
        return "50+"
    elif 40 <= x < 50:
        return "40-49"
    elif 30 <= x < 40:
        return "30-39"
    elif 20 <= x < 30:
        return "20-29"
    else:
        return np.nan
    


# In[59]:


combined_updated['age_cleaned'] = combined_updated['age_cleaned'].astype('float')


combined_updated['age_cleaned'] = combined_updated["age_cleaned"].apply(sort_age)


# In[60]:


combined_updated['age_cleaned'].value_counts().sort_index()


# Now that the age column has been cleaned, the following question can be answered: How many people in each age group resgined due to some kind of dissatisfaction?
#     

# In[61]:


dis_age = combined_updated.pivot_table(index='age_cleaned', values = "dissatisfied")

get_ipython().magic('matplotlib inline')
dis_age.plot(kind='bar', rot=30)


# It seems that as people age, they become slightly more dissatisifed with a significant increase at the 50+ mark. 

# In[62]:


dis_age.head()


# In[63]:


combined_updated.info()


# In[64]:


group = combined_updated.groupby("institute")
dete_group = group.get_group("DETE")

dete_group["dissatisfied"].value_counts()




# In[65]:


group = combined_updated.groupby("institute")
tafe_group = group.get_group("TAFE")

tafe_group["dissatisfied"].value_counts()


# More employees in the DETE survey ended their employment becuase they were dissatisfied in someway (149) as opposed to those in the TAFE survey (91).
