# Part 1

## Formulating the Problem
    This is an HMM/Bayes Net problem. The problem was broken down into 5 parts that performed different calculations related to the Net.

## How the Program Works
    The program works in 5 steps:
        1. The data is read in and word tallies are made. The word tallies break into three categories: how a sentence starts, which words are seen, and which pos transitions are seen. These form the basis for start, output (emission), and transition probabilities. (define.py)
        2. The word tallies are transformed into probabilities. The words for the start tallies are combined according to the pos it was assigned. These tallies per pos are then divided by the total word count. The output probabilities are found by totaling the tally of the word in all possible parts of speech and then dividing by the total per pos. The transition probabilities are found by totaling all of the words for a specific pos and then dividing each transition from that pos by the total. (prob.py) Both of these are done in the train function of pos_solver.py. 
        3. Then program finds the most likely sequence of parts of speech using both the simplified and hmm models. 
            a) Simplified: Uses the equation in step one of the A3 pdf. Looks at the occurrence of each word in each pos, calculates the likelihood and then the pos with the largest probability is chosen. If a word has never been seen before or has not been seen in a particular pos, it assigns the probability as .001/total number of words. The probabilities for each chosen pos tag are saved to be used in calculating the log of the posterior for the simple model. (simple.py) 
            b) HMM: Uses the equation in step 2 of the A3 pdf, which is the viterbi algorithm. This sets up a dictionary of each possible pos at each time stamp. If a word is the start of the sentence, the dictionary keeps check of the start probability * output probability. Otherwise, it drops the start probability and also takes into account the transition from the any previous pos to any current pos as well as the largest value from the previous pos. The new previous for the incoming pos node becomes the largest value from any previous pos node. Once all timestamps are accounted for, each timestamp is checked for the largest value and the associated pos becomes the designated pos for that word. (viterbi.py) 
        4. The program then finds the confidence of the viterbi model. It does this by calculating the marginal probability of each tag chosen for each word and reuses some of the code from the simple.py file. 
        5. The log of the posteriors are calculated for each model. 

## Problems, Assumptions, Design Decisions
    This problem was compartmentalized into different files to make it easier to work with. 

# Part 2
## Formulating the problem
Generally, the decryption problem is solved with a gradient descent. Each possible decryption is a particular T=(rearr_table, replace_table) pair.
The value given to each T is the product of all character transition probabilites (so treating the docment as a long markov chain).
These transition probabilities are calculated from the english 'corpus.txt' file.
Then the Metropolis-Hastings algorithm is used to find increasingly better decryption pairs T to decode the text.

## How the program works
1. English transition probabilities (letter-to-letter) are calculated given the 'corpus.txt' file. These are stored in 'transLL.json' for future use.
1. The Metropolis-Hastings algorithm is run for 10,000 iterations starting at a random T=(rearrange_table, replace_table).
1. Only the first 2,500 characters in the document are used when calculating P(D) (probability of the decoded text being english). Using trial and error, I found that only the first 2,500 characters are really necessary to reasonably show that the decoded text is english.
1. After 10,000 iterations, the Metropolis-Hastings algorithm is restarted at a new initial T value. This processes is repeated until the time limit runs out (360 seconds).
1. After the time limit runs out, the document is decoded with the best T=(rearrange_table, replace_table) pair, and the resulting text is saved to another file.

## Problems, assumptions, simplifications
* Initially I had trouble getting the regex to detect overlapping substrings when calculating the transition probabilities. For example "ee" substring can overlap with itself. To fix this, I used lookahead assertion (see python docs).
* I tried running more iterations of Metro-Hastings on smaller chunks of text; however, the english statistics of the text does not contain enough information in smaller chunks. I ended up finding 2,500 characters was enough (just by trial-and-error).
* For a while I had a bug from not doing full copies of the tuple T=(rearrange_table, replace_table)... but everything worked fine once this was fixed.
* I used log-likelihood transition probabilities once I realized they approached zero so quickly
* Also a non-infinite log probability was necessary for transitions that we don't have data for in the corpus.txt file (like 'zj'). If the log-probability -inf was used, then the probability of almost every incorrectly decoded document would be '-inf' (which isn't too helpful). Instead I found that a very small probability was good enough (I just used -30).
* I decided to save the transition probabilities in a file ('transLL.json'). This makes it much quicker to run break_code.py.

# Part 3

## Formulating the Problem

Basically followed the outline given in the assignment pdf.

## How the Program Works

1) Downloads 3 book files to use as training corpus.
1) `training.py` creates transition probabilities for characters and trains character detection data structure.
1) `training.py` has simple prediction code.
1) `vit.py` has HMM code called via `training.py`s

## Problems, Assumptions, Design Decisions

Initial implementation of probability of a letter given the image was effective, but could not interact well when including previous letter prediction probability.
Had to re-write program to interact with it.

Ran into the small-float problems. Using python's `Decimal` class didn't really work due to hasty implementation.
Finally got log math working.
