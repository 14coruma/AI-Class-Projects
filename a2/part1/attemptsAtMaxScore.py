### Attempts at maximizing the score ###
# None of these really worked; actually lowered average score

############################################
### Attempt 1 @ changing score_roll
###########################################
def score_roll(dice, filled_cats, category, bonus):
  """
  Trying to prioritize numbered die
  """
  filled_cats = filled_cats.copy()
  if category in filled_cats:
    raise Exception("cannot double fill a category")
  #print(category)
  counts = [dice.count(i) for i in range(1, 7)]
  print(counts)
  if 6 in counts: 
    place = counts.index(6)
    #print(place)
    #print("FOUND A 6")
    if category in Scorecard.Numbers:
      if place == 0 and category == 'Primis':
        print("Placed Primis")
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
      elif place == 1 and category == 'Secundus':
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
      elif place == 2 and category == 'Tertium':
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
      elif place == 3 and category == 'Quartus':
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
      elif place == 4 and category == 'Quintus':
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
      elif place == 5 and category == 'Sextus':
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
  elif 5 in counts:
    #print("FOUND A 5")
    if category in Scorecard.Numbers:
      place = counts.index(5)
    #print(place)
    #print("FOUND A 6")
    if category in Scorecard.Numbers:
      if place == 0 and category == 'Primis':
        print("Placed Primis")
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
      elif place == 1 and category == 'Secundus':
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
      elif place == 2 and category == 'Tertium':
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
      elif place == 3 and category == 'Quartus':
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
      elif place == 4 and category == 'Quintus':
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
      elif place == 5 and category == 'Sextus':
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
      #score = counts[Scorecard.Numbers[category]-1] * \
        #Scorecard.Numbers[category]
  elif 4 in counts:
    #print("FOUND A 4")
    if category in Scorecard.Numbers:
      place = counts.index(4)
    #print(place)
    #print("FOUND A 6")
    if category in Scorecard.Numbers:
      if place == 0 and category == 'Primis':
        print("Placed Primis")
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
      elif place == 1 and category == 'Secundus':
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
      elif place == 2 and category == 'Tertium':
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
      elif place == 3 and category == 'Quartus':
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
      elif place == 4 and category == 'Quintus':
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
      elif place == 5 and category == 'Sextus':
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
  elif 3 in counts:
    place = counts.index(3)
    if category in Scorecard.Numbers:
      if place == 0 and category == 'primis':
        print("Placed Primis")
        score = 3
      elif place == 1 and category == 'secundus':
        print("Placed Secundus")
        score = 2*3
      elif place == 2 and category == 'tertium':
        print("Placed Tertium")
        score = 3*3
      elif place == 3 and category == 'quartus':
        print("Placed Quartus")
        score = 4*3
        #score = counts[Scorecard.Numbers[category]-1] * \
        #  Scorecard.Numbers[category]
      elif place == 4 and category == 'quintus':
        print("Placed Quintus")
        score = 5*3
      elif place == 5 and category == 'sextus':
        print("Placed Sextus")
        score = 6*3
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

############################################
### Attempt 2 @ changing score_rolls
############################################
  """
  Another way of formatting ranking numbers above all other categories
  """
  
  if 6 in counts: 
    place = counts.index(6)
    if category in Scorecard.Numbers:
      if place == 0 and category == 'Primis':
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
      elif place == 1 and category == 'Secundus':
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
      elif place == 2 and category == 'Tertium':
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
      elif place == 3 and category == 'Quartus':
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
      elif place == 4 and category == 'Quintus':
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
      elif place == 5 and category == 'Sextus':
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
  elif 5 in counts:
    if category in Scorecard.Numbers:
      place = counts.index(5)
    if category in Scorecard.Numbers:
      if place == 0 and category == 'Primis':
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
      elif place == 1 and category == 'Secundus':
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
      elif place == 2 and category == 'Tertium':
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
      elif place == 3 and category == 'Quartus':
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
      elif place == 4 and category == 'Quintus':
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
      elif place == 5 and category == 'Sextus':
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
  elif 4 in counts:
    if category in Scorecard.Numbers:
      place = counts.index(4)
    if category in Scorecard.Numbers:
      if place == 0 and category == 'Primis':
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
      elif place == 1 and category == 'Secundus':
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
      elif place == 2 and category == 'Tertium':
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
      elif place == 3 and category == 'Quartus':
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
      elif place == 4 and category == 'Quintus':
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
      elif place == 5 and category == 'Sextus':
        score = counts[Scorecard.Numbers[category]-1] * \
          Scorecard.Numbers[category]
  elif 3 in counts:
    place = counts.index(3)
    if category in Scorecard.Numbers:
      if place == 0 and category == 'primis':
        print("Placed Primis")
        score = 3
      elif place == 1 and category == 'secundus':
        score = 2*3
      elif place == 2 and category == 'tertium':
        score = 3*3
      elif place == 3 and category == 'quartus':
        score = 4*3
      elif place == 4 and category == 'quintus':
        score = 5*3
      elif place == 5 and category == 'sextus':
        score = 6*3

