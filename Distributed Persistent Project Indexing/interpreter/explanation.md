# Interpreter

## Problem characteristics:

- **Defined structure**: the input code is well structured.
- **Simple syntax**: language consists of only three types of statements:

    - Variable assignment

    - Scope definition

    - Print statement


## Challenges

- **Code parsing**: Correctly interpreting the input and mapping it to different syntax types.

- **Variable scope**: Ensuring that each variable is properly scoped and accessible only within their own context.

- **Varible assignment acros scopes**: Proper handling of variables declared in parent or sibling contexts.

## Solution

- Solution lays in a well formated parser. 

#### Usual aproach is building an AST **(abstract syntax tree)**.

- A common method in programming language interpreters where code is parsed into a tree structure. Each node represents a language construct.
- In this exact example, building an AST would introduce additional complexity which is not our goal.

#### Dual approach

1. Simultaneous parsing and execution:
    - Input is both parsed and executed during the initial pass.
    - Suitable for small-scale interpreters where speed and simplicity are main goals.
2. Decoupled parsing and execution:
    - Input is first parsed and the executed separately.
    - This approach is more suitable for larger inputs or more complex syntax structures.

### Stack-based solution

Chosen for its simplicity and intuitive workflow similar to already existing computer science concepts.


#### Characteristics

- **Single pass parsing and execution**: Data is being parsed and executed during the initial pass. This eliminates redundant operations and ensured efficiency.

- **Use of stack frames**: Each new scope initalizes a new stack frame, similar to real world code execution environments. Stack frames isolate commands and variables by setting them into their own scope.

#### Advantages

- **Straightforward design**:  
For this specific problem, it is easier to understand and implement a solution with the stack-based approach.

- **Immediate execution**:  
Commands are executed as they are parsed. Allowing for reduced memory usage and fast feedback.