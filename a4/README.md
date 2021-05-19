# a4
## Problem formulation
I treat the tweets as an array of data points, with the location as their "class" and the list of words as the data point. I train two different classifiers (naive bayes MAP and decision tree), using the "presence of word X in tweet Y" as the features of each tweet. The traind classifiers can be saved to `.json`  files, then tested on other input data.

## Program description

### Data parsing
I used regular expressions to parse the input data into a list of tweets, their respective location,
and list of words used. I also used the regex to filter out non-alphanumeric characters (as I found they are
not necessarily helpful for classification in this case). Finally, I filter out filler words that occur very frequently in the English language (such as "the", "and", "all", etc.), as they appear relatively equally throughout English discourse (and hence tweets). The precense of these words in a tweet does not provide any useful information.

### Naive Bayes classifier
We seek to find the class that maxizes `P(class | data)`, which we know is proportional to `P(data | class)P(class)`(where data is the list of words in the tweet, and class is the city that the tweet originated from).
So to train the bayes classifier, I simply calculate `log(P(class))` and `log(P(word | class))` for each word in the training data. This information is stored in a dictionary then saved to a `.json`file. Then when applying the classifier, I find the class that maxemizes `sum(log(P(word | class))) + log(P(class))` (summing over all the words in the tweet).

For words in the testing data that are not present in the training data, I calculate `log(P(word | class))` using Laplace smoothing.

### Decision tree classifier
The decision tree algorithm used is ID3. It recursively builds the tree up to a max depth of 10 (this hyperparameter was chosen somewhat arbitrarily by testing a few different depths). At each iteration of ID3, I look over a list of the top 100 occuring words in the dataset. I split the data based on whether or not a word is present in the tweet. I then choose to split the tree based on the word-split that minimizes entropy. At the bottom of the
tree, I classify the tweet based on which city appears most often in the resulting subset of data.

This processes results in a tree, stored as a nested dictionary `{val: "word/class", pos: {...}, neg: {...}}`.
The tree is saved to a `.json` to be used by the testing code. To apply the tree to testing data, I simply traverse the tree to find the leaf-node that applies to the input tweet (thus finding the class that best suits the tweet).

## Problems, assumptions, decisions
Most problems I ran into were just simple bugs or typos. I had no significant hurdles to overcome when creating these classifiers.

One big assumption is which common English words are good to filter out of the tweets. I used a Wikipedia article to help me find the most common words. But these words may carry some city-related information that I had not anticipated. Of course, I did anticipate some common words having useful information for the classifiers (such as "new", which correlates to tweets from "New York"). I also assumed, after a little testing, that it is best to filter out non-alphanumeric characters from the tweets.

In the decision tree training process, I assume that it is best to look at the most common words first. This makes sense, as these words are most likely to appear in tweets in the testing set. However, this decision may be cause me to miss some non-frequent words that give splits with lower entropy.

I decided to store my data in dictionaries/lists and `.json` files because this is a very simple process in python (one that I am already familiar with).

## Works Cited
* General python documentation ([docs.python.org](docs.python.org))
* Webpage from [towardsdatascience.com](https://towardsdatascience.com/) describing [Laplace smoothing](https://towardsdatascience.com/laplace-smoothing-in-na%C3%AFve-bayes-algorithm-9c237a8bdece#:~:text=Laplace%20smoothing%20is%20a%20smoothing%20technique%20that%20helps%20tackle%20the,the%20positive%20and%20negative%20reviews.). 
* Wikipedia article on [most common words in English](https://en.wikipedia.org/wiki/Most_common_words_in_English) for my list of `common_words`.
