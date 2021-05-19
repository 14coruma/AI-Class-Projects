from itertools import combinations
from SebastianState import Scorecard
from numpy.random import randint

dice_nums = [i for i in range(0, 5)]

enumd_num_cats = list(enumerate(
    ["primis", "secundus", "tertium", "quartus", "quintus", "sextus"], start=1))
company_set = set([1, 2, 3, 4, 5])
dice_num_set = set([0, 1, 2, 3, 4])

optimize = {}

def get_dice_filling_categories(dice, cats_to_fill):
  pre_enumerated = list(enumerate(dice))
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

  counts = [dice.count(i) for i in range(1, 7)]

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
      loc = counts.index(mx) + 1
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
        if v == loc + 1:
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
      ret["squadron"] = [0,1,2,3,4]
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

def search_categories(dice, cats_left, depth=0, bonus=False, curr_scores=None, times_choose_cat=0):
    if depth == 0 and times_choose_cat <= 0:
      score, cat = best_score(dice, cats_left, bonus, curr_scores)
      return score, cat

    mx = 0
    mx_cat = ""
    have_score = []
    for cat in cats_left:
      _, _, test_score = score_roll(dice, curr_scores, cat, bonus)
      if test_score > 0:
        have_score.append(cat)
    if len(have_score) == 0:
      have_score = cats_left
    for cat in have_score:
      t = 0
      cpy = cats_left.copy()
      cpy.remove(cat)
      filled, bonus, orig_score = score_roll(dice, curr_scores, cat, bonus)
      if len(cpy) == 0:
        # only one category
        return orig_score, cat
      avg = 0
      iters = 50
      for i in range(iters):
        new_dice = list(randint(0, 7, 5))
        score, comb = search_max(new_dice, cpy.copy(), depth=2, bonus=bonus, curr_scores=filled.copy(), times_choose_cat=times_choose_cat - 1)
        avg += score
      new_score = orig_score + (avg / iters)
      if new_score >= mx:
        mx = new_score
        mx_cat = cat
    return mx, mx_cat

def search_max(dice, cats_left, depth=0, bonus=False, curr_scores=None, times_choose_cat=0): #, choose_roll=False, choose_cat=False):
  if len(cats_left) == 0:
    return 0, ""
  if depth == 0 and times_choose_cat == 0: # bottom
    score, cat = best_score(dice, cats_left, bonus, curr_scores)
    return score, ()

  if depth == 0:
    score, category = search_categories(
        dice, cats_left, depth=0, bonus=bonus, curr_scores=curr_scores, times_choose_cat=times_choose_cat - 1)
    return score, ()

  mx = 0.0
  mx_comb = tuple()
  dct = get_dice_filling_categories(dice, cats_left)
  sorted_categories = sorted(dct.items(), key=lambda x: len(x[1]), reverse=True)
  for cat, involved in sorted_categories:
    to_reroll = dice_num_set - set(involved)
    if len(to_reroll) == 0:
      # have set perfectly
      score, _ = best_score(dice, cats_left, bonus, curr_scores)
      return score, ()
    score = search_comb(dice, cats_left, to_reroll, depth-1,
                        bonus, curr_scores, times_choose_cat)
    if score > mx:
      mx = score
      mx_comb = to_reroll
  return mx, mx_comb


def search_comb(dice, cats_left, comb, depth=0, bonus=False, curr_scores=None, times_choose_cat=0):
  if depth == 0 or len(comb) == 0:
    score, cat = best_score(dice, cats_left, bonus, curr_scores)
    return score


  avg_sum = 0
  old_avg_sum = 0
  optimize_flag = True
  i = 1
  prob = (1/6) ** len(comb)
  t = str(comb)
  for die in comb:
    if t not in optimize.keys():
      optimize[t] = 0
      optimize_flag = False
    for i in range(1, 7):
      if optimize_flag == False:
        i += 1
        new_roll = dice[:]
        new_roll[die] = i
        score, _ = search_max(new_roll, cats_left, depth - 1, bonus, curr_scores, times_choose_cat=times_choose_cat)
        avg_sum += score
        if die == int(t[1]):
          optimize[t] = avg_sum
      elif optimize_flag == True:
        if die == int(t[1]):
          i += 1
          new_roll = dice[:]
          new_roll[die] = i
          score, _ = search_max(new_roll,   cats_left, depth - 1, bonus,  curr_scores,   times_choose_cat=times_choose_cat)
          avg_sum += score
          new_score = avg_sum
        else:
          if new_score > optimize[t]:
            optimize[t] = avg_sum
            i += 1
            new_roll = dice[:]
            new_roll[die] = i
            score, _ = search_max(new_roll,   cats_left, depth - 1, bonus,  curr_scores,   times_choose_cat=times_choose_cat)
            avg_sum += score
  return prob * avg_sum


