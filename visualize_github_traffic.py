import pandas as pd
import seaborn as sns
from glob import glob
import matplotlib.pyplot as plt
sns.set(style="darkgrid")

# Specify username
username = 'miykael'

# Collect all repo names
fdata = glob('results/*.tsv')

# Store all trafic information in one dataframe
data = []
header = []
for f in fdata:
    data.append(pd.read_csv(f, sep='\t', index_col=0)['View_count'])
    header.append(f[21:-4])

df = pd.concat(data, axis=1, keys=header)

# Eliminate entries with too few elements
too_small = df.sum(axis=0) >= 250
df = df[df.columns[too_small]]

# Plot overview figures
nTraffic = df.shape[1]
fig, ax = plt.subplots(nrows=nTraffic, figsize=(16, nTraffic * 3))

for i in range(nTraffic):
    df_name = df.columns[i]
    df[df_name].plot(ax=ax[i], legend=df_name)

fig.tight_layout()
fig.savefig('traffic_overview.svg', dpi=150)