############################################
### Attempt 3 @ changing score_rolls
############################################
  """
  Idea here is to rank categories based on how much they could provide to total score -> this idea might work out but I think I formatted it incorrectly 
  """
  score = 0
  if category == "company":
    score = 40 if sorted(dice) == [1, 2, 3, 4, 5] else 0
  elif 5 in counts: 
    if category == "quintuplicatam":
      score = 50 if max(counts) == 5 else 0
    elif category in Scorecard.Numbers:
      place = counts.index(5)
      if place == 0 and category == 'Primis':
        score = 5
      elif place == 1 and category == 'Secundus':
        score = 5*2
      elif place == 2 and category == 'Tertium':
        score = 5*3
      elif place == 3 and category == 'Quartus':
        score = 5*4
      elif place == 4 and category == 'Quintus':
        score = 5*5
      elif place == 5 and category == 'Sextus':
        score = 5*6
    elif category == "pandemonium":
      score = sum(dice)
  elif category == "prattle":
    score = 30 if (len(set([1, 2, 3, 4]) - set(dice)) == 0 or len(set(
        [2, 3, 4, 5]) - set(dice)) == 0 or len(set([3, 4, 5, 6]) - set(dice)) == 0) else 0
  elif 4 in counts:
    if category == "quadrupla":
      score = sum(dice) if max(counts) >= 4 else 0
    elif category in Scorecard.Numbers:
      place = counts.index(4)
      if place == 0 and category == 'Primis':
        score = 4
      elif place == 1 and category == 'Secundus':
        score = 4*2
      elif place == 2 and category == 'Tertium':
        score = 4*3
      elif place == 3 and category == 'Quartus':
        score = 4*4
      elif place == 4 and category == 'Quintus':
        score = 4*5
      elif place == 5 and category == 'Sextus':
        score = 4*6
    elif category == "pandemonium":
      score = sum(dice)
  elif 3 in counts:
    place = counts.index(3)
    if category in Scorecard.Numbers:
      if place == 0 and category == 'primis':
        score = 3
      elif place == 1 and category == 'secundus':
        score = 2*3
      elif place == 2 and category == 'tertium':
        score = 3*3
      elif place == 3 and category == 'quartus':
        score = 4*3
      elif place == 4 and category == 'quintus':
        score = 5*3
      elif place == 5 and category == 'sextus':
        score = 6*3
    elif category == "triplex":
      score = sum(dice) if max(counts) >= 3 else 0
    if 2 in counts:
      if category == "squadron":
        score = 25 if (2 in counts) and (3 in counts) else 0
    elif category == "pandemonium":
      score = sum(dice)
  else:
    print("Error: unknown category")

###########################################
###Attempt 1 @ changing best_score
###########################################

scorecard_nums = set(Scorecard.Numbers.keys())
def best_score(dice, cats_left, bonus, curr_scores):
  """
  Idea here was to prioritize the numbered die
  """
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
  if "prattle"  in cats_left:
    s = 30 if (len(set([1, 2, 3, 4]) - set(dice)) == 0 or len(set(
        [2, 3, 4, 5]) - set(dice)) == 0 or len(set([3, 4, 5, 6]) - set(dice)) == 0) else 0
    if s >= score:
        score = s
        chosen_cat = "prattle"
  if "squadron"  in cats_left:
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

  # print(score, chosen_cat)
  if chosen_cat == "":
    chosen_cat = cats_left.pop()
  return score, chosen_cat

#############################################
#Attempt 2 @ changing best_score
#############################################
  """
  Same idea as above but formatted a different way
  """
  numbers_flag = False
  flag6 = False
  flag5 = False
  flag4 = False
  flag3 = False
  op = [3,4,5,6]
  for i in counts:
    if 3 in counts: 
      flag3 = True
      numbers_flag = True
    if 4 in counts:
      flag4 = True
      numbers_flag = True
    if 5 in counts:
      flag5 = True
      numbers_flag = True
    if 6 in counts:
      flag6 = True
      numbers_flag = True
  score = 0
  s = 0
  chosen_cat = ""
  print(counts)
  if numbers_flag:
    for cat in cats_left:
      if cat in Scorecard.Numbers:
        if flag6:
          place = counts.index(6)
          if cat == 'primis' and place == 0:
            score = 6
            print("**3 primis**")
            chosen_cat = 'primis'
          elif cat == 'secundus' and place == 1:
            score = 6*2
            print("**3 secundus**")
            chosen_cat = 'secundus'
          elif cat == 'tertium'and place == 2:
            score = 6*3
            print("**3 tertium**")
            chosen_cat = 'tertium'
          elif cat == 'quartus'and place == 3:
            score = 6*4
            print("**3 quartus**")
            chosen_cat = 'quartus'
          elif cat == 'quintus'and place == 4:
            score = 6*5
            print("**3 quintus**")
            chosen_cat = 'quintus'
          elif cat == 'sextus'and place == 5:
            score = 6*6
            print("**3 sextus**")
            chosen_cat = 'sextus'
        elif flag5:
          place = counts.index(5)
          if cat == 'primis' and place == 0:
            score = 5
            print("**3 primis**")
            chosen_cat = 'primis'
          elif cat == 'secundus' and place == 1:
            score = 5*2
            print("**3 secundus**")
            chosen_cat = 'secundus'
          elif cat == 'tertium'and place == 2:
            score = 5*3
            print("**3 tertium**")
            chosen_cat = 'tertium'
          elif cat == 'quartus'and place == 3:
            score = 5*4
            print("**3 quartus**")
            chosen_cat = 'quartus'
          elif cat == 'quintus'and place == 4:
            score = 5*5
            print("**3 quintus**")
            chosen_cat = 'quintus'
          elif cat == 'sextus'and place == 5:
            score = 5*6
            print("**3 sextus**")
            chosen_cat = 'sextus'
        elif flag4:
          place = counts.index(4)
          if cat == 'primis' and place == 0:
            score = 4
            print("**3 primis**")
            chosen_cat = 'primis'
          elif cat == 'secundus' and place == 1:
            score = 4*2
            print("**3 secundus**")
            chosen_cat = 'secundus'
          elif cat == 'tertium'and place == 2:
            score = 4*3
            print("**3 tertium**")
            chosen_cat = 'tertium'
          elif cat == 'quartus'and place == 3:
            score = 4*4
            print("**3 quartus**")
            chosen_cat = 'quartus'
          elif cat == 'quintus'and place == 4:
            score = 4*5
            print("**3 quintus**")
            chosen_cat = 'quintus'
          elif cat == 'sextus'and place == 5:
            score = 4*6
            print("**3 sextus**")
            chosen_cat = 'sextus'
        elif flag3:
          place = counts.index(3)
          if cat == 'primis' and place == 0:
            score = 3
            print("**3 primis**")
            chosen_cat = 'primis'
          elif cat == 'secundus' and place == 1:
            score = 3*2
            print("**3 secundus**")
            chosen_cat = 'secundus'
          elif cat == 'tertium'and place == 2:
            score = 3*3
            print("**3 tertium**")
            chosen_cat = 'tertium'
          elif cat == 'quartus'and place == 3:
            score = 3*4
            print("**3 quartus**")
            chosen_cat = 'quartus'
          elif cat == 'quintus'and place == 4:
            score = 3*5
            print("**3 quintus**")
            chosen_cat = 'quintus'
          elif cat == 'sextus'and place == 5:
            score = 3*6
            print("**3 sextus**")
            chosen_cat = 'sextus'
        else: 
          s = counts[Scorecard.Numbers[cat] - 1] * Scorecard.Numbers[cat]
        if counts[Scorecard.Numbers[cat] - 1] >= 63:
          return score + 35, cat
    return score, chosen_cat
      #if s >= score:
      #  score = s
      #  print("SCORE")
      #  print(score)
        #chosen_cat = cat
  else:
    if "company" in cats_left:
      s = 40 if sorted(dice) == [1, 2, 3, 4, 5] else 0
      if s >= score:
        score = s
        chosen_cat = "company"
    if "prattle"  in cats_left:
      s = 30 if (len(set([1, 2, 3, 4]) - set(dice)) == 0 or len(set(
        [2, 3, 4, 5]) - set(dice)) == 0 or len(set([3, 4, 5, 6]) - set(dice)) == 0) else 0
      if s >= score:
        score = s
        chosen_cat = "prattle"
    if "squadron"  in cats_left:
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
  """
  if not bonus and len(scorecard_nums - set(curr_scores.keys())) == 0:
      bonusscore = 35 if sum(
          [curr_scores[i] for i in Scorecard.Numbers]) >= 63 else 0
      score += bonusscore
  """
  # print(score, chosen_cat)
  if chosen_cat == "":
    chosen_cat = cats_left.pop()
  print(score, chosen_cat)
  return score, chosen_cat

