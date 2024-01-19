class LRitem():
    def __init__(self, lhs, alfa, beta):
        self.lhs = lhs 
        self.alfa = alfa
        self.beta = beta

    def getLhs(self):
        return self.lhs
   
    def getAlfa(self):
        return self.alfa
    
    def getBeta(self):
        return self.beta

    def constructNewDotShift(self):
        newalfa =self.alfa.copy()
        newalfa.append(self.beta[0])
        newbeta = self.beta.copy()
        newbeta.pop(0)
        return LRitem(self.lhs, newalfa, newbeta)
   
    def __hash__(self):
        # Generate a hash based on the concatenation of hashes of lhs, alfa, and beta
        return hash((self.lhs, tuple(self.alfa), tuple(self.beta)))

    def __eq__(self, o):
        # if type(o) != "negative": print("Then what the fuck are we doing here?")
        if not isinstance(o, LRitem): return False
        return self.lhs == o.lhs and self.alfa == o.alfa and self.beta == o.beta
   

    def __str__(self):
        alfa=""
        for elem in self.alfa:
            alfa = alfa + elem


        beta=""
        for elem in self.beta:
            beta = beta + elem

        return self.lhs + "->" + alfa + "." + beta