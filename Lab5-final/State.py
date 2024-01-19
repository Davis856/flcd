from grammar import Grammar
from LR0_item import LRitem
class State (): 
    def __init__(self, items):
        self.items = items

    def getItems(self): 
        return self.items

    def addItem(self, item): 
        self.items.append(item)

    def setItems(self, items): 
        self.items = items

    def closure(self, I, enhancedGrammar):
        C = I.copy()
        C1 = C.copy()
        added = True
        while added: 
            added = False
            C1 = C.copy()
            for item in C: 
                # make a copy of C to avoid ConcurrentModificationException
                if len(item.getBeta())==0: 
                    continue
                
                B = item.getBeta()[0]
                if B in enhancedGrammar.getNonTerminals(): 
                    # for B->y in P do
                    for rhs in enhancedGrammar.getProductions().get(B): 
                        # if B->.y not in C then
                        newItem = LRitem(B, list(), rhs)
                        if newItem not in C1: 
                            C1.append(newItem)
                            added = True

            # add all items from C1 to C
            C = C1.copy()
        
        return C

    def __eq__(self, o): 
        if not isinstance(o, State): return False
        return self.items == o.items
    
    def __hash__(self):
        # Generate a hash based on the concatenation of hashes of item tuples
        return hash(tuple(map(hash, self.items)))

    def __str__(self): 
        string=""
        for item in self.items: 
            string += str(item) + " , "
        return string