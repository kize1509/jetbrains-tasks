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

- Missing current position feature and that implies that none of the Graph Search algorithms can be used.
- The problem is a blind search problem.
- No efficient algorithm can be used to solve the problem.
- Each solution step count depends on the grid size, goal position, and the initial player position.
- Approach used is a straightforward *right - down walk* further explained in the solution section.

# Solution

- Solution is a simple yet effective approach.
- When exploring a grid or matrix with rotation feature (torodial grid), we want to explore each row and column.
- And while exploring rows or columns in an incremental step fashion we usually get stuck in a loop.
- Since we do not have information on A nor B, walk consists of prime number of steps in right and down direction.
- The walk is called a *right - down walk*.
- Each new sequence of steps is a prime number. With growing primes, we lower the chance of repeating the same position in the grid.
- In this process we are able to cover the whole grid, but looping is not excluded since we do not have information on the grid size, only cycle length enlargment is possible.
- To prevent looping or exit loops, after a certain number of steps we perform an additional step in the opposite direction.
- With this approach we secure that the exploration of the grid/finding the apple is done in approximately 15 * S steps. (tested on 12000 random grids with random apple positions and radnom starting positions, grid dimensions range A : 1 - 1000000 ; B : 1 - 1000000 ; A * B < 10^6)


# Code explanation

- Code provided is a test sample.
- Main method is *traverse* method.
- Methods used are *move_right*, *move_down*, *move_up*. Each method handles the wrapping of the grid.
- During the traversal, none of the grid dimensions is used.
- All of the excess parameters and methods are used for testing purposes. Such as randomization of the grid, apple position, and player position.