import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# load the dataset
df = pd.read_csv('result/1_TGS.csv')

# set the background style of the plot
#sns.set_style('whitegrid')
# Set the global font size scale (e.g., to 1.5 times the default)
sns.set_theme(font_scale=3)
min_x = 10497
max_x = 15974
ax = sns.kdeplot(df['TGS'],clip=(10497,15974))
max_value = np.max(df['TGS'])
# ax = sns.kdeplot(df['TGS'])

x_data = ax.lines[0].get_xdata()
y_data = ax.lines[0].get_ydata()

# Interpolate the y-value for the specific x-value (mean_value)
# This works because the KDE curve is a continuous function, and we can estimate the density at any point
highlight_y = np.interp(max_value, x_data, y_data)
min_y = np.interp(min_x, x_data, y_data)
max_y = np.interp(max_x, x_data, y_data)

plt.plot(min_x, min_y, 'go', markersize=20, label="Minimum")
plt.annotate(f"Minimum: {min_x}", (min_x, min_y), color='green' ,textcoords="offset points", xytext=(0,20), ha='center')

plt.plot(max_x, max_y, 'o',color='orange', markersize=20, label="Maximum")
plt.annotate(f"Maximum: {max_x}", (max_x, max_y), color='orange' ,textcoords="offset points", xytext=(0,20), ha='center')

plt.plot(max_value, highlight_y, 'ro', markersize=20, label="Existing")
plt.annotate(f"Existing: {max_value}", (max_value, highlight_y), color='red' ,textcoords="offset points", xytext=(0,20), ha='center')

# 4. Highlight the specific point using plt.scatter()
#plt.scatter(x=max_value, y=highlight_y, color='red', zorder=10, label=f'Max ({max_value:.2f})')

plt.show()
