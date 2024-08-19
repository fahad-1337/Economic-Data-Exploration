# -*- coding: utf-8 -*-
"""economic data analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Xcv1kmDU_LTkhIf0A-II7S5-bvuAUbIx
"""

!pip install fredapi
pd.set_option('display.min_rows', 8)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px


from fredapi import Fred

fred_key = '83a864c605c9874a80f7c39ccda9d061'

fred = Fred(api_key=fred_key)

fred

fredsandp = fred.search('S&P', order_by='popularity')

fredsandp.head()

sp500 = fred.get_series(series_id='SP500')

sp500

sp500.plot(figsize=(10,5), title = 'S&P 500')

fred.search('umemployement ')

un_emp = fred.search('unemployment')

unrate = fred.get_series(series_id = 'UNRATE')

unrate.plot()

unemploy_df = fred.search('unemployement rate state', filter=('frequency','Monthly'))

unemploy_df = unemploy_df.query('seasonal_adjustment == "Seasonally Adjusted" and units == "Percent"')

unemploy_df = unemploy_df.loc[unemploy_df['title'].str.contains('Unemployment Rate in')]

unemploy_df = unemploy_df.drop('CNEWUR', axis=0)

pd.set_option('display.max_rows', 6)
unemploy_df

unemploy_df.shape

ids_to_drop = ['CWSTUR', 'CNERUR', 'CSOUUR', 'CMWRUR', 'LASMT391746000000003', 'LASMT261982000000003' ,'PRUR']


unemploy_df = unemploy_df.drop(ids_to_drop)

unemploy_df

all_results = []

for myid in unemploy_df.index:
 results = fred.get_series(myid)
 results = results.to_frame(myid)
 all_results.append(results)

unemp_results = pd.concat(all_results, axis=1)

unemp_results

state_name = unemploy_df['title'].str.replace('Unemployment Rate in', ' ').to_dict()

unemp_results.columns = [state_name[c] for c in unemp_results.columns]

unemp_results

#Unemployment Rate Plot

px.line(unemp_results, title = 'State Wise Unemployement Rate')

#2020 In Depth Analysis

bar_plot = unemp_results.loc[unemp_results.index == '2020-05-01'].T.sort_values('2020-05-01').plot(kind='barh', figsize=(12,10),title = 'Unemployment Rate by State, May 2020')

bar_plot.legend().remove()
bar_plot.set_xlabel('% Unemployed')
plt.show

part_df = fred.search('participation rate state', filter=('frequency','Monthly'))
part_df = part_df.query('seasonal_adjustment == "Seasonally Adjusted" and units == "Percent"')
part_df = part_df.loc[part_df['title'].str.contains('Participation Rate for')]

part_df

part_results = []

for myid in part_df.index:
 results = fred.get_series(myid)
 results = results.to_frame(myid)
 part_results.append(results)

part_rate_results = pd.concat(part_results, axis=1)

part_rate_results

part_state_name = part_df['title'].str.replace('Labor Force Participation Rate for', ' ').to_dict()

part_rate_results.columns = [part_state_name[c] for c in part_rate_results.columns]

part_rate_results

part_rate_results.columns = part_rate_results.columns.str.strip()

print(part_rate_results.columns)

unemp_results.columns = unemp_results.columns.str.strip()

print(unemp_results.columns)

#Fixing column name
unemp_results = unemp_results.rename(columns={'the District of Columbia':'District Of Columbia'})

unemp_results.columns

fig, axs  = plt.subplots(10, 5, figsize=(30,30), sharex=True)
axs = axs.flatten()

i=0
for state in unemp_results.columns:

  if state=='District Of Columbia':
    continue
  ax2 = axs[i].twinx()
  unemp_results.query('index >= 2020 and index < 2022')[state].plot(ax=axs[i], label='unemployment' )
  part_rate_results.query('index >= 2020 and index < 2022')[state].plot(ax=ax2, label='participation', color='red' )
  ax2.grid(False)
  axs[i].set_title(state, fontsize=20)
  i=i+1

plt.tight_layout
plt.show()