# Bugcrowd Platform Advertised Programs Analysis

## Step 1: Data Extraction
The site uses JSON format to read Programs data but in batches of size 25. Each batch is iteratively read and the results are written into [bugcrowd_Programs.csv](https://github.com/aytuncilhan/BugcrowdAnalysis/blob/master/bugcrowd_Programs.csv)

## Step 2 - 3: Data Analysis
BeautifulSoup package is used for HTML parsing and Pandas is used for data storage.

The “Program Details” are stored under a div with class name “bounty-content”.

Once obtained the raw text including program details, regular expressions and list operations are used to find dollar amounts (ruling out false-friends).

## Step 4: Results

In this step, the minimum and maximum dollar amounts obtained in step 3 are evaluated and a graph of the frequency of the minimum and maximum dollar amounts (histogram) is created. 

In doing so,
* Removed dataframe items which have $0 as both minimum and maximum values (since this means no bounty data was found for that program).
* The values are not rounded to full 1000s as it distored the dataset values :grimacing:. For instance most of the Min bounty values for rounded to 0 and hence ruled out... Albeit, the line to round values is still there, just commented out:
*  `bounties = [round(num,-3) for num in bounties]`

Below are the histograms generated useing matplotlib:

## Step 5: Future Work

As a future work, the following points can be considered:

### 1. Simple Frequency Analysis
Word frequency analysis in the program descriptions can be done. This way, the following insights can be extracted:
* Mostly mentioned technologies in cyber security, cloud technologies, 
* Bugcrowd’s program (or business customer) profile. E.g. "which type of industries require bugcrowd services the most?"

### 2. Collocation Analysis

Collocation Analysis can be done using some "predefined words" to find out which words are mentioned together with our area of interest (the area of interest will be the "predefined words". To identify the predefined words, we can do an unsupervised machine learning.

#### 2.1. Unsupervised Machine Learning 
To identify the area of interests (respectiveley the "predefined words" to be used in Collocation Analysis), we can initially do an *unsupervised machine learning* algorithm to see what word patterns come out (e.g. top 10).

#### 2.2. Supervised Machine Learning
If the resulsts from unsupervised machine learning is promising/sensible, we can go for a supervised machine learning as well.

Along with the outcome of the unsupervised learning, we can also use the words obtained by Simple Freqeuncy Analysis in step 1 . 

As a last resort, assuming Steps 1 and 2 have not produced fruitful results for our Collocation Analysis, we can always do manually scan program details focusing on program descriptions, metadata, company information etc.

### 3. What should **not** be done
* Sentiment Analysis won’t make sense since most probably all will turn out to be neutral.
* Lexical Diversity Analysis won't make sense since we are not interested in lingustic complexity of authors.
