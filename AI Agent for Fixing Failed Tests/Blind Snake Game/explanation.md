# BLIND SNAKE GAME

# Problem Definition

- Finding a 1x1 square on a torodial grid of unknow dimensions.
- The grid is a torodial grid, meaning that the edges are connected, no edge crossing signals.
- No current position information.
- No goal position information.
- No grid dimensions information.

# Problem Analysis

- The problem is a blind search problem.
- The problem is a torodial grid problem.
- Initial state: No information.
- Actions: Move in any direction.
- Transition model: The grid is a torodial grid.
- Goal state: 1x1 square.
- Path cost: 1 per move.
- Maximum moves: 35 * S, where S is the number of squares in the grid.


# Problem Formulation

- Key feature missing, current position. 
- The current position is the key to solving the problem.
- If the current position is known, the problem is a simple path finding problem, which can be implemented in O(S) time complexity.
- Since the current position is missing, we don't have a guarantee that there will not be redundant position visits.


# Problem Solution

- Initial idea is to perform a systematic search.
- The search will be a spiral search.

- Solution problems:
    - No time guarantee.
    - Possible redundant position visits.
    - Some grid sizes may not be solvable even in S^2 steps. 
    - For example in a 1x1000000 grid, the snake will cover small portion of the grid in 35xS steps.
    - This fenomenon occurs solely because of the torodial grid property and the lack of current position information which does not allow us to track visited positions.


- Addition to the solution:
    - Including a random/probabilistic component to the search.
    - This is just one possible solution.
    - While exploring the grid systematically, the snake will also make random moves after finishing a cycle of 5xS.
    - Then 3 random moves will be made to increase the chance of escaping the redundant cycles.

- The solution is not guaranteed to find the goal state in all cases.
- The solution is not guaranteed to find the goal state in a certain time.
- Solution is optimized for grids in varying dimensions of (100-1000)x(100-1000).
- Number of steps in solution for grids such as 1x1000000 is solely based on the initial position beacause of the exploring algorithm nature.
- Systematic search guarantees to explore the entire grid, but in a more time consuming manner.
- Random moves are added to increase the chance of finding the goal state in a reasonable time.
