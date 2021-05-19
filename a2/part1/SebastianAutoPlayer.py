# Automatic Sebastian game player
# B551 Fall 2020
# Alex Fuerst (alfuerst), Andrew Corum (amcorum), Kaitlynne Wilkerson (kwilker)
#
# Based on skeleton code by D. Crandall
#
#
# This is the file you should modify to create your new smart player.
# The main program calls this program three times for each turn. 
#   1. First it calls first_roll, passing in a Dice object which records the
# result of the first roll (state of 5 dice) and current Scorecard.
# You should implement this method so that it returns a (0-based) list 
# of dice indices that should be re-rolled.
#   
#   2. It then re-rolls the specified dice, and calls second_roll, with
# the new state of the dice and scorecard. This method should also return
# a list of dice indices that should be re-rolled.
#
#   3. Finally it calls third_roll, with the final state of the dice.
# This function should return the name of a scorecard category that 
# this roll should be recorded under. The names of the scorecard entries
# are given in Scorecard.Categories.
#
from itertools import combinations
from copy import copy
from collections import defaultdict
from SebastianState import Dice
from SebastianState import Scorecard
from SebSearchTree import SebSearchTreeNode
import random
import heapq
import yahtzee_expectimax

enumd_num_cats = list(enumerate(["primis", "secundus", "tertium", "quartus", "quintus", "sextus"], start=1))
company_set = set([1, 2, 3, 4, 5])
dice_num_set = set([0,1,2,3,4])

def get_dice_filling_categories(roll, cats_to_fill):
  pre_enumerated = list(enumerate(roll.dice))
  ret = {}
  for n, num_cat in enumd_num_cats:
    if num_cat in cats_to_fill:
      ret[num_cat] = [i for i, v in pre_enumerated if v == n]
  if "company" in cats_to_fill:
    found_set = set()
    ret["company"] = []
    for i, v in pre_enumerated:
      if v in company_set and v not in found_set:
        found_set.add(v)
        ret["company"].append(i)
  if "pandemonium" in cats_to_fill:
    ret["pandemonium"] = []
    for i, v in pre_enumerated:
      # expect a better value on a re-roll when v < 4
      # only re-roll lesser dice
      if v >= 4:
        ret["pandemonium"].append(i)

  if "prattle" in cats_to_fill:
    ret["prattle"] = []

  counts = [roll.dice.count(i) for i in range(1, 7)]

  if "quintuplicatam" in cats_to_fill:
    mx = max(counts)
    y = list(enumerate(counts))
    y.reverse()
    # search from back to find count with maximum value if two are equal
    for i, v in y:
      if v == mx:
        loc = i + 1
        break
    ret["quintuplicatam"] = []
    for i, v in pre_enumerated:
      # reroll every dice that doens't fit with grouping
      if v == loc:
        ret["quintuplicatam"].append(i)

  if "quadrupla" in cats_to_fill:
    ret["quadrupla"] = []
    mx = max(counts)
    if mx == 5:
      loc = counts.index(mx)
      if loc < 4:
        # we have an unnecessary die, reroll one for hopefully a better score
        ret["quadrupla"] = [0, 1, 2, 3]
      else:
        ret["quadrupla"] = [0, 1, 2, 3, 4]
    elif mx == 4:
      loc = counts.index(mx) +1
      for i, v in pre_enumerated:
        # reroll the one die that doens't fit with grouping
        if v > 4 or v == loc:
          ret["quadrupla"].append(i)
    else:
      y = list(enumerate(counts))
      y.reverse()
      # search from back to find count with maximum value if two are equal
      for i, v in y:
        if v == mx:
          loc = i + 1
          break

      for i, v in pre_enumerated:
        # reroll every dice that doens't fit with grouping
        if v == loc:
          ret["quadrupla"].append(i)

  if "triplex" in cats_to_fill:
    ret["triplex"] = []
    mx = max(counts)
    if mx >= 3:
      loc = counts.index(mx)
      for i, v in pre_enumerated:
        if v == loc +1:
          ret["triplex"].append(i)
          if len(ret["triplex"]) >= 3:
            break
      for i, v in pre_enumerated:
        if v > 4 and i not in ret["triplex"]:
            ret["triplex"].append(i)
    else:
      y = list(enumerate(counts))
      y.reverse()
      # search from back to find count with maximum value if two are equal
      for i, v in y:
        if v == mx:
          loc = i + 1
          break

      for i, v in pre_enumerated:
        # reroll every dice that doens't fit with grouping
        if v == loc:
          ret["triplex"].append(i)
  
  if "squadron" in cats_to_fill:
    if (2 in counts) and (3 in counts):
      ret["squadron"] = [1, 2, 3, 4, 5]
    else:
      best, second, = sorted(counts, reverse=True)[:2]
      best_loc = counts.index(best) + 1
      if best == second:
        second_loc = counts.index(second, best_loc) + 1
      else:
        second_loc = counts.index(second) + 1
      if best == 5:
        ret["squadron"] = [1, 2, 3]
      else:
        ret["squadron"] = []
        best = 0
        for i, v in pre_enumerated:
          if v == best_loc and best < 3:
            best += 1
            ret["squadron"].append(i)
          elif v == second_loc:
            ret["squadron"].append(i)
  if len(ret) != len(cats_to_fill):
    raise Exception("Did not add enough category counts given num to fill")
  return ret

