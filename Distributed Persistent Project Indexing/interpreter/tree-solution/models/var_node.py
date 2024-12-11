

#Variable node can recieve a real value but also a referenece to another variable, every variable value is stored in its scope values.
class VarNode:


    def __init__(self, id, scope, val):
        self.id = id
        self.val = scope.vals.get(val, val)