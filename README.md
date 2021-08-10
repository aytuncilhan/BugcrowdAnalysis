# Bugcrowd Platform Advertised Programs Analysis

## Step 1:
The site uses JSON format to read Programs data but in batches of size 25. Each batch is iteratively read and the results are written into [bugcrowd_Programs.csv](https://github.com/aytuncilhan/BugcrowdAnalysis/blob/master/bugcrowd_Programs.csv)

## Step 2 - 3: Data Analysis
BeautifulSoup package is used for HTML parsing and Pandas is used for data storage.

The “Program Details” are stored under a div with class name “bounty-content”.

Once obtained the raw text including program details, regular expressions and list operations are used to find dollar amounts (ruling out false-friends).

## Step 4: Results

Lorem ipsum dolor

## Step 5: Future Work

As a future work, 

### 1. Simple Frequency Analysis
Word frequency analysis in the program descriptions can be done. This way, the following insights can be extracted:
* Mostly mentioned technologies in cyber security, cloud technologies, 
* Bugcrowd’s program (or business customer) profile. E.g. "which type of industries require bugcrowd services the most?"

### 2. Collocation Analysis

First spend: unsupervised ML to see top 10 topics. Depending on the result (if promising), you can go for a supervised ML.

Collocation Analysis to "predefined words" can be done to find out which words are mentioned together with our area of interest (the area of interest will be the "predefined words"

#### Unsupervised Machine Learning
To identify the area of interests (respectiveley the "predefined words" to be used in Collocation Analysis), we can initially do an *unsupervised machine learning* algorithm to see what words come out.

Along with the outcome of the unsupervised learning, we can also use the words obtained by Simple Freqeuncy Analysis in step 1. As a last resort, assuming Steps 1 and 2 have not produced fruitful results for our Collocation Analysis, we can always do manually scan program details focusing on program descriptions, metadata, company information etc.

### 3. What should *not* be done
* Lexical Diversity Analysis won't make sense since we are not interested in lingustic complexity of authors.
* Sentiment Analysis won’t make sense since most probably all will turn out to be neutral.
