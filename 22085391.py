# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 12:53:23 2024

@author: Nisarg
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import seaborn as sns
import seaborn.objects as so
from matplotlib.gridspec import GridSpec

def read_data():
    df = pd.read_csv("Electric_Vehicle_Population_Data.csv")
    make_list = ["AUDI","BMW","CHEVROLET","CHRYSLER","FORD","HYUNDAI","JEEP","KIA","MERCEDES-BENZ","NISSAN","PORSCHE","TESLA","TOYOTA","VOLKSWAGEN","VOLVO"]
    df = df.loc[(df['Model Year']>=2013) & (df['Model Year']<=2023) & (df['Make'].isin(make_list)) ]
    
    return df;
    
def plot_ev_producers(df, grid):
    plt.subplot(grid[0 , 0])
    
    df_grouped  = df.groupby(["Make","Electric Vehicle Type"]).size().reset_index(name='Count')
    df_grouped_make  = df.groupby(["Make"]).size().reset_index(name='Count')
    make_filter = df_grouped_make[df_grouped_make["Count"]>1000]["Make"]
    
    df_grouped_filter = df_grouped[df_grouped["Make"].isin(make_filter)]
    df_grouped_filter["Count"] = (df_grouped_filter["Count"]/1000).round(2)

   

    # Pivot the DataFrame to create a stacked bar chart
    pivot_df = df_grouped_filter.pivot_table(index='Make', columns='Electric Vehicle Type').fillna(0)
    
    pivot_df[("Count","Total")] = pivot_df.iloc[:,0] + pivot_df.iloc[:,1]
    # Initialize the matplotlib figure
    #fig = plt.figure(dpi=300)
    #ax = fig.add_subplot()
 
 
    # Plot the total crashes
    #sns.set_theme()

    ax = sns.barplot(x="Make", y="Count", data=pivot_df.loc[:,("Count","Total")].reset_index(name='Count'),
            label="Plug-in Hybrid Electric Vehicle (PHEV)", color="b")
    
    #ax.bar_label(ax.containers[0], labels=pivot_df.loc[:,("Count","Total")].values.round(2))

    # Plot the crashes where alcohol was involved
    sns.set_color_codes("muted")
    sns.barplot(x="Make", y="Count", data=pivot_df[("Count","Battery Electric Vehicle (BEV)")].reset_index(name='Count'),
            label="Battery Electric Vehicle (BEV)", color="b")

    # Add a legend and informative axis label
    ax.legend(ncol=1, loc="upper left", frameon=True)
    ax.set(ylabel="NUMBER OF VEHICLES(K)",
       xlabel="MAKE")
    plt.title("The number of ELECTRIC VEHICLE of Respective Producers")
    plt.xticks(rotation=90)
   
  
def plot_compare_year_of_make(df, grid):
     plt.subplot(grid[0 , 2])
     df_grouped  = df.groupby(["Model Year","Electric Vehicle Type"]).size().reset_index(name='Count')
     df_bev = df_grouped.loc[df_grouped["Electric Vehicle Type"]=="Battery Electric Vehicle (BEV)"]
     df_phev = df_grouped.loc[df_grouped["Electric Vehicle Type"]=="Plug-in Hybrid Electric Vehicle (PHEV)"]

     #plt.figure(figsize=(10, 6),dpi=300)
     #print(df_grouped)
     sns.lineplot(data=df_bev,y="Count",x="Model Year", label="Battery Electric Vehicle (BEV)")
     sns.lineplot(data=df_phev,y="Count",x="Model Year", label="Plug-in Hybrid Electric Vehicle (PHEV)")
     #plt.subplot(1, 2, 1)
     #plt.pie(df_bev['Count'], labels=df_bev['Model Year'], autopct='%1.1f%%', pctdistance=0.8)
     #plt.title('Battery Electric Vehicle (BEV)')
     
     #plt.subplot(grid[1 , 1])
     #plt.pie(df_phev['Count'], labels=df_phev['Model Year'], autopct='%1.1f%%', pctdistance=0.8)
     #plt.title('Plug-in Hybrid Electric Vehicle (PHEV)')
     #plt.suptitle('Comparson of BEV vs PHEV onYear of make', fontsize=15)

def plot_ev_range(df, grid):
     plt.subplot(grid[0 , 1])
     df_make_range =  df[["Make","Electric Range"]]
     df_grouped  = df_make_range.groupby(["Make"]).agg({'Electric Range':'max'})
     df_grouped["Make"] = df_grouped.index
     #print(df_grouped)
     df_grouped = df_grouped.sort_values(by=['Electric Range'],ascending=False)
     #sns.set_theme()
     #sns.set_color_codes("pastel")
     ax = sns.barplot(x="Electric Range", y="Make", data=df_grouped, color="b")
     ax.bar_label(ax.containers[0], labels=df_grouped['Electric Range'])
     plt.title("The maximum Electric Range of Top 15 Producers.")
     
def plot_country_ev(df, grid):
    plt.subplot(grid[1 , 2])
    df_grouped = df.groupby(["City"]).size().reset_index(name='Count')
    df_grouped = df_grouped.sort_values(by=['Count'],ascending=False)[0:10]

    
  
    plt.pie(df_grouped['Count'], labels=df_grouped['City'], autopct='%1.1f%%', pctdistance=0.58, startangle=60)
    my_circle=plt.Circle( (0,0), 0.75, color='white')
    p=plt.gcf()
    p.gca().add_artist(my_circle)
    
    plt.title('Location of city of EV respectively',  y=0.92)
   
    
def plot_text(grid):
    # Add a subplot for key insights
    plt.subplot(grid[1 , 1])
    text = "Key Insights:\n\n" \
           "1. Lorazepam, sold under the brand name\n" \
           "2. Lorazepam, sold under the brand name.\n" \
           "3. Lorazepam, sold under the brand name.\n" \
           "4. Lorazepam, sold under the brand name \n" \
           "lorazepam, sold under the brand name."
    plt.text(0.5 , 0.5 , text , ha='center' , va='center' , fontsize=12 ,
             color='gray' , fontstyle='italic' , fontweight='bold')
    plt.axis('off')

    # Add student information
    plt.subplot(grid[1 , 0])
    text = "Student Name: Nisarg Bhikhubhai Kanojia\n" \
           "Student ID: 22085391"
    plt.text(0.5 , 0.5 , text , ha='center' , va='center' , fontsize=12 , color='gray' ,
             fontstyle='italic' , fontweight='bold')
    plt.axis('off')

    # Main title for the entire dashboard
    fig.suptitle('USA Electric Vehicle Dashboard' , fontsize=25 , fontweight='bold')

    
###### Main funciton ######

df = read_data()

# Create a 2x3 grid
sns.set_color_codes("pastel")
sns.despine(left=True, bottom=True)
fig = plt.figure(figsize=(18 , 10),dpi=300)
grid = GridSpec(2 , 3 , width_ratios=[1 , 1 , 1] , height_ratios=[1 , 1])


plot_ev_producers(df, grid)
plot_compare_year_of_make(df, grid)
plot_ev_range(df, grid)
plot_country_ev(df, grid)
plot_text(grid)


plt.show()