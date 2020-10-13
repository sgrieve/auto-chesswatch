import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from datetime import datetime

dateparse = lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S')

rain = pd.read_csv('data/278744TP-rainfall-tipping_bucket_raingauge-t-15_min-mm.csv',
                    parse_dates=['date'], date_parser=dateparse)

# we only want data for the last 12 months
date_range = pd.to_datetime('now') - pd.DateOffset(months=1)
rain = rain.query('date > @date_range')

rain_series = pd.Series(data=rain['measurement'].values, index=rain['date'])

daily_totals = rain_series.groupby(pd.Grouper(freq='D')).sum()

fig, ax = plt.subplots()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d\n%b'))
ax.bar(daily_totals.index, daily_totals.values, width=1,
       color=sns.color_palette("Blues_d")[3], edgecolor='k')


plt.xlabel('')
plt.ylabel('Total Rainfall (mm)')
plt.tight_layout()
plt.savefig('plots/rainfall-month.png')