class DiceIterator:

  def __init__(self, roll, dice_to_reroll):
    if isinstance(roll, Dice):
      self.dice = roll.dice
    else:
      self.dice = roll
    self.dice_to_reroll = dice_to_reroll

  def __iter__(self):
      self.curr_dice_pos = 0
      self.dice_val = 1
      return self

  def __next__(self):
    if len(self.dice_to_reroll) <= 0:
      self.dice_val = 999
      self.curr_dice_pos = 0

    if self.dice_val > 6:
      self.dice_val = 1
      self.curr_dice_pos += 1
      if self.curr_dice_pos >= len(self.dice_to_reroll):
        raise StopIteration()
    new_dice = self.dice[:]

    to_reroll = self.dice_to_reroll[self.curr_dice_pos]
    new_dice[to_reroll] = self.dice_val
    self.dice_val += 1
    return new_dice

class SebastianAutoPlayer:
  dice_nums = [i for i in range(0, 5)]

  def __init__(self):
    pass

  def choose_best_reroll(self, roll, scorecard):
    _, curr_best_score = self.choose_best_score(roll, scorecard)
    best_reroll = []
    poss_rolls = defaultdict(list)
    total_combs = 0
    for r in range(1, 5):
      for comb in combinations(self.dice_nums, r):
        chance = (1 / 6) ** len(comb)
        score_sum = 0
        for reroll in DiceIterator(roll, comb):
          _, score = self.choose_best_score(reroll, scorecard)
          score_sum += score

        if score_sum * chance > curr_best_score:
          curr_best_score = score * chance
          best_reroll = comb
    return best_reroll

  def roll_children_comb(self, root: SebSearchTreeNode, with_roll):
      for reroll in DiceIterator(root.roll, with_roll):
        chd = SebSearchTreeNode(
            root, root.roll, root.scorecard, with_roll)
        yield chd 

  def roll_children(self, root: SebSearchTreeNode):
    for r in range(1, 6):
        for comb in combinations(self.dice_nums, r):
          for child in self.roll_children_comb(root, comb):
            yield child

  def expand_tree(self, root, num_rerolls, num_turns, cats):
    if num_turns < 0:
      # bottomed out
      return
    dct = get_dice_filling_categories(root.roll, cats)
    sorted_categories = sorted(dct.items(), key=lambda x: len(x[1]), reverse=True)

    if num_rerolls == 0 and num_turns >= 0:
      # assign scores and possibly search next turn
      for cat, _ in sorted_categories[:3]:
        chd = SebSearchTreeNode(
            root, root.roll, root.scorecard, [])
        chd.score_category(cat)
        root.add_child(chd)
        cpy = cats.copy()
        cpy.remove(cat)
        self.expand_tree(chd, num_rerolls=2, num_turns=num_turns - 1, cats=cpy)
      return

    # search reroll space
    curr_score = root.scorecard.totalscore
    to_explore = sorted_categories[:3]
    for cat, involved in to_explore:
      to_reroll = dice_num_set - set(involved)
      for child in self.roll_children_comb(root, sorted(list(to_reroll))):
        root.add_child(child)
        self.expand_tree(child, num_rerolls-1, num_turns, cats=cats)

  def get_max(self, root):
    if len(root.children) == 0:  # leaf
      if root.new_cat:
        return root.scorecard.totalscore, root
      else:  # expected value
        return root.scorecard.totalscore * root.prob, root

    if root.children[0].new_cat:  # max layer
      mx = 0
      mx_node = None
      for child in root.children:
        score, _ = self.get_max(child)
        if score > mx:
          mx = score
          mx_node = child
      return mx, mx_node
    else:  # chance layer
      mx = 0
      mx_node = None
      for child in root.children:
        score = self.get_avg(child)
        print(score)
        if score > mx:
          mx = score
          mx_node = child
      return mx, mx_node

  def get_avg(self, root):
    sumExp = 0
    if len(root.children) == 0:
      expectVal = root.scorecard.totalscore * root.prob
      return expectVal, root 
    if root.children[0].new_cat:
      for child in root.children:
        score, _ = self.get_max(child)
        expectVal = score * child.prob
        sumExp += expectVal
      return sumExp / len(root.children)
    else: 
      for child in root.children:
        score = self.get_avg(child)
        expectVal = score * child.prob
        sumExp += expectVal
      return sumExp / len(root.children)

  def first_roll(self, roll, scorecard):
    remaining_cats = list(set(Scorecard.Categories) - set(scorecard.scorecard.keys()))
    score, reroll = yahtzee_expectimax.search_max(
        roll.dice, cats_left=remaining_cats, depth=2, bonus=scorecard.bonusflag, curr_scores=scorecard.scorecard, times_choose_cat=1)
    return reroll

    remaining_cats = list(set(Scorecard.Categories) - set(scorecard.scorecard.keys()))
    root = SebSearchTreeNode(None, roll, scorecard, [])
    self.expand_tree(root, num_rerolls=2, num_turns=0, cats=remaining_cats)
    score, best_node = self.get_max(root)
    return best_node.rerolled

  def second_roll(self, roll, scorecard):
    remaining_cats = list(set(Scorecard.Categories) - set(scorecard.scorecard.keys()))
    score, reroll = yahtzee_expectimax.search_max(roll.dice, cats_left=remaining_cats, depth=1, bonus=scorecard.bonusflag, curr_scores=scorecard.scorecard, times_choose_cat=2)
    return reroll

    remaining_cats = list(set(Scorecard.Categories) - set(scorecard.scorecard.keys()))
    root = SebSearchTreeNode(None, roll, scorecard, [])
    self.expand_tree(root, num_rerolls=1, num_turns=0, cats=remaining_cats)
    score, best_node = self.get_max(root)
    return best_node.rerolled
        
  def third_roll(self, roll, scorecard):
    remaining_cats = list(set(Scorecard.Categories) - set(scorecard.scorecard.keys()))
    score, cat = yahtzee_expectimax.search_categories(roll.dice, remaining_cats, depth=0, bonus=scorecard.bonusflag, curr_scores=scorecard.scorecard, times_choose_cat=2)
    return cat


    remaining_cats = list(set(Scorecard.Categories) - set(scorecard.scorecard.keys()))
    root = SebSearchTreeNode(None, roll, scorecard, [])
    self.expand_tree(root, num_rerolls=0, num_turns=1, cats=remaining_cats)
    score, best_node = self.get_max(root)
    return best_node.category

  def choose_best_score(self, roll, scorecard):
    remaining_categories = list(set(Scorecard.Categories) - set(scorecard.scorecard.keys()))
    cat = remaining_categories[0]
    score = 0
    for category in remaining_categories:
      test_score = self.calc_score(roll, scorecard, category)
      if test_score > score:
        score = test_score
        cat = category

    return cat, score

  def calc_score(self, roll, scorecard, category):
    if category in scorecard.scorecard:
      return scorecard.totalscore
      
    scored_categories = scorecard.scorecard
    if isinstance(roll, Dice):
      dice = roll.dice
    else:
      dice = roll
    counts = [dice.count(i) for i in range(1,7)]
    if category in Scorecard.Numbers:
      score = counts[Scorecard.Numbers[category]-1] * Scorecard.Numbers[category]
    elif category == "company":
      score = 40 if sorted(dice) == [1,2,3,4,5] else 0
    elif category == "prattle":
      score = 30 if (len(set([1,2,3,4]) - set(dice)) == 0 or len(set([2,3,4,5]) - set(dice)) == 0 or len(set([3,4,5,6]) - set(dice)) == 0) else 0
    elif category == "squadron":
      score = 25 if (2 in counts) and (3 in counts) else 0
    elif category == "triplex":
      score = sum(dice) if max(counts) >= 3 else 0
    elif category == "quadrupla":
      score = sum(dice) if max(counts) >= 4 else 0
    elif category == "quintuplicatam":
      score = 50 if max(counts) == 5 else 0
    elif category == "pandemonium":
      score = sum(dice)
    else:
      print("Error: unknown category")

    if not scorecard.bonusflag and len(set(Scorecard.Numbers.keys()) - set(scored_categories.keys())) == 0:
        bonusscore = 35 if sum(
            [scored_categories[i] for i in Scorecard.Numbers]) >= 63 else 0
        score += bonusscore

    return score + scorecard.totalscore

def timer(d):
  d.roll()
  get_dice_filling_categories(d, set(Scorecard.Categories))

if __name__ == "__main__":
  # import cProfile
  #import timeit
  d = Dice()
  s = Scorecard()
  ap = SebastianAutoPlayer()
  d.roll()
  d.dice = [3, 3, 5, 4, 3]
  for i in range(10):
    d.roll()
    print(d)
    which_to_reroll = ap.first_roll(d, s)
    print(which_to_reroll)
  which_to_reroll = ap.third_roll(d, s)
  print(which_to_reroll)
