# Bugcrowd Platform Advertised Programs Analysis

## Step 1:
Packages used: json and csv
The site uses JSON to retrieve data but in batches of size 25. 
Parsed each batch iteratively and collected the results in a list to write in the CSV.

## Step 2 - 3: Data Analysis
Packages used: BeautifulSoup for web scarping, Pandas for data collection
The “Program Details” are stored under a div with class “bounty-content”.
Remark:
Once obtained the raw text including program details, used regular expressions to find dollar amounts. Filtered empty list elements out and converted the string matrix into an integer matrix.

## Step 4: Results

Lorem ipsum dolor

## Step 5: Future Work

Word frequency analysis of company names
Word frequency analysis of program descriptions 
* Most of the descriptions have the word security)
* Maybe some have “management" etc.
* This way we find out what industries are Bugcrowd’s customers

Sentiment analysis won’t make sense since most probably all will turn out neutral.

Collatation analysis of specific words 
* E.g. colotation analysis of the word unity: over the entire dataset you check which words this words is mentioned together.

First spend: unsupervised ML to see top 10 topics. Depending on the result (if promising), you can go for a supervised ML.

Rewards Targets

If no accurate results - we can go thru the program details manually ...
* Title - company description etc.
