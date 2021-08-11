# Bugcrowd Platform Advertised Programs Analysis

## Step 1: Data Extraction
Pyhton (3.8.2) script for this step: [Step1.py](https://github.com/aytuncilhan/BugcrowdAnalysis/blob/82085841dbb6370f643da0cc0753f98613ddeb88/Step1.py)

The site uses JSON format to read Programs data but in batches of size 25. Each batch is iteratively read and the results are written into [bugcrowd_Programs.csv](https://github.com/aytuncilhan/BugcrowdAnalysis/blob/master/bugcrowd_Programs.csv)

## Step 2 - 3: Data Analysis
Pyhton (3.8.2) script for this step: [Step2-3.py](https://github.com/aytuncilhan/BugcrowdAnalysis/blob/82085841dbb6370f643da0cc0753f98613ddeb88/Step2-3.py)

BeautifulSoup package is used for HTML parsing and Pandas is used for data storage.

The “Program Details” are stored under a div with class name “bounty-content”. The details of the search and filter algortihms can be found in comment blocks in the code. The overall procedure is summarized below with some examples. 

1. for each program, using [the CSV file obtained in Step 1](https://github.com/aytuncilhan/BugcrowdAnalysis/blob/master/bugcrowd_Programs.csv), the text including program details is retrieved using `ProgramDetails = soup.find_all('div', {'class': 'bounty-content'})`

2. Then, the text is cleaned to be in compliance with the search algorithms (e.g. $1.5k is converted to $1500).

Below is the code piece where the search text is cleaned from some prepositions since they cause false positives. There are instances where there might be non-bounty related descriptions in the text including the $ symbol and a number which is picked up by the search algorithm. These non-bounty related dollar amounts usually come after prepositions. Hence, removing prepositions from the text solves the issue of finding false positive bounty numbers.

```python
for item in arr:
        # Search for prepositions coming right before a $ amount to rule out unrelated descriptions 
        exclude_text = ['for', 'a', 'on']
        if('$' in item and arr[i-1] in exclude_text):
            del arr[i]
```

This approach can be extended to implement **removing Stopwords** which are words that don't contribute to the meaning or substance of the text (e.g. "the", "at", "in", "on", "by", "for" etc.). There are custom-built libraries to remove stopwords from the search text.

3. The search algorithm parses through the _cleaned text_ using regular expressions (searching for specific tags e.g. `tag1_numsMax = re.findall(r"max&quot;:(.*?)[^\d]", searchText)`) and other list operations to find dollar amounts while ruling out false positive cases and false negative cases.

    A sample case where cleaning prevents false positives:

    > The `'min&quot;:` tag occurs right before a local min (and possibly global min) bounty amount. Respectively, `"min&quot;:null"` occurence will be rendered as $0. But `'min&quot;:null&quot;max&quot;:null'` occurences are **not renedered** and only appear as placeholder tags in HTML. If `'min&quot;:null&quot;max&quot;:null'` is not removed from the search text, the search algortihm will think there is a 0$ due to the `'min&quot;: '` part wheras in reality, it's not even displayed on the page. Hence, a false positive scenario would occur.

    A sample case where cleaning prevents false negatives:

    > There are cases where the intervals are displayed as "Up to: $100" (which mathematically means "$0 - 100$"). In this case, the search algorithm fails to add $0 to the found bounties list - hence a false negative case occurs. To handle this exception, a conditional is implemented to check if "Upto:" (yes, in the html text there is no space between up and to) exists in the search text and if so, "0" is added into the found bounties list.

4. All the retrieved dollar amounts (bounties) are stored in a list. Minimum value in the list is the minimum bounty of the program and the same logic applies for maximum bounty Each program's name, url, min bounty, and max bounty values are stored in a Pandas dataframe [bugcrowd_bounties.pkl](https://github.com/aytuncilhan/BugcrowdAnalysis/blob/97873e93dd6ef5681f90ef336137c66a68affe90/bugcrowd_bounties.pkl) to be read in Step 4.
          section_title<a name="Step 5: Future Work"></a>    


## Step 4: Results
Pyhton (3.8.2) script for this step: [Step4.py](https://github.com/aytuncilhan/BugcrowdAnalysis/blob/82085841dbb6370f643da0cc0753f98613ddeb88/Step4.py)

In this step, the minimum and maximum dollar amounts obtained in step 3 (which are stored in [bugcrowd_bounties.pkl](https://github.com/aytuncilhan/BugcrowdAnalysis/blob/97873e93dd6ef5681f90ef336137c66a68affe90/bugcrowd_bounties.pkl)) is read to plot the histogram of minimum and maximum dollar amounts in bugcrowd programs. 

In doing so,
* Removed dataframe items which have $0 as both minimum and maximum values (since this means no bounty data was found for that program).
* The values _are not_ rounded to full 1000s since this distored the dataset values: For instance, many of the Min bounty values were are rounded to 0 since they are less then 500 and hence get ruled out... Nevertheless, the line to round values is still there, just commented out:
    `bounties = [round(num,-3) for num in bounties]`

As required in the exercise, there are two plots to be generated: **Minimum Bounty Histogram** and **Maximum Bounty Histogram**. 

The plots look nicer and more meaningful when the x-axis is plotted in log scale (since the values increase drastically even if they are all Min - or respectively all Max). However, both linear scale and log scale x-axis versions of the histograms are plotted and depicted below (In the script, I've added a scale parameter to a custom plot function to specify x-axis scale: `plotHistograms(minB, maxB, 'log')`)

Below are the histograms generated using matplotlib:
Log scale x-axis | Linear scale x-axis
------------ | -------------
![Plot](https://github.com/aytuncilhan/BugcrowdAnalysis/blob/a8021d809b4ec4694ebe38a05781df710e963a48/Plots/LogscaleHistograms.png) | ![Plot](https://github.com/aytuncilhan/BugcrowdAnalysis/blob/753011a530752bba6f056d5b246da596a73ec6f1/Plots/LinearscaleHistograms.png) 

## Step 5: Future Work

For further analysis, the following points can be considered for 

### 1. Improving Processing Speed & Efficiency

* Removing stop words from the search text (e.g. removing prepositions). A similar exercise is carried out in the code and explained in detail in Step 2 - 3 section above.
* Normalizing the text using methods as Stemming (removing unnecesary suffixes) and Lemmatization (transofrming words into their root form).

### 2. Identifying Thematically Similar Blocks

To identify patterns and thematically similar blocks the following points can be considered.

#### 2.1. Collocation Analysis

Collocation Analysis can be done using some "predefined words/phrases" to find out which words are mentioned together with these predefined words. This way, thematically similar blocks can be clustered. 

To identify these "predefined words", unsupervised machine learning can be used. This way, we obtain naturally existing patterns and analyse the results to see if the they are sensible. If the resulsts from unsupervised machine learning is promising, we can go for a supervised machine learning as well.

In addition to unsupervised machine learning, we can also do a Simple Freqeuncy Analysis to see which themes/topics are mostly mentioned in the descriptions.

#### 2.2. Simple Frequency Analysis
Carrying out a word frequency analysis for the program descriptions is a simple and cost effective way to extract isnights as,
* Mostly mentioned themes/technologies in bugcrowd customers (e.g. in areas like cyber security, cloud technologies, various business models etc.)
* Bugcrowd’s business customer profile. More specifically, to asnwer _"which type of industries/companies require bugcrowd services the most?"_.

### 2.3. Manual Scan
As a last resort, assuming items 1 and 2 have not produced fruitful results, we can always manually scan the program details focusing on program descriptions, the metadata as average bounty pay, company information etc. to identify similarities and common themes across different programs.

### 3. Bonus: What should **not** be done
* Sentiment Analysis won’t make sense since most probably all will turn out to be neutral.
* Lexical Diversity Analysis won't make sense since we are not interested in lingustic complexity of authors.