scorecard_nums = set(Scorecard.Numbers.keys())


def best_score(dice, cats_left, bonus, curr_scores):
  counts = [dice.count(i) for i in range(1, 7)]
  score = 0
  chosen_cat = ""
  for cat in cats_left:
    if cat in Scorecard.Numbers:
      s = counts[Scorecard.Numbers[cat] - 1] * Scorecard.Numbers[cat]
      if counts[Scorecard.Numbers[cat] - 1] >= 3:
        return score + 35, cat
      if s >= score:
        score = s
        chosen_cat = cat
  if "company" in cats_left:
    s = 40 if sorted(dice) == [1, 2, 3, 4, 5] else 0
    if s >= score:
        score = s
        chosen_cat = "company"
  if "prattle" in cats_left:
    s = 30 if (len(set([1, 2, 3, 4]) - set(dice)) == 0 or len(set(
        [2, 3, 4, 5]) - set(dice)) == 0 or len(set([3, 4, 5, 6]) - set(dice)) == 0) else 0
    if s >= score:
        score = s
        chosen_cat = "prattle"
  if "squadron" in cats_left:
    s = 25 if (2 in counts) and (3 in counts) else 0
    if s >= score:
        score = s
        chosen_cat = "squadron"
  if "triplex" in cats_left:
    s = sum(dice) if max(counts) >= 3 else 0
    if s >= score:
        score = s
        chosen_cat = "triplex"
  if "quadrupla" in cats_left:
    s = sum(dice) if max(counts) >= 4 else 0
    if s >= score:
        score = s
        chosen_cat = "quadrupla"
  if "quintuplicatam" in cats_left:
    s = 50 if max(counts) == 5 else 0
    if s >= score:
      score = s
      chosen_cat = "quintuplicatam"
  if "pandemonium" in cats_left:
    s = sum(dice)
    # want at least double another score to avoid using pandemonium
    # or use if nothing else possible
    if score == 0 or s > score * 4:
      score = s
      chosen_cat = "pandemonium"

  if not bonus and len(scorecard_nums - set(curr_scores.keys())) == 0:
      bonusscore = 35 if sum(
          [curr_scores[i] for i in Scorecard.Numbers]) >= 63 else 0
      score += bonusscore

  if chosen_cat == "":
    chosen_cat = cats_left.pop()
  return score, chosen_cat


def score_roll(dice, filled_cats, category, bonus):
  filled_cats = filled_cats.copy()
  if category in filled_cats:
    raise Exception("cannot double fill a category")

  counts = [dice.count(i) for i in range(1, 7)]
  if category in Scorecard.Numbers:
    score = counts[Scorecard.Numbers[category]-1] * \
        Scorecard.Numbers[category]
  elif category == "company":
    score = 40 if sorted(dice) == [1, 2, 3, 4, 5] else 0
  elif category == "prattle":
    score = 30 if (len(set([1, 2, 3, 4]) - set(dice)) == 0 or len(set(
        [2, 3, 4, 5]) - set(dice)) == 0 or len(set([3, 4, 5, 6]) - set(dice)) == 0) else 0
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
  if not bonus and len(scorecard_nums - set(filled_cats.keys())) == 0:
      bonus = True
      bonusscore = 35 if sum(
          [filled_cats[i] for i in Scorecard.Numbers]) >= 63 else 0
      score += bonusscore
  filled_cats[category] = score
  return filled_cats, bonus, score
  
if __name__ == "__main__":
  d = list(randint(0, 7, 5))
  print(d)
  print(search_max(d, cats_left=set(Scorecard.Categories), depth=2, bonus=False, curr_scores={}, times_choose_cat=1))
