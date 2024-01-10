
"""
GitHub link : https://github.com/nbkanojia/UH-DHV-Assigment1
"""
import pandas as pd
import matplotlib.pyplot as plt

import seaborn as sns
import matplotlib.colors as mcolors
from matplotlib.gridspec import GridSpec


def read_data():
    """ function to read csv """
    df = pd.read_csv("Electric_Vehicle_Population_Data.csv")
    make_list = ["AUDI", "BMW", "CHEVROLET", "CHRYSLER", "FORD",
                 "HYUNDAI", "JEEP",
                 "KIA", "MERCEDES-BENZ", "NISSAN", "PORSCHE", "TESLA",
                 "TOYOTA", "VOLKSWAGEN", "VOLVO"]
    df = df.loc[(df['Model Year'] >= 2013) & (df['Model Year'] <= 2023) &
                (df['Make'].isin(make_list))]

    return df


def plot_ev_producers(df, grid):
    """ create the ev bar chart to compare production
    between top 15 compqnies """

    fig = plt.subplot(grid[0, 0])

    df_grouped = df.groupby(["Make", "Electric Vehicle Type"]).size()\
        .reset_index(name='Count')
    df_grouped_make = df.groupby(["Make"]).size().reset_index(name='Count')
    make_filter = df_grouped_make[df_grouped_make["Count"] > 1000]["Make"]

    df_grouped_filter = df_grouped[df_grouped["Make"].isin(make_filter)]
    df_grouped_filter["Count"] = (df_grouped_filter["Count"]/1000).round(2)

    # Pivot the DataFrame to create a stacked bar chart
    pivot_df = df_grouped_filter.pivot_table(index='Make',
                                             columns='Electric Vehicle Type')\
        .fillna(0)

    pivot_df[("Count", "Total")] = pivot_df.iloc[:, 0] + pivot_df.iloc[:, 1]
    # Initialize the matplotlib figure
    # fig = plt.figure(dpi=300)
    # ax = fig.add_subplot()

    # Plot the total crashes
    sns.set_theme(palette="pastel")
    ax = sns.barplot(x="Make", y="Count",
                     data=pivot_df.loc[:, ("Count", "Total")].reset_index(
                         name='Count'),
                     label="Plug-in Hybrid Electric Vehicle \n(PHEV)",
                     color="b")

    ax.bar_label(ax.containers[0],
                 labels=pivot_df.loc[:, ("Count", "Total")].values.round(1),
                 fontsize=12, rotation=0)

    ax.set_ylim(0, 100)
    # Plot the crashes where alcohol was involved
    sns.set_color_codes("muted")
    ax1 = sns.barplot(x="Make", y="Count",
                      data=pivot_df[(
                          "Count", "Battery Electric Vehicle (BEV)")]
                      .reset_index(name='Count'),
                      label="Battery Electric Vehicle \n(BEV)", color="b")
    ax1.set_ylim(0, 85)

    # Add a legend and informative axis label
    ax.legend(ncol=1, loc="upper left", frameon=True)
    ax.set(ylabel="Number Of Vehicles(K)",
           xlabel="MAKE")
    fig.xaxis.set_label_coords(0.4, -0.4)

    plt.title("The total number of EV sold by top 15 Companies")
    plt.xticks(rotation=90)
    sns.set_theme(palette="deep")


def plot_ev_range(df, grid):
    """ create EV horizontal bar char to compare the battery range """

    fig = plt.subplot(grid[0, 1])

    # plt.subplots_adjust(left=0.5,right=1)
    df_make_range = df[["Make", "Electric Range"]]
    df_grouped = df_make_range.groupby(["Make"])\
        .agg({'Electric Range': 'max'})
    df_grouped["Make"] = df_grouped.index
    # print(df_grouped)
    df_grouped = df_grouped.sort_values(by=['Electric Range'],
                                        ascending=False)
    # sns.set_theme()
    # sns.set_color_codes("pastel")
    ax = sns.barplot(x="Electric Range", y="Make", data=df_grouped, color="b")
    ax.bar_label(ax.containers[0], labels=df_grouped['Electric Range'],
                 fontsize=12)
    ax.set_xlim(0, 370)
    plt.xlabel('Electric Range (Miles)')

    fig.yaxis.set_label_coords(-0.32, 0.65)
    plt.title("The maximum Electric Range of top 15 producers")


