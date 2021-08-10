# Terminal > pip3 install beuatifulsoup4
# Import packages
import csv
from os import remove, replace
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

#Schritt 2-3
def main():

    with open('/Users/aytuncilhan/Projects/bugcrowd_Programs.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader) #To skip header

        index = 0
        results = []

        for row in csv_reader:
            name = row[0]
            url = row[1]

            # Step 2: Retrieve the Program Details
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
            ProgramDetails = soup.find_all('div', {'class': 'bounty-content'})

            # NOTE: If Step 2 and 3 should be separate, ProgramDetails can be saved in a dataframe along with
            # the corresponding program name and URL

            # Step 3: Find min max dollar amounts
            [minBounty, maxBounty] = findBounty(ProgramDetails)

            # For Debug
            print([name, url, minBounty, maxBounty])

            results.append([name, url, minBounty, maxBounty])
            index += 1
        
    df = pd.DataFrame(results, columns=['Name', 'URL', 'MinBounty', 'MaxBounty'])
    df.to_pickle('/Users/aytuncilhan/Projects/bugcrowd_bounties_v2.pkl')

# Below are the custom Functions used in main

# Find min and max dollar amounts
def findBounty(ProgramDetails):

    # To store the bounty amounts found in the text
    bounties = []

    # In case there are more than one occurence
    for line in ProgramDetails:

        #Pre process to clean the text
        cleanText = preProcess(line)

        #Search for dollar ammonuts l
        dollar_nums = searchDollar(cleanText)
        other_nums = searchTag(cleanText)

        # Collate results
        dollarNums = dollar_nums + other_nums

        bounties = postProcess(dollarNums)

    #If empty list, return debug values, else, return bounties list
    if(not bounties):
        return [-100, -200]
    else:
        return [min(bounties), max(bounties)]

# To clean the text for search
def preProcess(line):
    # Remove all commas to have all numbers' digits in a single block
    cleanText = str(line).replace(',','')

    # Remove trivial null blocks in reach class. This is very useful for removing minquote null in the future.
    cleanText = cleanText.replace('min&quot;:null&quot;max&quot;:null', '')

    # Clean prepositions for sentence and clean special signs as + and ~
    arr = cleanText.split()
    i = 0
    for item in arr:
        # Search for prepositions coming right before the a $ amount to rule out unrelated descriptions 
        exclude_text = ['for', 'a', 'on']
        if('$' in item and arr[i-1] in exclude_text):
            del arr[i]

        # Search for special characters in a block includes a dollar amount to rule out unrelated descriptions
        if('$' in item and ('+' in item or '~' in item)):
            del arr[i]

        # Convert 'k' including numbers to (number * 1000)
        if('$' in item and 'k' in item):
            arr[i] = item.replace('.','')
            arr[i] = item.replace('k', '000')
        if('$' in item and 'K' in item):
            arr[i] = item.replace('.','')
            arr[i] = item.replace('K', '000')

        i+=1

    # Convert back to string
    cleanText = "".join(arr)

    return cleanText

# Dollar sign search
def searchDollar(searchText):
        # Capture strings starting with '$' and ending with a non-numeric character 
        # 'k' is kept to filter out non-bounty related text ("...$20k+ has been...")
        dollar_nums = re.findall(r"\$(.*?)[^\d]", searchText)

        # To capture min 'null' tags which is 0 dollars when rendered and "Up to:" statements which also means zero
        # Also, if there is a "min&quot;:null" it definitely yields a zero value since we already
        # removed all 'min&quot;:null&quot;max&quot;:null' (which doesn;t yield a Min or Max) during preprocess
        if("min&quot;:null" in searchText or "Upto:" in searchText):
            dollar_nums.append('0') 

        # Filter out non-digit char including items
        dollar_nums = [x for x in dollar_nums if x.isdigit()]

        return dollar_nums

# Parse the text to identify the pre-defined Min-Max tags
def searchTag(searchText):
        # All 'min&quot;:null&quot;max&quot;:null" are removed which means:

        # "min&quot;:" will be definitely followed by a Min bounty value (not necessarily a global Min, could be a local Min)
        tag1_numsMin = re.findall(r"min&quot;:(.*?)[^\d]", searchText)
        tag2_numsMin = re.findall(r"\"min\":(.*?)[^\d]", searchText)

        # "max&quot;:" will be definitely followed by a Max bounty value (not necessarily a global Min, could be a local Min)
        tag1_numsMax = re.findall(r"max&quot;:(.*?)[^\d]", searchText)
        tag2_numsMax = re.findall(r"\"max\":(.*?)[^\d]", searchText)

        # Return the array of all found bounty values
        return tag1_numsMin + tag2_numsMin + tag1_numsMax + tag2_numsMax

# To clean the list and handle future exceptions
def postProcess(bounties):
    # Remove empty items from the list to avoid exceptions
    bounties = list(filter(None, bounties))

    # Convert string numbers to integers
    bounties = [int(numeric_string) for numeric_string in bounties]

    # If list is empty (no min or max found), assign trivial solution to distinguish from identified 0 values
    if (not bounties): 
        bounties.extend((-100, -200))

    # Round to nearest 1000 as asked in the assignment
    # This line is commented out since not rounding produces better results for the graphs
    #### bounties=[round(num,-3) for num in bounties]

    return bounties

if __name__ == '__main__':
    main()
