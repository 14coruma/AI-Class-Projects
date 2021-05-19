#!/usr/bin/python3
# Build and test tweet location classifiers (MAP and DT)
# By Andrew Corum (Dec 2020)
from argparse import ArgumentParser, RawTextHelpFormatter
import re
import json
import math
import random

classes = ['LosAngeles', 'SanFrancisco', 'Manhattan', 'SanDiego', 'Houston',
        'Chicago', 'Philadelphia', 'Atlanta', 'Toronto', 'Washington', 'Orlando',
        'Boston']

# Most common words in English (list found on wikipedia)
# Ignore these in tweets (don't really add much information)
# Still use some obviously helpful words (like "new")
# List of words is a subset taken from Wikipedia's article on "Most commen words in English"
common_words = ['the', 'be', 'to', 'of', 'and', 'in', 'a', 'that', 'have', 'i',
        'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this',
        'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 'an',
        'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what', 'so', 'up',
        'out', 'if', 'about', 'who', 'get', 'which', 'when', 'make',
        'can', 'like', 'no', 'just', 'him', 'know', 'take', 'into',
        'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other', 'than',
        'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also',
        'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well',
        'way', 'even', 'want', 'because', 'any', 'these', 'give', 'day', 'most',
        'job', 'jobs', 'is', 'im', 'hiring', 'careerarc', 'were', 'latest', 'amp',
        'click', 'here', 'me', 'was']

# Handle program arguments
def get_args():
    parser = ArgumentParser(description="Build and test tweet location classifiers.")
    subparser = parser.add_subparsers(title="mode", dest="mode", help="Choose to 'train' or 'test' a model")
    subparser.required = True

    # Parser for train-mode
    train_parser = subparser.add_parser('train', help="train a model")
    train_parser.add_argument("type", type=str, choices=['bayes', 'dtree'],
            help="classifier type")
    train_parser.add_argument("training_input", type=str, help="Input training data file location")
    train_parser.add_argument("model_output", type=str, help="Output model file location")

    # Parser for test-mode
    test_parser = subparser.add_parser('test', help="test a model")
    test_parser.add_argument("type", type=str, choices=['bayes', 'dtree'],
            help="classifier type")
    test_parser.add_argument("model_input", type=str, help="Input model file location")
    test_parser.add_argument("testing_input", type=str, help="Input testing data file location")
    test_parser.add_argument("testing_output", type=str, help="Output classified tweets file location")

    args = parser.parse_args()
    return args

# Process input data (loction & tweets)
def parse_data(raw):
    # Filter out non alphanumeric characters
    raw = re.sub('[^a-zA-Z\d\n ]', '', raw)
    data = []
    pattern = re.compile('(' + '|'.join(classes) + ')\w* (.*)')
    # Put data into array, storing city and list of words
    for line in raw.splitlines():
        matches = pattern.match(line)
        if matches:
            words = matches.groups()[1].lower().split()
            data.append([matches.groups()[0], [w for w in words if w not in common_words]]) 
    return data

# Print top 5 words for each city (for bayes model)
def bayes_top_5(model):
    for city in classes:
        top_words = []
        for word in model['word_counts']:
            count = 0
            for k in model['word_counts'][word]: count += model['word_counts'][word][k]
            if count >= 5:
                prob = math.log(model['word_counts'][word][city])-model['total_words'][city]
                top_words.append((prob, word))
                top_words.sort(reverse=True)
                if len(top_words) > 5: top_words = top_words[:5]
        print("{}: {}".format(city, ', '.join([w for p,w in top_words])))

# Train a naive bayes classifier (MAP)
def train_bayes(data):
    prior = {key: 0 for key in classes}
    total_words = {key: 0 for key in classes}
    word_counts = {}
    for row in data:
        prior[row[0]] += 1
        total_words[row[0]] += len(row[1])
        for word in row[1]:
            if word not in word_counts.keys():
                # Each word have a count of at lest 1 (laplace smoothing)
                word_counts[word] = {key: 1 for key in classes}
            word_counts[word][row[0]] += 1
    for key in prior:
        prior[key] = math.log(prior[key] / len(data))
    for key in total_words:
        total_words[key] = math.log(total_words[key])
    return {'prior': prior, 'total_words': total_words, 'word_counts': word_counts}

# Test a naive bayes classifier
def test_bayes(model, data):
    estimates = []
    num_correct = 0
    for row in data:
        max_prob = float('-inf')
        max_city = None
        for city in classes:
            prob = model['prior'][city]
            for word in row[1]:
                w_count = 0 if word not in model['word_counts'] else math.log(model['word_counts'][word][city])
                prob += w_count - model['total_words'][city] - math.log(len(row[1]))
            if prob > max_prob:
                max_prob = prob
                max_city = city
        if max_city == row[0]: num_correct += 1
        estimates.append(max_city)
    print("Accuracy: {}".format(num_correct / len(data)))
    return estimates

