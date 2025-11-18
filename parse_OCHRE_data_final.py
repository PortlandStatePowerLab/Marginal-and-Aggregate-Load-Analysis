# -*- coding: utf-8 -*-
"""
Created on Wed Sep 24 14:46:47 2025

@author: Joe_admin
"""


import pandas as pd
from datetime import datetime

# Converts the datetime information in the HEMS data to usable datetimes
def convert_custom_datetime(series):
    return series.apply(lambda x: datetime.strptime(x, "%d/%m/%Y %H:%M"))


############################################################################
#                           Enter inputs here                              #
############################################################################

# enter in the input and output file names.   
input_file_name  = "C:/Users/Joe_admin/Documents/IEEE_2026_paper/Inputs/hpwh_baseline_all.csv"
output_file_name  = "C:/Users/Joe_admin/Documents/IEEE_2026_paper/Ready_data/hpwh_baseline_ready_data.csv"

############################################################################
#                             Program Start                                #
############################################################################

# read data 
df = pd.read_csv(input_file_name)

# remove any NAN values that will mess up the datetime conversion. 
df = df.dropna(axis=0)

# convert time column to a usable datetime fomat
df['time'] = convert_custom_datetime(df['Time'])

# Create column that contains hour and minute data
df['hr_min'] = df['time'].dt.strftime('%H:%M')

# drop unwanted columns
df = df.drop(['Time', 'Total Electric Power (kW)', 'Total Electric Energy (kWh)', 'Water Heating COP (-)', 
              'Water Heating Deadband Upper Limit (C)', 'Water Heating Deadband Lower Limit (C)', 'Water Heating Heat Pump COP (-)', 
              'Water Heating Control Temperature (C)', 'Hot Water Outlet Temperature (C)', 'Temperature - Indoor (C)', 'time'], axis=1)


# pivot the table
df_pivot = df.pivot_table(index = 'Home', columns = 'hr_min', values = 'Water Heating Electric Power (kW)')

# write data to csv
df_pivot.to_csv(output_file_name, index=True)
