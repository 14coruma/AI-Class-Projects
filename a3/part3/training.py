#!/usr/bin/python
#
# Authors: Alex Fuerst
#

from PIL import Image
import pandas as pd
import pickle, os
from math import log
from collections import Counter, defaultdict

import vit

CHARACTER_WIDTH = 14
CHARACTER_HEIGHT = 25
TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
let_set = set([c for c in TRAIN_LETTERS])

def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [["".join(['*' if px[x, y] < 1 else ' ' for x in range(
            x_beg, x_beg+CHARACTER_WIDTH)]) for y in range(0, CHARACTER_HEIGHT)], ]
    return result

def load_training_letters(fname):
    letter_images = load_letters(fname)
    return {TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS))}

def train_hmm(train_txt_fnames):
  counts = {}
  char_cts = {}
  start_cts = {}

  if os.path.exists("__pycache__/counts"):
    print("loading hmm from cache")
    with open("__pycache__/counts", "r+b") as f:
      counts = pickle.load(f)
    with open("__pycache__/char_cts", "r+b") as f:
      char_cts = pickle.load(f)
    with open("__pycache__/start_cts", "r+b") as f:
      start_cts = pickle.load(f)
  else:
    print("training hmm")
    for c1 in TRAIN_LETTERS:
        counts[c1] = [0]*len(TRAIN_LETTERS)
        char_cts[c1] = 0
        start_cts[c1] = 0
    bad = 0
    cnt = 0
    bad_char = set()
    for train_txt_fname in train_txt_fnames:
      with open(train_txt_fname, "r") as f:
        for line in f.readlines():
          # line = " ".join(line.strip().replace("`", "'").split()[0::2])
          if line[0] in TRAIN_LETTERS:
            start_cts[line[0]] += 1
          for i in range(0, len(line)-1):
            if line[i] not in TRAIN_LETTERS:
              bad += 1
              bad_char.add(line[i])
              continue
            if line[i+1] not in TRAIN_LETTERS:
              bad += 1
              bad_char.add(line[i+1])
              continue
            cnt += 1
            char_cts[line[i]] += 1
            counts[line[i+1]][TRAIN_LETTERS.index(line[i])] += 1

    with open("__pycache__/counts", "w+b") as f:
      pickle.dump(counts, f)
    with open("__pycache__/char_cts", "w+b") as f:
      pickle.dump(char_cts, f)
    with open("__pycache__/start_cts", "w+b") as f:
      pickle.dump(start_cts, f)

  df = pd.DataFrame.from_dict(counts, orient="index", columns=[
                              c for c in TRAIN_LETTERS])
  df = df / df.sum(axis=0)
  df.fillna(0, inplace=True)

  char_df = pd.Series(char_cts.values(), char_cts.keys())
  char_df = char_df / char_df.sum()

  start_df = pd.Series(start_cts.values(), start_cts.keys())
  start_df = start_df / start_df.sum()

  return df, char_df, start_df


def train_simple_bayes(train_img_fname):
  trained_image = []
  train_letters = load_training_letters(train_img_fname)

  for h in range(CHARACTER_HEIGHT):
    trained_image.append([])
    for w in range(CHARACTER_WIDTH):
      trained_image[h].append(set())

  for char, image in train_letters.items():
    for h in range(CHARACTER_HEIGHT):
      for w in range(CHARACTER_WIDTH):
        if image[h][w] == "*":
          trained_image[h][w].add(char)
  return trained_image

memory = {}


def transition_from(state_i, state_j, trans_df, char_df, start_df):
  if state_i is None:
    if start_df[state_j] == 0:
      return 0
    return - log(start_df[state_j])
  # print(state_i, "->", state_j, "=", trans_df[state_j][state_i])
  if trans_df[state_j][state_i] == 0:
    return 0
  return - log(trans_df[state_j][state_i])


