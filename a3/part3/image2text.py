#!/usr/bin/python
#
# Perform optical character recognition, usage:
#     python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png
# python3 ./image2text.py courier-train.png ../part1/bc.train test-2-0.png
#
# Authors: Alex Fuerst
# (based on skeleton code by D. Crandall, Oct 2020)
#

import sys
from training import train_hmm, train_simple_bayes, simple_infer_image, load_letters, load_training_letters, hmm_infer_whole
import urllib.request
import os

training_files = []
for url in ["https://www.gutenberg.org/files/84/84-0.txt", "http://www.gutenberg.org/cache/epub/345/pg345.txt", "https://www.gutenberg.org/files/1661/1661-0.txt"]:
  txt = urllib.request.urlopen(url)
  pth = url.split("/")[-1]
  if not os.path.exists(pth):
    training_files.append(url.split("/")[-1])
    with open(url.split("/")[-1], 'w') as f:
        f.write(txt.read().decode('utf-8'))

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]

trained_image = train_simple_bayes(train_img_fname)

trans_df, char_df, start_df = train_hmm(training_files)
test_letters = load_letters(test_img_fname)
train_letters = load_training_letters(train_img_fname)

for char, img in train_letters.items():
  inference = simple_infer_image(trained_image, img)
  if inference != char:
    print("ERROR: inferred:", inference, " vs expexted:", char)

simple_msg = ""
for img in test_letters:
  c = simple_infer_image(trained_image, img)
  simple_msg += c

hmm_msg = ""
hmm_msg = hmm_infer_whole(test_letters, trained_image, trans_df, char_df, start_df)

# The final two lines of your output should look something like this:
print("Simple: ", simple_msg)
print("   HMM: ", hmm_msg)
