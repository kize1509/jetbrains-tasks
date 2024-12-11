import sys
from models.print_node import PrintNode
from models.var_node import VarNode
from models.scope_node import ScopeNode

#Task text tells us that there are only 3 different types of syntax. print function, var declaration, and scope definition

        

#Parsin the code, creating a tree
if __name__ == '__main__':
    filename = sys.argv[1]
    stack=[]
    with open(filename, 'r') as f:

        starting_scope = ScopeNode({})
        current = starting_scope
        stack.append(current)
        
        for line in f.readlines():

            stripped = line.strip()
            tokens = stripped.split(" ")
            identifier = tokens[0]

            match identifier:
                
                case 'scope':
                    stack.append(current)
                    new_scope = ScopeNode(current.vals.copy())
                    current.add(new_scope)
                    current = new_scope
                    
                case 'print':
                    current.add(PrintNode(tokens[1], current))

                case '}':
                    current = stack.pop()
                    
                case _:
                    current.add(VarNode(tokens[0], current, tokens[2]))




        # executing the code
        starting_scope.traverse()