def probability(state_j, time_t_plus, trans_df, char_df, start_df, times, memory, trained_image):
  if memory[state_j][time_t_plus] != -1:
    # print(state_j, time_t_plus, "cached")
    return memory[state_j][time_t_plus]
  # print(state_j, time_t_plus, "compute")

  if time_t_plus == 0:
    p_i_j = transition_from(None, state_j, trans_df, char_df, start_df)
    e_j = prob_infer_image(trained_image, times[time_t_plus], state_j)
    # p_i_j = 1
    p = e_j + p_i_j
    if p != 0:
      p = - log(p)
    memory[state_j][time_t_plus] = p
    return p

  m = float('inf')
  mc = ''
  for state_i in TRAIN_LETTERS:
    p_i_j = transition_from(state_i, state_j, trans_df, char_df, start_df)
    # p_i_j = 1
    v_i = probability(state_i, time_t_plus-1, trans_df, char_df, start_df, times, memory, trained_image)
    if m > p_i_j + v_i:
      m = p_i_j + v_i
      mc = state_i
  # m = 1
  e_j = prob_infer_image(trained_image, times[time_t_plus], state_j)
  # print(state_j, e_j)
  p = m + e_j
  if p != 0:
    p = - log(p)
  memory[state_j][time_t_plus] = p
  return p


def hmm_infer_whole(images, trained_image, trans_df, char_df, start_df):
  return vit.infer_hmm(images, trained_image, trans_df, char_df, start_df)

  for c in TRAIN_LETTERS:
    memory[c] = [-1 for _ in range(len(images))]
  for state_j in TRAIN_LETTERS:
    probability(state_j, len(images)-1, trans_df,
                char_df, start_df, images, memory, trained_image)
  for c, times in memory.items():
    print(c, times)
  msg = ""
  for i in range(len(images)):
    m = float('inf')
    mc = ''
    for c in TRAIN_LETTERS:
      if m > memory[c][i]:
        m = memory[c][i]
        mc = c
    msg += mc
  if len(msg) != len(images):
    raise Exception("Invalid prediction length", len(msg), len(images), msg)
  # for c, times in memory.items():
  #   print(c, times)
  return msg

m = 5

def prob_infer_image(bayes, img, char):
  global m
  maxes = []

  for h in range(CHARACTER_HEIGHT):
    for w in range(CHARACTER_WIDTH):
      if img[h][w] == "*" and char in bayes[h][w]:
        p = (100 - m) / 100
      elif char in let_set - bayes[h][w]:
        p = (100 - m) / 100
      else:
        p = m / 100
      maxes.append(p)
  p = maxes[0]
  for mx in maxes[1:]:
    p *= mx
  p = - log(p)
  # if p > 1:
  #   print(char, p)
  return p

def simple_infer_image(bayes, img):
  global m
  maxes = {}
  for c in TRAIN_LETTERS:
    maxes[c] = []

  for h in range(CHARACTER_HEIGHT):
    for w in range(CHARACTER_WIDTH):
      for char in TRAIN_LETTERS:
        if img[h][w] == "*":
          if char in bayes[h][w]:
            p = (100 - m) / 100
          else:
            p = m / 100
          maxes[char].append(p)
        else:
          if char in let_set - bayes[h][w]:
            p = (100 - m) / 100
          else:
            p = m / 100
          maxes[char].append(p)

  mc = "*"
  curr_m = float('inf')
  for c, ps in maxes.items():
    p = ps[0]
    for next_p in ps[1:]:
      p *= next_p
    p = - log(p)
    if p < curr_m:
      # print("REPLACE", c, p)
      curr_m = p
      mc = c
  return mc

if __name__ == "__main__":
  import sys
  (train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
  trained_image = train_simple_bayes(train_img_fname)
  trans_df, char_df, start_df = train_hmm([train_txt_fname])
  test_letters = load_letters(test_img_fname)
  train_letters = load_training_letters(train_img_fname)

  msg = ""
  for img in test_letters:
    c = simple_infer_image(trained_image, img)
    msg += c
    # break
  print("/",msg,"\\")
  # test_letters = test_letters[:5]
  # hmm_msg = hmm_infer_whole(test_letters, trained_image, trans_df, char_df, start_df)
  # print("/", hmm_msg, "\\")

  hmm_msg = vit.infer_hmm(test_letters, trained_image, trans_df, char_df, start_df)
  print("/", hmm_msg, "\\")
