# Import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

#Schritt 4:
def main():

    # Read pickled data from
    readPkl = '/Users/aytuncilhan/Projects/bugcrowd_bounties.pkl'

    df = pd.read_pickle(readPkl) 

    # Clean data before plotting
    df = cleanData(df)

    # Retrieve Min and Max Bounty from the lists
    minB = df["MinBounty"]
    maxB = df["MaxBounty"]

    # For debug
    #pd.set_option('display.max_rows', None)
    #print(df)

    # Custom function to plot Histogram provifing the scale to be log
    # Scale can be Log scale or Linear scale
    plotHistograms(minB, maxB, 'log')

# Below are the custom Functions used in main

def cleanData(df):
    # Removed programs which have $0 as both minimum and maximum values 
    # (since this means no bounty data was found for this program)
    df = df[df['MaxBounty'] > 0 ]

    # Reset the indexing
    df.reset_index(drop=True, inplace=True)

    return df

def plotHistograms(minB, maxB, scale):

    # Log scale
    logbins = np.geomspace(maxB.min(), maxB.max(), 24)

    # Ticker for thousand separator commas
    fmt = '${x:,.0f}'
    tick = mtick.StrMethodFormatter(fmt)

    #Main Title for two subplots
    plt.suptitle("Min and Max Bounty Amount Histograms \n of Bugcrowd Programs", y=0.985, size=16)

    # First Subplot: Histogram of Min Bounty
    plt.subplot(2, 1, 1)
    ax = plt.subplot(2, 1, 1)
    plt.title('Histogram of Min Bounty')
    # Check if log specified. Default set to linear
    if(scale=='log'):
        plt.hist(minB, color='steelblue', bins=logbins, alpha=0.8, label='Min Bounty')
        plt.xscale('log')
    else:
        plt.xlabel('Bounty ($)')
    ax.xaxis.set_major_formatter(tick) 
    plt.ylabel('Occurence Count')
   
    # Seconf Subplot: Histogram of Max Bounty
    plt.subplot(2, 1, 2)
    ax = plt.subplot(2, 1, 2)
    plt.title('Histogram of Max Bounty')
    # Check if log specified. Default set to linear
    if(scale=='log'):
        plt.hist(maxB, color='firebrick', bins=logbins, alpha=0.8, label='Max Bounty')
        plt.xscale('log')
    else:
        plt.hist(maxB, color='firebrick', bins=24, alpha=0.8, label='Max Bounty')
    plt.xlabel('Bounty ($)')
    ax.xaxis.set_major_formatter(tick) 
    plt.ylabel('Occurence Count')
    plt.tight_layout()

    plt.subplots_adjust(left=None, bottom=None, right=None, top=0.8, wspace=None, hspace=0.7)

    plt.show()
    
if __name__ == '__main__':
    main()