# Recursively print the top levels of a decission tree
def dtree_to_string(tree, max_depth=3, curr_depth=3):
    nTabs = max_depth - curr_depth
    if not tree: return ''
    if curr_depth == 0: return '    '*nTabs + tree['val']
    return format("{}\n{}\n{}".format(
        '    '*nTabs + tree['val'],
        dtree_to_string(tree['pos'], max_depth, curr_depth-1),
        dtree_to_string(tree['neg'], max_depth, curr_depth-1)))

# Calculate average entropy of a split
# If the word is present in tweet, then classify as pos_class (otw neg_class)
def split_entropy(word, data_pos, data_neg):
    prob_class_pos = [len(list(filter(lambda x: x[0] == c, data_pos)))/len(data_pos) for c in classes]
    prob_class_neg = [len(list(filter(lambda x: x[0] == c, data_neg)))/len(data_neg) for c in classes]
    prob_pos = len(data_pos)/(len(data_pos)+len(data_neg))
    prob_neg = len(data_neg)/(len(data_pos)+len(data_neg))
    return prob_pos * sum(map(lambda x: 0 if x == 0 else -x*math.log(x), prob_class_pos)) + prob_neg * sum(map(lambda x: 0 if x == 0 else -x*math.log(x), prob_class_neg))

# Train a decision tree, with set max depth
# Recursive algorithm
def train_dtree(data, depth):
    # Base cases
    # All data has same class:
    city = data[0][0]
    all_same_class = True
    for row in data:
        if row[0] == city: continue
        else: all_same_class = False
    if all_same_class:
        return {'val': city, 'pos': None, 'neg': None}
    # Bottom of tree (choose most-likely case)
    if depth == 0:
        return {'val': sorted([[len(list(filter(lambda x: x[0] == c, data))), c] for c in classes], reverse=True)[0][1], 'pos': None, 'neg': None}

    # Count word occurances in the data
    word_counts = {}
    for row in data:
        for word in row[1]:
            if word not in word_counts.keys():
                word_counts[word] = 0
            word_counts[word] += 1
    min_entropy = float('inf')
    min_word = None
    word_counts = dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:100])
    # Find word-split that minimizes entropy
    for word in word_counts:
        data_pos = list(filter(lambda x: word in x[1], data))
        data_neg = list(filter(lambda x: word not in x[1], data))
        if len(data_pos) == 0 or len(data_neg) == 0: continue
        entropy = split_entropy(word, data_pos, data_neg)
        if entropy < min_entropy:
            min_entropy, min_word = entropy, word

    # Build tree based on the min_word split
    data_pos = list(filter(lambda x: min_word in x[1], data))
    data_neg = list(filter(lambda x: min_word not in x[1], data))
    return {'val': min_word, 'pos': train_dtree(data_pos, depth-1), 'neg': train_dtree(data_neg, depth-1)}

# Traverse decision tree (for the words in a given tweet)
def traverse_dtree(tree, words):
    if not tree['pos'] and not tree['neg']: return tree['val']
    if tree['val'] in words: return traverse_dtree(tree['pos'], words)
    else: return traverse_dtree(tree['neg'], words)

# Test a decision tree classifier
def test_dtree(model, data):
    estimates = []
    num_correct = 0
    for row in data:
        prediction = traverse_dtree(model, row[1])
        if prediction == row[0]: num_correct += 1
        estimates.append(prediction)
    print("Accuracy: {}".format(num_correct / len(data)))
    return estimates

# Parse input data then train a model
def train_model(type, training_input):
    data = None
    with open(training_input, 'r') as f:
        raw = f.read()
        data = parse_data(raw)
    if type == "bayes":
        model = train_bayes(data)
        bayes_top_5(model)
        return model
    elif type == "dtree":
        model = train_dtree(data, 10)
        print(dtree_to_string(model))
        return model

# Test model on new data
def test_model(type, model_input, testing_input):
    model, raw, data, estimates = None, None, None, None
    with open(model_input, 'r') as f:
        model = json.load(f)
    with open(testing_input, 'r') as f:
        raw = f.read()
        data = parse_data(raw)
    if type == "bayes":
        estimates = test_bayes(model, data)
    elif type == "dtree":
        estimates = test_dtree(model, data)
    results = ""
    for i in range(len(estimates)):
        results += estimates[i] + ' ' + raw.splitlines()[i] + '\n'
    return results

def main():
    args = get_args()
    if args.mode == 'train':
        model = train_model(args.type, args.training_input)
        with open(args.model_output, 'w') as f:
            json.dump(model, f)
    elif args.mode == 'test':
        results = test_model(args.type, args.model_input, args.testing_input)
        with open(args.testing_output, 'w') as f:
            f.write(results)
            f.close()

if __name__ == "__main__":
    main()
