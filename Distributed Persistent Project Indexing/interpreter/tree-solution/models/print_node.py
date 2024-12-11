
#Print node recieves the id (name) of the variable for printing
class PrintNode:

    def __init__(self, value, scope):
        self.id = value
        self.scope = scope
    
#prints null if the variable does not exist
    def execute(self):
        print(self.scope.vals.get(self.id, 'null')) 