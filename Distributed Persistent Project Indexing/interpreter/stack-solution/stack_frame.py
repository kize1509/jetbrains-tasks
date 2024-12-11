class StackFrame:

    elments = []
    len = 0
    vars = {}
    depth = 0

    def __init__(self, vars, depth):
        self.vars = vars
        self.depth = depth

    def add(self, tokenized):

       self.vars[tokenized[0]] = self.vars.get(tokenized[2], tokenized[2]) 
       self.len += 1


    def get_vars(self):
    
        return self.vars

    def get_depth(self):

        return self.depth

    def execute_print(self, var):
        val = self.vars.get(var, 'null')
        
        print(val)

