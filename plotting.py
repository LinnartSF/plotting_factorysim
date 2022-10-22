
"""

This is a module wrapping pandas and matplotlib.pyplot

This module can be used to make use of predefined plots, that receive pandas dataframes in predefined structures.

The idea is to setup a database into which analysis results from e.g. a discrete-event simulation model are written; for this I wrote another module that is available in another repository. 
Using that module would ensure a standardized way of registring simulation results, and in that case standardized plots as in this module could be used.

Especially when working with simulation tools that do not have that flexible statistics or visualizations, an approach like this can make good sense.

"""


__author__ = "Linnart Felkl"
__email__ = "linnartsf@gmail.com"

from matplotlib import pyplot as plt
plt.style.use("fivethirtyeight")
import pandas

def warning(msg: str) -> None:
    """ helper function that prints a warning into console; used when invalid input is forwarded to one of the functions in the module """
    print(f"WARING: {msg}")

def set_plotstyle(style: str) -> None:
    """ sets matplotlib plotstyle """
    plt.style.use(style)

def set_fontsizes(smallsize: float, mediumsize: float, largesize: float):
    plt.rc('font', size = smallsize)          # controls default text sizes
    plt.rc('axes', titlesize = smallsize)     # fontsize of the axes title
    plt.rc('axes', labelsize = mediumsize)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize = smallsize)    # fontsize of the tick labels
    plt.rc('ytick', labelsize = smallsize)    # fontsize of the tick labels
    plt.rc('legend', fontsize = smallsize)    # legend fontsize
    plt.rc('figure', titlesize = largesize)   # fontsize of the figure title

def save_plot(filepathpng: str, filepathpdf: str, filename: str) -> None:
    """ stores plot as png and pdf, for specified equipment name """
    plt.savefig(filepathpng+"\\"+filename+".png")
    plt.savefig(filepathpdf+"\\"+filename+".pdf")

def plot_statedistribution(df: pandas.DataFrame) -> None:
    """ creates a stacked barplot distribution plot for the entire dataframe provided """
    # pre-process dataframe
    df["totals"] = df[["time_idle",
                       "time_waiting",
                       "time_avoiding",
                       "time_busyladen",
                       "time_busyunladen",
                       "time_blocked"]].sum(axis=1)
    
    # calculate plot values
    x = df["equipment_name"]
    y1 = df["time_idle"]/df["totals"]
    y2 = df["time_waiting"]/df["totals"]
    y3 = df["time_avoiding"]/df["totals"]
    y4 = df["time_busyladen"]/df["totals"]
    y5 = df["time_busyunladen"]/df["totals"]
    y6 = df["time_blocked"]/df["totals"]
    
    # draw plots
    plt.bar(x, y1, 
        label="idle")
    plt.bar(x, y2, bottom=y1, 
        label="waiting")
    plt.bar(x, y3, bottom=y2+y1, 
        label="avoiding")
    plt.bar(x, y4, bottom=y3+y2+y1, 
        label="busyladen")
    plt.bar(x, y5, bottom=y4+y3+y2+y1, 
        label="busyunladen")
    plt.bar(x, y6, bottom=y5+y4+y3+y2+y1, 
        label="blocked")
    plt.legend()

    # add title and axis labels
    plt.title("Equipment status distribution")
    plt.xlabel("Equipment")
    plt.ylabel("State occupancy [%]")

def plot_throughputtimeline(df: pandas.DataFrame, cumulative: bool, mintime: float = 0.0,maxtime: float = 0.0) -> None:
    """ creates a line plot showing cumulative or non-cumulative throughput over time  """
    
    # create line plots for each equipment one by one
    for equipment in df["equipment_name"].unique():
        if cumulative == True:
            plt.plot(df[df["equipment_name"]==equipment]["time_sim"], df[df["equipment_name"]==equipment][["picks","places"]].sum(axis=1), label = equipment)
        else:
            plt.plot(df[df["equipment_name"]==equipment]["time_sim"], df[df["equipment_name"]==equipment][["pick","place"]].sum(axis=1), label = equipment)

    # if only a certain time window of results should be displayed then frame x axis accordingly
    if maxtime > 0.0:
        plt.xlim(mintime, maxtime)
    
    # add legend
    plt.legend()

    # add title and axis labels
    if cumulative == True:
        plt.title("Simulated cumulative throughput over time")
    else:
        plt.title("Throughput over time")
    plt.xlabel("Time [sec]")
    plt.ylabel("Throughput [-]")

