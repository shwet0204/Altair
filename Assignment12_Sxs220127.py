#!/usr/bin/env python
# coding: utf-8

# In[3]:


conda install -c conda-forge altair vega_datasets


# In[4]:


import pandas as pd
import numpy as np
import altair as alt
from vega_datasets import data


# In[6]:


df=pd.read_csv(r'/Users/shwetshah/Desktop/DatViz/Assignment 12/JHU.csv')


# In[7]:


df.head()


# In[9]:


df=df[['Countyname','ST_Name','ST_Abbr','ST_ID','FIPS','FatalityRa','Confirmed','Deaths','TotalPop']]



# In[10]:


df=df.head(3250)


# In[11]:


df


# In[13]:


alt.Chart(df).transform_aggregate(
    count= 'sum(Confirmed):Q',
    groupby=['ST_Name']
).transform_window(
    rank='rank(count)',
    sort=[alt.SortField('count',order='descending')]
).transform_filter(
    alt.datum.rank < 11
).mark_bar().encode(
    y=alt.Y('ST_Name:N', sort= '-x'),
    x='count:Q'
)


# In[14]:


input_dropdown = alt.binding_select(options=['New York','California','Florida','Texas','New Jersey'])
selection = alt.selection_single(fields=['ST_Name'], bind=input_dropdown, name='State')
color = alt.condition(selection,
                     alt.Color('ST_Name:N', legend=None),
                     alt.value('lightgray'))
    
alt.Chart(df).mark_point().encode(
    x=alt.X('Confirmed:Q', scale= alt.Scale(domain=[0,50000])),
    y=alt.Y('Deaths:Q', scale=alt.Scale(domain=[0,4000])),
    color=color,
    tooltip= ['Countyname:N','ST_Name']
).add_selection(
    selection
).properties(
width=800,
height=500
).interactive()


# In[15]:


counties = alt.topo_feature(data.us_10m.url, 'counties')

alt.Chart(counties).mark_geoshape().encode(
color=alt.Color('FatalityRa:Q',scale=alt.Scale(domain=[1,10], scheme='bluepurple')),
tooltip=['FatalityRa:Q']
).transform_lookup(
lookup='id',
from_=alt.LookupData(df, 'FIPS', ['FatalityRa'])
).project(
type='albersUsa'
).properties(
width=500,
height=300
)


# In[ ]:




