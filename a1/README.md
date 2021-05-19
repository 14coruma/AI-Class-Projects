# Assignment 1

## Part 1

### Formulating the Problem

1. Definitions and Explanations:
    a) Search Space: The search space is all possible configurations of the 20 puzzle that can be reached by a path of f length and using moves that get the R1/C1 values to the goal position in the shortest number of moves. 

    b) Successor Function: All possible moves that bring the canonical first row and column values closer to their goal position, which decreases the h value.

    c) Cost Function (g(s)): Each move adds one to the f value.

    d) Goal State: Canonical configuration of the 20 puzzle.

    e) Heuristic Function (h(s)): (Sum of the moves needed for the canonical values of the first row and column to get to their goal position from the current state, excluding repeated numbers (so 1)) - (Number of tiles from R1/C1 that are not in the correct position and currently share a row or column, excluding the smallest value in each instance)

        i) For example in board 2, the sum of the canonical tiles is 3 (0 + 1 + 0 + 0 + 0 + 2 + 0 + 0). 2 and 6 share a column, so the number of tiles from the shared column is 1 (2 and 6, but 2 is not included). So the h value is 3 - 1 = 2. 

        ii) The smallest value in each instance of a shared row or column is not included in the shared value because it is assumed that moving the smaller tile will help move the larger tile closer to the goal position (and it did in practice).

        iii) This heurisitic is admissible because it always at most takes into account the moves needed to get R1/C1 into the correct place. Getting R1 and C1 into the correct place takes care of placement of the rest of the tiles on the board. Since the heuristic also accounts for tiles in the same row or column, it usually lowers the upper bound on the value to be equal to or lower than the n value for all of the boards I tested, where n is the number of moves made to get to the initial state from the canonical state. It never failed to find a solution equal to or less than the n value.

        iv) I found this specific heuristic (and the accompanying search algorithm) by trying to solve several puzzles by hand and then attempting to convert the strategy that I used to find the correct answer into a heuristic and algorithm. 

### The Search Algorithm 

2. The search algorithm starts by taking the state popped from the fringe and running it through a search function. The search function first calculates the distance from the current position to the goal of each value canonically in row 1 and column 1. This calculation takes into account the wrap around feature of the puzzle. It also calculates the number of moves needed for a left, right, up or down move. Search prunes any value with a total distance of 0 from the tiles to be moved. It also examines whether any tiles are in the same row or column, takes note of how many there are (excluding the smallest tile in the shared row or column), and prunes those tiles from the list of tiles to be moved (again exluding the smallest tile). The heuristic value is calculated using (the total number of moves for a state) - (the shared column/row information). Search passes this information to a function called rightPlace, which looks at whether the tiles to be moved are in the right row or column. rightPlace calls another function called posMoves, which uses the information from rightPlace to tell us whether it would be more beneficial to move L/R for an incorrect column or U/D for an incorrect row. posMoves calls a final function called code that translates this information into moves that might be found by the successor function. It also uses the number of moves needed to make a L/R/U/D move (found in search) to decide whether a (L or R) or (U or D) move would be better. This information is passed back to search and the solve function, which receives the list of pre-generated moves and the heuristic value, prunes any moves from the successor function that are not in the pre-generated list. Finally, any path longer than the f value (length of the current path + heuristic value of current state) is pruned from the fringe. 

### Problems Encountered

3. The biggest problem that I faced was finding a heuristic value that worked. I went through about 16 different heuristics before finding one that actually worked. The issue with each of the 16 heuristics that I tried was that it usually provided me with a much larger path length than the n value of the board I made. I did make the assumption that the n value was close to the optimal solution, so I wanted a heurisitic that either matched or undervalued that number. One strategy that I used to design the search algorithm was to start with a smaller puzzle that I called the 6 puzzle (2X3 board of numbers 1-6). This allowed me to more easily break the problem apart and fine tune the moving pieces. It also worked pretty well when translated to the 20 puzzle. One design decision that I made, however, was to hard code the correct move for tiles close to the edges of the row or column where wrap around would decrease the distance. This helped lower the heuristic value by a decent amount. As of Thursday, I was able to get all of the puzzles, except board10 to produce a solution in under 30 seconds. I have not been able to get board10 to produce a result at all. I've considered trying to optimize the code more, however, the strategies that I have tried, such as preventing states from being revisited, seem to increase the run time instead. I've tried about 5 or 6 different versions of the same search algorithm and the one that I currently have decreases the run time the most. I have not had an issue with getting paths of improper length. 

## Part 2

### Formulating Problem

1. Road directions are analogous to finding paths through a graph. The edges are roads, and the nodes are inersections of roads, or destinations such as cities or towns.
1. The state space is simply the road-segments and city-gps turned into a graph representation.
1. Sucessors of a node are all of the nodes it has edges to.
1. The weight of each edge depends on the cost function being used.

* `segments` gives each edge a weight of 1
* `distance` uses the road-segments length
* `time` computes the amount of time it would take to travel the segment at 5 miles an hour above the length's speed limit
* `cycling` computes the chance of an accident on the segment given it's speed limit and length

The two heuristic functions, the second one is the default:

1. Haversign: The original haversign formula was failing to find the correct path (i.e. inadmissible), so I changed it to h/2 and then it started working. I assume there is some incorrectness or rounding in the dataset since Haversign is *the* direct path cost between two lat/ong coortinade points. Which should always be less than or equal to the true path. Halving it just forces it to match the inequality.
1. Pythagorean hypotenuse: The difference between coordinate values is small even across the contiguous US. And as locations get closer the difference shrinks. This is a significant under-estimation of the direct distance between two locations. It will break if two locations are in different hemisphere quadrants.

### Description of Search Algorithm

This is just A* with two minor efficiency changes.

1. h(x) values are cached since locations to not move and h(x) is stable
1. g(x) to each new item being added to the fringe are tracked, and if path to a location is already known with a shorter cost, that path is dropped.

### Problems, assumptions, decisions

* I initially had trouble with large contiguous sections of point with missing coordinates, because my h(x) incorrectly computed the distance to the closest actual location.
* The hardest part was finding a workable heuristic for the distance between two lat/long pairs.
The Haversine formula calculates the distance in miles between two such pairs, but some path lengths must be rounded or different from reality, as it was overestimating some of the approximations.
Reducing it by a factor of two worked, but does not explain why the original formula failed.
I tried several lat/long formulas for distance, that took into account different map projection styles, but they all ran into the same issue.
I eventually settled for a simple pythagorean hypotenuse calculation.

## Part 3

### Formulating Problem
Goal is to find a grouping of *n* students which minimizes the provided cost function.
All *n* students must be placed into groups of size 1-3. The cost function is based
on the number of groups and the students' preferences.

* **State space:** All legal groupings of the students (groups are legal if size is <= 3).
* **Succ(s):** Set of all legal groupings where two groups in s have been combined.
* **Cost(s,s'):** The change in cost when combining 2 groups (can be positive or negative).
* **Goal states:** Legal grouping with minimzed cost.
* **h(s) = 0**
* **f(s) = g(s) =** The total cost of the group *s*

### Description of Search Algorithm
Search begins with a state where all *n* students are in their own groups (*n* groups).
Then Best-First-Search is used to search the tree for solutions with the smallest cost
(fringe is a priority queue).
Since we defined *Succ(s)* as above, when given enough time and a large enough fringe, BFS could traverse all possible states.

However, to speed things up in large trees, the fringe size is limited. This makes the Best-First-Search algorithm behave more like a local search (Beam search). 

Whenever the algorithm finds a state with the smallest cost seen so far, it prints the result
and updates the minCost value.

After beam search traverses down a path for a set number of steps, the algorithm shuffles the
list of students and restarts the search again (to traversing other paths through the tree).

### Problems, Assumptions, Decisions
Biggest problem is that the search tree is HUGE for a large number of students.
This makes it hard to store and work through the entire fringe in a best-first-search approach.
Additionally, often times there are optimal solutions that have a high cost early in the tree.
This makes it easy to get stuck around a local minimum and miss the optimal solution.

To address the first problem, I limit the size of the fringe. This solves the memory
and time constraint. However, it does not solve the problem of getting stuck around a local min.
To fix this, after a fixed number of steps, I restart the search with shuffled students.
This re-orders the fringe early on, encouraging new paths to be taken.

Before coming to this solution, I tried a different formulation of the problem.
I tried starting the tree in a state with just one student. Then, successors add a new
student (either on his/her own, or joining a previous group).
While this formulation is still valid, it results in a larger tree. Also, not all
states have potential to be goal states! This means that to solve this formulation,
the search algorithm must reach the bottom of the tree every time. So I had used a
guided DFS search, which was very slow. Even when attempting to create a heuristic,
this method did not improve.

One possible solution that I tried, but not perfected, is to use a Monte Carlo Descent.
This could help avoid the problem of being stuck around a local minimum.
To get this working, I might need to combine beam search and MC descent (run multiple MC descent paths
at once). I think if this is done correctly, an optimal solution could be found much
faster than the current method.
