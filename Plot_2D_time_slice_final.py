# -*- coding: utf-8 -*-
"""
Created on Wed Sep 24 08:57:35 2025

@author: Joe_admin
"""

import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

start_time = time.time()

############################################################################
#                           Enter inputs here                              #
############################################################################

total_power = True

if total_power:
    # enter in the input and output file names.   
    ninety_fifth_file_name  = "C:/Users/Joe_admin/Documents/IEEE_2026_paper/ML_files/hpwh_975th_300_03.csv"
    mean_file_name          = "C:/Users/Joe_admin/Documents/IEEE_2026_paper/ML_files/hpwh_mean_300_03.csv"
    fifth_file_name         = "C:/Users/Joe_admin/Documents/IEEE_2026_paper/ML_files/hpwh_025th_300_03.csv"

else:
    ninety_fifth_file_name  = "C:/Users/Joe_admin/Documents/IEEE_2026_paper/ML_files/hpwh_975th_300_01.csv"
    mean_file_name          = "C:/Users/Joe_admin/Documents/IEEE_2026_paper/ML_files/hpwh_Mean_300_01.csv"
    fifth_file_name         = "C:/Users/Joe_admin/Documents/IEEE_2026_paper/ML_files/hpwh_025th_300_01.csv"


time_select = '21:45'
############################################################################
#                             Program Start                                #
############################################################################

# read data 
ninety_fifth_df = pd.read_csv(ninety_fifth_file_name)
mean_df         = pd.read_csv(mean_file_name)
fifth_df        = pd.read_csv(fifth_file_name)


# remove the columns we dont need
ninety_fifth_df = ninety_fifth_df.drop(['Unnamed: 0'], axis=1)
mean_df         = mean_df.drop(['Unnamed: 0'], axis=1)
fifth_df        = fifth_df.drop(['Unnamed: 0'], axis=1)


# cut off the early data
ninety_fifth_df = ninety_fifth_df.tail(499)
mean_df         = mean_df.tail(499)
fifth_df        = fifth_df.tail(499)


ninety_fifth_data = ninety_fifth_df[time_select]
mean_data         = mean_df[time_select]
fifth_data        = fifth_df[time_select]

# Create the figure and plot the initial data
A = 16
fig = plt.figure(figsize=(9, 7))
ax1 = fig.add_subplot()

# plot each data in grey
X = mean_data.index.to_numpy()

# 97.5th percentile
ax1.plot(X, ninety_fifth_data.values, color='gray', alpha=1, linewidth=3)
ax1.fill_between(X, ninety_fifth_data.values, mean_data.values, color='pink', alpha=0.3)

# mean
ax1.plot(X, mean_data.values, color='blue', alpha=1, linewidth=3)

# 2.5th percentile
ax1.plot(X, fifth_data.values, color='gray', alpha=1, linewidth=3)
ax1.fill_between(X, fifth_data.values, mean_data.values, color='pink', alpha=0.3)

# plot the numpy polynomial model best fit for the mean
z = np.polyfit(X, mean_data.values, 1) # R values still > 0.99 when the number of units is 1000.
f = np.poly1d(z)
print(f)
coefficient_of_dermination = r2_score(mean_data.values, f(X))
print(coefficient_of_dermination)

# ax1.plot(X, f(X), color='green', linewidth=2)
ax1.plot(X, f(X), label='ax + b fit', color='red', linewidth=1.5)

# annotate the best fit line
arc = 0.18
ax1.annotate(r'$P_{mean} = 0.1507N + 0.1501$', xy=(280, 42), xytext=(110, 65), fontsize=A, color='red', 
             bbox=dict(boxstyle='round,pad=0.2', fc='grey', alpha=0.3),
             arrowprops=dict(arrowstyle="->",color='k' ,linewidth=2.5,connectionstyle=f"arc3,rad={arc}"))  
  
ax1.text(110, 59, r'$R^2 = 0.999$', fontsize=A, color='red',
         bbox=dict(boxstyle='round,pad=0.2', fc='grey', alpha=0.3))

# Create a secondary y-axis that shares the same x-axis
ax2 = ax1.twinx()

# plot the uncertainty as  proportion of the mean
CI_width = ( ninety_fifth_df['18:00'] - fifth_df['18:00'] ) / mean_df['18:00'] * 100

ax2.plot(X, CI_width, color='green', linewidth=2)

ax2.axhline(y=20, color='g', linestyle='--', alpha=0.5)
ax1.axvline(x=430, color='g', linestyle='--', alpha=0.5)
ax2.plot(430, 20, 'o', color='k')
ax2.text(351, 14, r'$N \approx 430$', fontsize=A, color='k',
         bbox=dict(boxstyle='round,pad=0.2', fc='grey', alpha=0.3))

# Set y scale to exponential if needed
'''
ax1.set_yscale('log', base=10) # original log scale
ax2.set_yscale('log', base=10) # original log scale
ax1.set_xscale('log', base=10) # original log scale
'''

# ax.set(ylim=(.255,0.262))
ax1.grid(True, alpha=0.4)
ax1.set_ylabel('Power [kW]', fontsize=A)
ax2.set_ylabel('95% CI / Mean [%]', fontsize=A, color='green')
ax2.set_ylim(-4.5, 100)
ax1.set_xlabel('Units [N]', fontsize=A)
ax1.tick_params(axis='x', labelsize=A)
ax1.tick_params(axis='y', labelsize=A)
ax2.tick_params(axis='y', labelsize=A, colors='g', grid_color='g')
plt.show()

# print out the time it took to run the program
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")
execution_min = execution_time/60
print(f"Execution time: {execution_min} minutes")
