
# coding: utf-8

# In[3]:

#question to answer by this data analysis 1.)Who was being polled and what was their party affiliation?
#2.)Did the poll results favor Romney or Obama?
#3.) How do undecided voters effect the poll?
#4.) Can we account for the undecided voters? 
#5.)How did voter sentiment change over time? 
#6.) Can we see an effect in the polls from the debates?


# In[4]:

import pandas as pd
from pandas import DataFrame,Series
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
sb.set_style('whitegrid')
get_ipython().magic('matplotlib inline')


# In[5]:

from __future__ import division
import requests
from io import StringIO


# In[6]:

url = "http://elections.huffingtonpost.com/pollster/2016-general-election-trump-vs-clinton.csv"

source = requests.get(url).text


pollData = StringIO(source)


# In[7]:

pollDf = pd.read_csv(pollData)

pollDf.info()


# In[8]:

sb.factorplot('Affiliation',kind='count',data=pollDf)


# In[9]:

sb.factorplot('Affiliation',kind='count',data=pollDf,hue='Population')


# In[19]:

avg = pd.DataFrame(pollDf.mean()) 
avg.drop('Number of Observations',axis=0,inplace=True)
avg


# In[20]:

pollDf.mean()


# In[ ]:




# In[12]:

std = pd.DataFrame(pollDf.std())
std.head()


# In[21]:

std


# In[22]:

avg.plot(yerr=std,kind='bar',legend=False)


# In[23]:

poll_avg = pd.concat([avg,std],axis=1) 
poll_avg.columns = ['Average','STD']


# In[24]:

poll_avg


# In[25]:

pollDf.plot(x='End Date',y=['Trump','Clinton','Undecided'],marker='o',linestyle='')


# In[26]:

from datetime import datetime


# In[27]:

pollDf['Difference'] = (pollDf.Trump - pollDf.Clinton)/100
pollDf.head()


# In[28]:

pollDf = pollDf.groupby(['Start Date'],as_index=False).mean()
pollDf.head()


# In[29]:

fig = pollDf.plot('Start Date','Difference',figsize=(12,4),marker='o',linestyle='-',color='red')


# In[30]:

row_in = 0
xlimit = []

for date in pollDf['Start Date']:
    if date[0:7] == '2016-06':
        xlimit.append(row_in)
        row_in +=1
    else:
        row_in += 1
        
print(min(xlimit)) 
print(max(xlimit)) 


# In[32]:

fig = pollDf.plot('Start Date','Difference',figsize=(12,4),marker='o',linestyle='-',color='purple',xlim=(134,158))

#debates
plt.axvline(x=134+2, linewidth=4, color='grey')
plt.axvline(x=134+10, linewidth=4, color='grey')
plt.axvline(x=134+21, linewidth=4, color='grey')


# In[37]:

#Donors data
#The questions we will be trying to answer while looking at this Data Set is:

#1.) How much was donated and what was the average donation?
#2.) How did the donations differ between candidates?
#3.) How did the donations differ between Democrats and Republicans?
#4.) What were the demographics of the donors?
#5.) Is there a pattern to donation amounts?
#  http://classic.fec.gov/disclosurep/PDownload.do


# In[35]:

donor_df = pd.read_csv('P00000001-ALL.csv')
donor_df.info()


# In[36]:

donor_df.head()


# In[39]:

donor_df['contbr_occupation'].value_counts()


# In[40]:

don_mean = donor_df['contbr_occupation'].mean()

don_std = donor_df['contbr_occupation'].std()
#ecat type
print ('The average donation was %.2f with a std of %.2f' %(don_mean,don_std))


# In[41]:

top_donor = donor_df['contbr_occupation'].copy()

top_donor.sort()
top_donor


# In[42]:

top_donor = top_donor[top_donor >0]

top_donor.sort()

top_donor.value_counts().head(10)


# In[43]:

com_don = top_donor[top_donor < 2500]
com_don.hist(bins=100)


# In[45]:

candidates = donor_df.cand_id.unique()

candidates


# In[46]:

party_map = {'Rubio, Marco': 'Republican',
           'Santorum, Richard J.': 'Republican',
           'Perry, James R.': 'Republican',
           'Carson, Benjamin S.': 'Republican',
           'Cruz, Rafael Edward': 'Republican',
           'Paul, Rand': 'Republican',
           'Clinton, Hillary Rodham': 'Democrat',
           'Sanders, Bernard': 'Democrat',
           'Fiorina, Carly': 'Republican',
           'Huckabee, Mike': 'Republican',
           'Pataki, George E.': 'Republican',
           "O'Malley, Martin Joseph": 'Democrat',
           'Graham, Lindsey O.': 'Republican',
             'Bush, Jeb': 'Republican',
             'Trump, Donald J.': 'Republican',
             'Jindal, Bobby': 'Republican',
                      
           'Christie, Christopher J.': 'Republican',
             'Walker, Scott': 'Republican',
             'Stein, Jill': 'Green',
             'Webb, James Henry Jr.': 'Democrat',
            
                      
           'Kasich, John R.': 'Republican',
             'Gilmore, James S III': 'Republican',
             'Lessig, Lawrence': 'Democrat',
             'Johnson, Gary': 'Libertarian',
             'McMullin, Evan': 'Independent'}


donor_df['Party'] = donor_df.cand_nm.map(party_map)


# In[48]:

# Clear refunds
donor_df = donor_df[donor_df.contbr_occupation >0]

# Preview DataFrame
donor_df.head()


# In[51]:

donor_df.groupby('cand_id')['contbr_occupation'].count()


# In[52]:

# Groupby candidate and then displayt the total amount donated
donor_df.groupby('cand_id')['contbr_occupation'].sum()


# In[53]:

# Start by setting the groupby as an object
cand_amount = donor_df.groupby('cand_id')['contbr_occupation'].sum()

# Our index
i = 0

for don in cand_amount:
    print(" The candidate %s raised %.0f dollars " %(cand_amount.index[i],don))
    print ('\n')
    i += 1


# In[54]:

# PLot out total donation amounts
cand_amount.plot(kind='bar')


# In[59]:

donor_df.groupby('Party')['contbr_occupation'].sum().plot(kind='bar')


# In[63]:

occupation_df = donor_df.pivot_table('contbr_occupation',
                                index='contbr_employer',
                                columns='Party', aggfunc='sum')



# In[64]:

occupation_df.shape


# In[65]:

occupation_df.head(20)


# In[66]:

occupation_df = occupation_df[occupation_df.sum(1) > 1000000]
occupation_df.shape

occupation_df.plot(kind='bar')


# In[67]:


occupation_df.plot(kind='barh',figsize=(10,12),cmap='seismic')


# In[68]:

occupation_df.drop(['INFORMATION REQUESTED PER BEST EFFORTS','INFORMATION REQUESTED'],axis=0,inplace=True)


# In[69]:

# Set new ceo row as sum of the current two
occupation_df.loc['CEO'] = occupation_df.loc['CEO'] + occupation_df.loc['C.E.O.']
# Drop CEO
occupation_df.drop('C.E.O.',inplace=True)


# In[70]:

occupation_df.plot(kind='barh',figsize=(10,12),cmap='seismic')


# In[ ]:



