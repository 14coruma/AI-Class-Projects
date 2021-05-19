# from copy import copy
from SebastianState import Scorecard

class SebSearchTreeNode:

    def __init__(self, parent, roll, scorecard, rerolled):
      self.parent = parent
      self.roll = roll
      self.rerolled = rerolled
      self.children = []
      self.scorecard = scorecard
      self.prob = (1 / 6) ** len(self.rerolled)
      self.new_cat = False
      self.category= ""

    def add_child(self, child):
      self.children.append(child)

    def value(self):
      return self.prob * self.scorecard.totalscore

    def score_category(self, category):
      # lazily copy scorecard, should not be edited externally
      new_card = Scorecard()
      new_card.scorecard = self.scorecard.scorecard.copy()
      new_card.totalscore = self.scorecard.totalscore
      new_card.bonusscore = self.scorecard.bonusscore
      new_card.bonusflag = self.scorecard.bonusflag
      self.scorecard = new_card
      # self.scorecard = deepcopy(self.scorecard)
      self.scorecard.record(category, self.roll)
      self.new_cat = True
      self.category = category

    @staticmethod
    def count_nodes(root):
      return sum([SebSearchTreeNode.count_nodes(child) for child in root.children]) + 1

    def __str__(self):
      return "dice: {}, reroll: {} category:{}".format(self.roll, self.rerolled, self.category)
