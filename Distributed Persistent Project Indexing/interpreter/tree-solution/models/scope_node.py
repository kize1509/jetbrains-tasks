from models.var_node import VarNode
from models.print_node import PrintNode

#Each scope node, has its own children set of variables/commands/scopes, parsing proccess is actually a creation of a tree
class ScopeNode:

    def __init__(self, vals):
        self.scope =[]
        self.vals = vals

#We need to keep track of current values inside the scope, that is why the check is performed
    def add(self, node):
        if isinstance(node, VarNode):
            self.vals[node.id] = node.val
        self.scope.append(node)


#Traversing the children nodes, based on the node type, if a nested scope appears the recursion continues. Otherwise print is executed.
    def traverse(self):
        for child in self.scope:
            if isinstance(child, ScopeNode):
                child.traverse()
            if isinstance(child, PrintNode):
                child.execute()
