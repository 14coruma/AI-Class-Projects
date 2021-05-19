# a0

*Note: please grade the version that is on the master branch.*

## Part 1: Navigation
* **Valid states:** Set of all positions (y,x), where each position is a tuple containing a valid position of pichu, "p", on the given board/map.
* SUCC(s) = Set of all legal adjacent (non-diagonal) neighboring positions of s=(y,x). Namely (y+1,x), (y-1,x), (y,x-1), (y,x+1). *(note, if any of these positions are not legal, they will not be included in SUCC(s))*.
* C(s,s') = 1. *(assume s != s', and s' \in SUCC(s))*
* **Initial state:** Initial position, (y,x), of pichu "p".
* **Goal state:** Position, (y,x), of you "@".

There is a problem with `route_pichu.py` as given. Previously visited states are added to the fringe, so DFS may enter a loop. To fix this, I created a dictionary (hash table) which remembers all the states that have been previously visited. Then, when the search algorithm uses SUCC(s) to add states to the fringe, it only adds states that do not already appear in the visited dictionary. This prevents loops from occuring in the search algorithm.

Another problem with `route_pichu.py`: uses DFS. This does not necessarily find an optimal solution. I created a map with filename `map0.txt`. Using this map, the original DFS search finds a non-optimal solution. Instead, if the fringe is implemented as a queue, the search algorithm will always find an optimal solution (BFS).

## Part 2: Hide-and-seek
* **Valid states:** Set of all boards with 1 or more pichus that cannot see each other.
* SUCC(s) = Set of all valid states that are identical to s but with one more pichu placed in a legal position.
* C(s,s') = 1. *(assume s!= s', and s' \in SUCC(s))*
* **Initial state:** A board with one pichu.
* **Goal state:** A valid board with k pichus (for the provided/desired k value).

**Design process:** First I fixed the provided code by making sure that `add_pichu()` always
puts pichus in valid positions.

Then I tried to speed up the `add_pichu()` step by remembering which positions
on the board were illegal on previous depths. I think this method of pruning the search tree 
should speed things up a lot. However, this method was a bit more complicated than I expected, so I scrapped the idea.

Next I decided to force the code to place Pichus starting from the top of the board to the
bottom. This way, `arrange_pichus.py` can remember at each state what row a pichu was last added
to. There is no need to attempt adding Pichus to rows above this point, becuase those rows
are already full. This reduces the number of potential successor boards to search through,
thus speeding up the process significantly.

Finally I solved the extra credit problem (when K=0, place max # of Pichus, assuming they cannot see eachother diagonally as well). To do this, I duplicated and modified a few functions
to check for Pichus along the diagonal (when creating a state's list of legal successors).
Then the `solution_EC()` function keeps track of the board with the max number of Pichus
that it has seen thus far, returning this value when the entire state tree has been processed.

## Other Notes
This code is definitely not the cleanest. In particular, there is a lot of room to [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)-out some functions by removing duplicate code (the `legal_state()` functions are especially messy). However, the code gets the job done,
and should be documented well enough to be easily readable.

The code in this assignment began with provided skeleton code (for CSCI B551). Then it
was modified only by me (Andrew Corum) using no outside sources (other than basic
Python syntax resources, such as [w3schools](https://www.w3schools.com/) and [python docs](https://docs.python.org/3/reference/index.html)).