numbers_flag = False
  flag6 = False
  flag5 = False
  flag4 = False
  flag3 = False
  op = [3,4,5,6]
  for i in counts:
    if 3 in counts: 
      flag3 = True
      numbers_flag = True
    if 4 in counts:
      flag4 = True
      numbers_flag = True
    if 5 in counts:
      flag5 = True
      numbers_flag = True
    if 6 in counts:
      flag6 = True
      numbers_flag = True
  score = 0
  s = 0
  #chosen_cat = ""
  print(counts)
  if numbers_flag:
    if category in Scorecard.Numbers:
      if flag6:
        place = counts.index(6)
        if category == 'primis' and place == 0:
          score = 6
        elif category == 'secundus' and place == 1:
          score = 6*2
        elif category == 'tertium'and place == 2:
          score = 6*3
        elif category == 'quartus'and place == 3:
          score = 6*4
        elif category == 'quintus'and place == 4:
          score = 6*5
        elif category == 'sextus'and place == 5:
          score = 6*6
      elif flag5:
        place = counts.index(5)
        if category == 'primis' and place == 0:
          score = 5
        elif category == 'secundus' and place == 1:
          score = 5*2
        elif category == 'tertium'and place == 2:
          score = 5*3
        elif category == 'quartus'and place == 3:
          score = 5*4
        elif category == 'quintus'and place == 4:
          score = 5*5
        elif category == 'sextus'and place == 5:
          score = 5*6
      elif flag4:
        place = counts.index(4)
        if category == 'primis' and place == 0:
          score = 4
        elif category == 'secundus' and place == 1:
          score = 4*2
        elif category == 'tertium'and place == 2:
          score = 4*3
        elif category == 'quartus'and place == 3:
          score = 4*4
        elif category == 'quintus'and place == 4:
          score = 4*5
        elif category == 'sextus'and place == 5:
            score = 4*6
      elif flag3:
        place = counts.index(3)
        if category == 'primis' and place == 0:
          score = 3
        elif category == 'secundus' and place == 1:
          score = 3*2
        elif category == 'tertium'and place == 2:
          score = 3*3
        elif category == 'quartus'and place == 3:
          score = 3*4
        elif category == 'quintus'and place == 4:
          score = 3*5
        elif category == 'sextus'and place == 5:
          score = 3*6
    #return score, chosen_cat