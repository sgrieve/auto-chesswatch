import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from datetime import datetime


def offset_correction(df, id):
    '''
    The Chesham data needs an offset of -27cm applied to all values,
    and any negative values should be fixed at 0.
    '''

    if id == '2852TH-level-stage-i-15_min-mASD':
        df['measurement'] = df['measurement'] - 0.27
        df['measurement'] = df['measurement'].clip(lower=0.0)

    return df

dateparse = lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S')

id = sys.argv[1]
title = sys.argv[2]

flow = pd.read_csv('data/{}.csv'.format(id), parse_dates=['date'], date_parser=dateparse)

# we only want data for the last 12 months
date_range = pd.to_datetime('now') - pd.DateOffset(months=12)
flow = flow.query('date > @date_range')

flow = offset_correction(flow, id)

flow_series = pd.Series(data=flow['measurement'].values, index=flow['date'])

daily_flow = flow_series.groupby(flow_series.index.date).mean()
flow_days = sorted(list(set(flow_series.index.date)))

ax = plt.gca()
fig = plt.gcf()

fig.set_size_inches(6.4, 2.4)

ax.spines['bottom'].set_visible(True)
ax.set_ylabel('River level (mASD)')

ax.plot(flow_days, daily_flow.values, color='tab:blue')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.spines['left'].set_visible(True)

# Creating a fake axis so we can have the title on the right
ax2 = ax.twinx()
ax2.set_ylabel(title, fontsize=14)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.set_yticks([])

ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
plt.tight_layout()

plt.savefig('plots/{}.png'.format(id), dpi=100)