def plot_compare_year_of_make(df, grid):
    """ compare BEV vs PHEV production over the years """

    plt.subplot(grid[0, 2])
    df_grouped = df.groupby(["Model Year", "Electric Vehicle Type"]).size()\
        .reset_index(name='Count')
    df_bev = df_grouped\
        .loc[df_grouped["Electric Vehicle Type"] ==
             "Battery Electric Vehicle (BEV)"]
    df_phev = df_grouped.loc[df_grouped["Electric Vehicle Type"] ==
                             "Plug-in Hybrid Electric Vehicle (PHEV)"]

    # plt.figure(figsize=(10, 6),dpi=300)
    # print(df_grouped)
    sns.lineplot(data=df_bev, y="Count", x="Model Year",
                 label="Battery Electric Vehicle (BEV)")
    sns.lineplot(data=df_phev, y="Count", x="Model Year",
                 label="Plug-in Hybrid Electric Vehicle (PHEV)")

    plt.xlabel('Year')
    plt.ylabel('Number of EV')
    plt.title('Comparson of BEV vs PHEV on year of make')


def plot_city_ev(df, grid):
    """ compare the usa top 10 cities with heightest EV cars """
    plt.subplot(grid[1, 2])
    df_grouped = df.groupby(["City"]).size().reset_index(name='Count')
    df_grouped = df_grouped.sort_values(by=['Count'], ascending=False)[0:10]

    plt.pie(df_grouped['Count'], labels=df_grouped['City'], autopct='%1.1f%%',
            pctdistance=0.60, startangle=60, radius=1.1,
            textprops={'fontsize': 11})
    my_circle = plt.Circle((0, 0), 0.79, color='#f6f6f6')
    p = plt.gcf()
    p.gca().add_artist(my_circle)

    plt.title('Cities with heights EV, among the top 10 cities',
              y=0.94)


def plot_text(grid):
    """ print text on dashboard """
    # Add a subplot for key insights
    plt.subplot(grid[1, 1])
    text = "Key Insights:\n\n" \
           "1. Tesla is by far the most popular EV brand globally, with 73.4K"\
        + " sales all time. \nTesla has the same number of EV sales as the "\
        + "next 14 largest brands combined\n" \
           "\n2. Tesla also has the highest range of these top 15 "\
        + "producers.\n" \
           "\n3. BEV sales have grown significantly in the past few years,"\
        + "  \nwith sales in 2022 being 111.11% higher than in 2014\n" \
           + "\n4. Seattle has by far the most EVs, with 25.4% more than the "\
        + "next highest city. \nThis may be due to the EV " \
        + "tax incentives Washington state \nprovides to its residents\n"

    plt.text(-0.3, 0.55, text, ha='left', va='center', fontsize=12,
             color='gray', fontstyle='italic', fontweight='bold')
    plt.axis('off')

    # Add student information
    plt.subplot(grid[1, 0])
    text = "Student Name: Nisarg Bhikhubhai Kanojia\n" \
           "Student ID: 22085391"
    plt.text(0.5, 0.5, text, ha='center', va='center', fontsize=12,
             color='gray', fontstyle='italic', fontweight='bold')
    plt.axis('off')

    # Main title for the entire dashboard
    fig.suptitle('USA Electric Vehicle(EV) Dashboard',
                 fontsize=25, fontweight='bold')


###### Main funciton ######

# read data
df = read_data()

# Create a 2x3 grid
sns.set_theme()

# set figure
fig = plt.figure(figsize=(19, 10), dpi=300)
fig.patch.set_facecolor('#f6f6f6')
# configure grid
grid = GridSpec(2, 3, width_ratios=[1, 1, 1], height_ratios=[1, 1], wspace=0.4)

# plot graphs
plot_ev_producers(df, grid)
plot_compare_year_of_make(df, grid)
plot_ev_range(df, grid)
plot_city_ev(df, grid)
plot_text(grid)
extent = fig.get_window_extent().transformed(fig.dpi_scale_trans.inverted())

# save or show the file
plt.savefig("22085391.png", dpi=300, bbox_inches='tight')
#plt.show()
