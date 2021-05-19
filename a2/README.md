# a2
## Part 1

### Formulation

We formulated Sebastian as a expectimax problem, since each turn is the player rolling random dice and making choices to maximize their score.
There is no minimization as the goal is to achieve the highest score possible and there are no additional players that can interfere.

At some root node where the turn is, we have a decision layer (max layer) choosing which dice to reroll (first or second roll), or choosing what category to fill (end of turn).
Both decisions are followed by a randomization (expected value layer) of dice rolling.
```
                          Root
                        /      \
Dice Combos            ()       (1,3)
                       |        /  |  \
Possible Rolls        []       []  [] []
                      |        /\  /\  /\
Optimal Category    Squad     ...  ...  ...
```
### Program workings

The `SebastionAutoPlayer` uses the code in `yahtzee_expectimax` to do future looking and decision making.
On the first and second decisions to re-roll dice it calls `search_max` that searches several reroll attempts and turns in the future.
On the final look at the dice, `search_categories` is called and that picks the ideal category for the current hand while trying to look
into the future and see if we have a better long-term strategy.

When deciding at each layer which dice to reroll, we discern what dice are helping us fill each category.
To do this, we search for categories that already have the greatest number of dice filling them.
When picking a category, only those categories that can increase the score are initially tested. If none of these categories return a positive result, then we search the remaining unfilled categories in  hopes of the least-bad pick.

The other code in `SebastionAutoPlayer` is unused from previous attempts.

### Problems, assumptions, simplifications

The biggest problem was the sheer number of states that may need to be searched if you tried every possible dice reroll and category pick, even for just a few turns.
This increased the runtime complexity to unacceptable levels.

We made several optimizations to avoid searching paths that had no value when better solutions were known to exist. 
The first optimization strategy was to examine each category that was currently unfilled to determine how many of the dice in that roll worked to fulfill the criteria. 
If there were die that did not work to fulfill the criteria, we assumed that those die needed to be rerolled. 
This information was gathered into sets of the die to reroll.
By pre-determining which combination of die needed to be rerolled, we pruned many of the nodes in the decision layers. 

The second optimization technique was to look for sets of rerolled die that were repeated.
Sets may have been repeated because the same die may have been picked to be rerolled to fit different categories. 
For each set that had not been seen before, we added the set to a dictionary and cached the expected value of rerolling the first die in the set. 
Our assumption was that if a set was repeated, then we could determine whether calculating the full expected value was worthwhile to pursue. 
If a set matched any of the keys in the dictionary, meaning that it had been seen before, we compared the expected value of the first die and if it was less than or equal to the cached result, the set would be pruned. 

As an additional time-saving measure, we stopped using the `SebastianState` file for internal calculations. Passing it around and copying the data for successive
turn layers proved too expensive time-wise.

We did have some difficulty incentivizing the program to achieve the bonus score. A small portion of the games manage to receive the bonus. We made several attempts to prioritize which categories were picked in the hopes that it would increase the proportion of games that received the bonus score.

The first attempt centered on prioritizing filling the numbers categories when at least three of a kind existed in the roll. 
We calculated three of a kind to be the minimum number of counts needed in a roll to make the total value of the numbers categories greater than or equal to sixty-three. 
This only worked part of the time and tended to lead to more zeros in the scorecard at the end of the game than was helpful. 

The second attempt focused on ranking categories to be filled based on how much that category was likely to increase the overall score and what counts were needed to make that happen. 
For example, quintuplicatam added fifty points to the score card so that was prioritized first. 
It was also grouped under the categories that would benefit from having all five die be the same value, so the numbers categories and pandemonium were checked next if quintuplicatam was not chosen. 
The rest of the rankings followed the same logic.
Again, we ran into the issue of this method producing holes in the scorecard and, generally, decreasing the overall score. 

## Part 2
### Problem Formulation
Goal of a `betsy.py` program is to, when given input of (current player, board, time limit),
produce the board resulting from the best possible move for the current player (within the time limit).
To do this, it makes sense to represent the game of Betsy as a graph, then perform a minimax search
to find the optimal move.

* **State space:** All tuples (b,p), where b is a Betsy board and p is the current player.
* **Succ(b,p):** Set of all states (b',p') where b' is the board b after player p made their move,
and p' is the next player.
* **Goal states:** All states (b,p) where one of the two players has lost a king
* **h(b,p):** The value of board b to the maximizing player (white). So if b is very good for white,
h(b,p) will take on a large positive value. But if b is good for black, then h(b,p) will have a
negative value.

