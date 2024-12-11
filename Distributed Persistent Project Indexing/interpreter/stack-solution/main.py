import sys

from stack_frame import StackFrame



stack = []
tokens = []
filename = sys.argv[1]
with open(filename, 'r') as f:
    
    current = StackFrame({}, 0)
    stack.append(current)

    for l in f.readlines():
        stripped = l.strip()
        tokens = stripped.split(' ')
        identifier = tokens[0]
        match identifier:
             
            case 'scope':
                    
                vars_copy = current.get_vars().copy()  
                new_frame = StackFrame(vars_copy, len(stack))
                stack.append(new_frame)
                current = new_frame

            case 'print':
                current.execute_print(tokens[1])

            case '}':
                current = stack[current.get_depth()-1]

            case _:
                current.add(tokens)