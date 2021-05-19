from math import log

CHARACTER_WIDTH = 14
CHARACTER_HEIGHT = 25
TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
let_set = set([c for c in TRAIN_LETTERS])
graph = {}
m = 10


def transition_from(state_t, state_t_plus, trans_df, start_df):
  if state_t_plus is None:
    if start_df[state_t] == 0:
      return 0
    return - log(start_df[state_t])
  # print(state_t, "->", state_t_plus, "=", trans_df[state_t_plus][state_t])
  if trans_df[state_t_plus][state_t] == 0:
    return 0
  return - log(trans_df[state_t_plus][state_t])

def prob_infer_image(bayes, img, char):
  global m
  maxes = []

  for h in range(CHARACTER_HEIGHT):
    for w in range(CHARACTER_WIDTH):
      if img[h][w] == "*" and char in bayes[h][w]:
        p = (100 - m) / 100
      elif img[h][w] != "*" and char in let_set - bayes[h][w]:
        p = (100 - m) / 100
      else:
        p = m / 100
      maxes.append(p)
  p = maxes[0]
  for mx in maxes[1:]:
    p *= mx
  p = - log(p)
  return p


def start_cost(state_t, images, trans_df, start_df, trained_image):
    p = transition_from(state_t, None, trans_df, start_df)
    e_j = prob_infer_image(trained_image, images[0], state_t)
    graph[state_t][0] = p + e_j
    return p + e_j


def cost(state_t, images, time_t, trans_df, start_df, trained_image):
  if graph[state_t][time_t] != float('inf'):
    return graph[state_t][time_t]

  if time_t == 0:
    c = start_cost(state_t, images, trans_df, start_df, trained_image)
    graph[state_t][time_t] = c
    return c

  mx = float('inf')
  mc = ''
  e_j = prob_infer_image(trained_image, images[time_t], state_t)
  for char in TRAIN_LETTERS:
    prev_cost = cost(char, images, time_t-1, trans_df, start_df, trained_image)
    p = transition_from(char, state_t, trans_df, start_df)
    new_cost = prev_cost + p + e_j
    # print(char, new_cost)
    if new_cost < mx:
      mx = new_cost
      mc = char

  graph[state_t][time_t] = mx
  return mx

def infer_hmm(images, trained_image, trans_df, char_df, start_df):
  for c in TRAIN_LETTERS:
    graph[c] = [float('inf') for _ in range(len(images))]
  for c in TRAIN_LETTERS:
    _ = cost(c, images, len(images)-1, trans_df, start_df, trained_image)
  msg = ""
  for i in range(len(images)):
    m = float('inf')
    mc = ''
    for c in TRAIN_LETTERS:
      if m > graph[c][i]:
        m = graph[c][i]
        mc = c
    msg += mc
  if len(msg) != len(images):
    raise Exception("Invalid prediction length", len(msg), len(images), msg)
  # print(msg)
  return msg
  
# C("a"| <start>) => - log(P("a") + - log(P("a" | <image>))
# C("a"|"B") => - log(P("a"|"B")) + - log(P("a" | <image>))