### How the Program Works
#### What is in this `part2` directory:
* `betsy.py`: Handles argument parsing, init current board, init the AI, print move recommended by the AI.
* `BetsyBoard.py`: "Board" class. Manages a board state (b,p). Contains functions for finding Succ(b,p)
(ie `move_space()`), making moves, and printing moves.
* `BetsyAI.py`: "AI" class. Manages time limit. `get_move(board)` uses alpha-beta pruned minimax to
find optimal move. Has evaluation function to determine heuristic h(b,p).
* `PieceSquares.py`: dictionary storing relative positional values for each piece.
* `game.py`: Manages a Betsy game between two players. Players can be AI or humans.
* `HumanPlayer.py`: "Human" class. Contains a `get_move(board)` function, but uses human input.
Takes command-line input from human (in chess algibraic notation) and returns move.

The most interesting code in this project appears in `BestyAI.py`. This contains the "AI" class
which performs the minimax search. The search is done recursively (rather than keeping track of a fringe).
I implemented the same algorithm with a fringe (see function in `MinimaxFringe.py`); however, I 
found that the recursive method was faster. `BetsyAI.py` uses alpha-beta pruning to avoid
searching through irrelevant branches.

The heuristic function does two main things:
1. Count up the # pieces, giving varying weights to each piece based on its value to the game
1. Add/subtract additional points for each piece's position on the board

`get_move()` primarily performs an iterative deepening search to find the best move (while staying
within the time limit). A couple improvements were made on top of the alpha-beta pruning to speed
up the search and improve result:
1. Initially randomize the move space (ie successors) to mimize chance of unnecessary draws
1. Keep track of a Principal Variation array (list of the moves in the best path from previous
depth iteration). Look at these moves first to increase chance of pruning.
1. Sort moves based on decreasing impact (again, to favor more pruning)
1. Rather than evaluating an entire board at each leaf, `alphabeta()` keeps track of the change in value
that each move causes (calculated by `eval_m()`). This value is then propogated down the tree to the leaves.
1. After seeing a capture towards the bottom of the tree (resulting in large change in board value),
`alphabeta()` will explore that branch further to gain a better picture of the capture's impact.

### Problems, Assumptions, and Decisions
It was a long process to get `BetsyAI` into its current state. Lots of testing was done to tweak
its performance. For example, I had to decide whether it was better to have a complicated heuristic
(that tries to capture more information about the current state) or a fast heuristic that
allows for a deeper search. In my testing, it seems like the faster heuristic performs better.
Another decision was to use a recursive search (rather than a fringe). The recursive method
was faster when tested, so the fringe was scratched.

In other branches, I implemented a lot of ideas that I ended up scratching (usually due to hindering
performance of BetsyAI).
These include (but are not limited to):
1. **Null heuristic:** allow opponent to move 2 turns in a row, then take their score as a alpha/beta
value (to improve pruning)
1. **Transposition database:** keep track of boards (and their score) that we have evaluated before.
Use these to reduce size of tree (ie stop exploring branches that we have seen before).
1. **Openings database:** I compiled a huge database of opening chess moves and their success rates.
This can be used to encourage a good early-game setup (that minimax will not find on it's own).
1. **Bit Boards:** I created a version of my Board class using "Bit Boards". Each board can be represented
as a handful of 64-bit uints. Then, ideally, the successor function, and other operations, can be
calculated very quickly (with simple bit operations).

A few online resources shaped my decisions in this project. Wikipedia's [article on alpha-beta pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)
contains pseudo-code that was useful in writng the recursive `alphabeta()` function.
I consulted a [page on Cornell's website](https://www.cs.cornell.edu/boom/2004sp/ProjectArch/Chess/algorithms.html), which provides some interesting discussion on techniques used to create a successful Chess AI.
Wikipedia also has an [article on chess piece values](https://en.wikipedia.org/wiki/Chess_piece_relative_value#Changing_valuations_in_the_endgame), which I referenced when designing my heuristic.
I also used a page from [freecodecamp.org](https://www.freecodecamp.org/news/simple-chess-ai-step-by-step-1d55a9266977/) to find relative piece positional values for my Piece-Square tables.
To create my database of opening moves, I processed over 800,000 chess games. These games come from
records from the [Free Internet Chess Server (FICS)](https://www.freechess.org/). I used games
of players ranked 2000+, captured from 2008-2019. These records can be found [here](https://www.ficsgames.org/download.html).
My idea of the Principal Variation array came directly from [chessprogramming.org](https://www.chessprogramming.org/Principal_Variation). I read a lot of the pages from this site as I worked on constructing
my Bit-Board implementation.
