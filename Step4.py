# Import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

    # Custom function to plot Histogram
    plotHistograms(minB, maxB)

# Below are the custom Functions used in main

def cleanData(df):
    # Removed programs which have $0 as both minimum and maximum values 
    # (since this means no bounty data was found for this program)
    df = df[df['MaxBounty'] > 0 ]

    # Reset the indexing
    df.reset_index(drop=True, inplace=True)

    return df

def plotHistograms(minB, maxB):

    logbins = np.geomspace(maxB.min(), maxB.max(), 24)

    plt.suptitle("Min and Max Bounty Amount Histograms \n of Bugcrowd Programs", y=0.985, size=16)
    plt.subplot(2, 1, 1)
    plt.title('Histogram of Min Bounty')
    plt.hist(minB, color='steelblue', bins=40, alpha=0.8, label='Min Bounty')
    plt.xlabel('Bounty ($)')
    plt.ylabel('Occurence Frequency')
   
    plt.subplot(2, 1, 2)
    plt.title('Histogram of Max Bounty')
    plt.hist(maxB, color='firebrick', bins=logbins, alpha=0.8, label='Max Bounty')
    plt.xscale('log')
    plt.xlabel('Bounty ($)')
    plt.ylabel('Occurence Frequency')
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()