def plot_pickstimeline(df: pandas.DataFrame, cumulative: bool, mintime: float = 0.0,maxtime: float = 0.0) -> None:
    """ creates a line plot showing cumulative or non-cumulative input over time  """
    
    # create line plots for each equipment one by one
    for equipment in df["equipment_name"].unique():
        if cumulative == True:
            plt.plot(df[df["equipment_name"]==equipment]["time_sim"], df[df["equipment_name"]==equipment]["picks"], label = equipment)
        else:
            plt.plot(df[df["equipment_name"]==equipment]["time_sim"], df[df["equipment_name"]==equipment]["pick"], label = equipment)

    # if only a certain time window of results should be displayed then frame x axis accordingly
    if maxtime > 0.0:
        plt.xlim(mintime, maxtime)
    
    # add legend
    plt.legend()
    
    # add title and axis labels
    if cumulative == True: 
        plt.title("Cumulative input over time")
    else:
        plt.title("Input over time")
    plt.xlabel("Time [sec]")
    plt.ylabel("Input [-]")

def plot_placestimeline(df: pandas.DataFrame, cumulative: bool, mintime: float = 0.0,maxtime: float = 0.0) -> None:
    """ creates a line plot showing cumulative or non-cumulative output over time  """
    
    # create line plots for each equipment one by one
    for equipment in df["equipment_name"].unique():
        if cumulative == True:
            plt.plot(df[df["equipment_name"]==equipment]["time_sim"], df[df["equipment_name"]==equipment]["places"], label = equipment)
        else:
            plt.plot(df[df["equipment_name"]==equipment]["time_sim"], df[df["equipment_name"]==equipment]["place"], label = equipment)

    # if only a certain time window of results should be displayed then frame x axis accordingly
    if maxtime > 0.0:
        plt.xlim(mintime, maxtime)
    
    # add legend
    plt.legend()

    # add title and axis labels
    if cumulative == True:
        plt.title("Cumulative output over time")
    else:
        plt.title("Output over time")
    plt.xlabel("Simulation time [sec]")
    plt.ylabel("Output [-]")

def plot_throughputavg(df: pandas.DataFrame) -> None:
    """ creates average (productive) throughput plots, stacked by picks and places """
    
    # calculate average hourly input (pick) and output (place)
    df = df[["equipment_name","pick","place"]].groupby("equipment_name").sum() / ((df["time_sim"].max() - df["time_sim"].min())/3600)

    # prepare plot values
    x = df.index.values
    y1 = df["pick"]
    y2 = df["place"]
    
    # draw plot
    plt.bar(x, y1, 
        label="input")
    plt.bar(x, y2, bottom=y1, 
        label="output")
    
    # add legends
    plt.legend()

    # add titles and axis labels
    plt.title("Hourly throughput by equipment")
    plt.xlabel("Equipment")
    plt.ylabel("Throughput [-/hr]")

def plot_positions(equipment: str, df: pandas.DataFrame, mintime: float = 0.0, maxtime: float = 0.0) -> None:
    """ creates a time-based polt of listed equipments, in x, y, z positions; 2D line plot; plot is created for one equipment only """

    # create plot 
    plt.plot(df["time_sim"], df["pos_x"],
        label = "x position")
    plt.plot(df["time_sim"], df["pos_y"],
        label = "y position")
    plt.plot(df["time_sim"], df["pos_z"],
        label = "z position")
    
    # if only a specific time frame should be visualized, adjust axis limits accordingly
    if maxtime > 0.0:
        plt.xlim(mintime, maxtime)

    # create legends
    plt.legend()

    # create titles and axis labels
    plt.title("Axis positions of " + equipment)
    plt.xlabel("Simulation time")
    plt.ylabel("Position [mm]")