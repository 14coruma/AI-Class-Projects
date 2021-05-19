###################################
# CS B551 Fall 2020, Assignment #3
#
# Your names and user ids:
# Alex Fuerst (alfuerst), Andrew Corum (amcorum), Kaitlynne Wilkerson (kwilker)
#
# (Based on skeleton code by D. Crandall)
#


import random
import math
import define 
import prob
import simple
import viterbi


# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:
    
    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling. Right now just returns -999 -- fix this!
    def posterior(self, model, sentence, label):
        if model == "Simple":
            total = 1
            for i in simpler:
                total *= i
            result = math.log(total,10)
            return result
        elif model == "HMM":
            total = 1
            for i in confidence:
                total *= i
            result = math.log(total, 10)
            return result
        else:
            print("Unknown algo!")

    # Do the training!
    #
    def train(self, data):
        """
        Splits data from file into words and pos. Passes this data to the define file so that the parameters are found. 
        """
        
        for d in data:
            words = d[0]
            pos = d[1]
            define.define(words, pos)
        prob.probstart()
        prob.probtran()
        totalwords = prob.probout()

    # Functions for each algorithm. Right now this just returns nouns -- fix this!
    #
    """
    The following 3 functions returns the pos per word. 
    """
    def simplified(self, sentence):
        new = list(sentence)
        total = prob.totalwords
        simplepath = []
        global simpler
        simpler = []
        for i in new:
            (tag, largest) = simple.find(i, total)
            if tag == None: # this works
            #finds tag for word not previously seen
                l = len(simplepath) -1 
                if len(simplepath) > 0:
                    l = len(simplepath) -1 
                    tag = simple.examineTransition(simplepath[l])
                else:
                    tag = simple.examineTransition('.')
            simplepath += [tag]
            simpler += [largest]
        return simplepath

    def hmm_viterbi(self, sentence):
        new = list(sentence)
        total = prob.totalwords
        hmmpath = []
        global h
        h = []
        count = 0
        for i in new:
            if count == 0: 
                viterbi.start(i, total)
            else:
                viterbi.rest(i, total)
            count += 1
        hmmpath = viterbi.trace()
        hmm = []
        for i in hmmpath:
            hmm += [i[1]]
            h += [i[0]]
        return hmm

    def confidence(self, sentence, answer):
        global confidence
        confidence = []
        for i in range(0, len(sentence)):
            simple.find(sentence[i], prob.totalwords)
            pr = simple.con[answer[i]]
            confidence += [pr]
        return confidence


    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #

    """
    Calls the above 3 functions to display to the screen.
    """
    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        else:
            print("Unknown algo!")

