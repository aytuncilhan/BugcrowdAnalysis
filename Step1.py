# Terminal > pip3 install requests
# Import packages
import json
import requests
import csv

#Schritt 1: Datenextraktion 1
def main():

    # Initiate variables
    sourceURL = "https://bugcrowd.com/programs.json"
    destination = "/Users/aytuncilhan/Projects/bugcrowd_Programs.csv"
    headerCSV = ["ProgramName", "ProgramURL"]
    programCount = getTotal(sourceURL)
    increment = 25
    programs = []

    # Loop through the JSON files until we reach totalCount to populate the programs list
    for offset in range(0, programCount, increment):
        programs += decodeJSON(sourceURL + "?offset[]=" + str(offset))

    # Produce the CSV file using the programs list
    writeCSV(programs, headerCSV, destination)

# Below are the custom Functions used in main

# Returns how many programs exist in total on BugCrowd
def getTotal(url):
    jsonText = requests.get(url).text 
    readjson = json.loads(jsonText)
    return readjson['meta']['totalHits']

# Decode a JSON file into a list given the URL
def decodeJSON(url):
    jsonText = requests.get(url).text 
    readjson = json.loads(jsonText)
    return readjson['programs']

# Produce CSV file given a list of programs, headers, and a file path
def writeCSV(programs, headers, filePath):
    with open(filePath, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        # Write name and URL for each program item into CSV iteratively
        for index in range(0, len(programs)):
            progName = programs[index]['name']
            progURL = "https://bugcrowd.com" + programs[index]['program_url']
            writer.writerow([progName, progURL])

if __name__ == '__main__':
    main()