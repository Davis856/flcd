import re
class Grammar():
    def __init__(self,filename):
        self.startingSymbol = ""
        self.filename = filename
        self.nonTerminals = list()
        self.terminals = list()
        self.productions = dict() # A -> B C | D E | F G as A: [[B, C], [D, E], [F, G]]
        self.indexedProductions = dict()
        self.isCFG=True
        self.index= 1
        self.startingSymbol= ""
        self.readGrammar()
        
    
    def getNonTerminals(self):
        return self.nonTerminals
    
    def getTerminals(self):
        return self.terminals
    
    def getProductions(self):
        return self.productions
    
    def getGrammarSymbols(self):
        return self.nonTerminals + self.terminals
    
    def getProductionsNonterminal(self, nonTerminal):
        return self.productions[nonTerminal]
    
    def getProductionIndex(self, lhs, rhs):
        for key in self.indexedProductions.keys():
            if self.indexedProductions[key][0]==lhs and self.indexedProductions[key][1]==rhs:
                return key
    
    def getProductionByIndex(self, index):
        return self.indexedProductions[index]
            
    def readGrammar(self):
        with open(self.filename, "r") as f:
            lines = f.readlines()
            
        for line in lines: 
            line = line.strip()
            if len(line) ==0: 
                continue
            
            # split line into lhs and rhs once we find the "::=" sign (lhs ::= rhs) rhs can contain ::= sign
            splitLine = line.split("::=", 2)
            lhs = splitLine[0].strip()
            rhs = splitLine[1].strip()
            rhsSymbols = rhs.split("|")
            # split even further by spaces
            rhsSymbolsList = list()
            for rhsSymbol in rhsSymbols: 
                rhsSymbolSplit = rhsSymbol.strip().split(" ") 
                rhsSymbolList = list()
                for rhs in rhsSymbolSplit:
                    if rhs.startswith("<") and rhs.endswith(">") and not rhs =="<>":
                        rhs = rhs[1:-1]
                        if rhs not in self.nonTerminals:
                            self.nonTerminals.append(rhs)
                    if rhs.startswith('"') and rhs.endswith('"') and not rhs =='""':
                        rhs = rhs[1:-1]
                        if rhs not in self.terminals:
                            self.terminals.append(rhs)
                    rhsSymbolList.append(rhs)
                rhsSymbolsList.append(rhsSymbolList)
            

            # add lhs, rhs to productions (lhs is key, rhs is value)
            # add lhs, rhs to productionsCG only if lhs is a list (lhs is key, rhs is value)
            lhsSplit = lhs.split(" ") 
            if len(lhsSplit) > 1: 
                self.isCFG = False
            else:
                if lhs.startswith("<") and lhs.endswith(">") and not lhs =="<>":
                    lhs = lhs[1:-1]
                if self.startingSymbol == "":
                    self.startingSymbol = lhs
                self.productions[lhs]=rhsSymbolsList
                if lhs not in self.nonTerminals: 
                    self.nonTerminals.append(lhs)
                
                # for each symbol in rhs, add it to terminals or nonTerminals
                for rhsList in rhsSymbolsList: 
                    if lhs != self.startingSymbol:
                        self.indexedProductions[self.index] = [lhs, rhsList]
                        self.index+=1

                    for rhsSymbol in rhsList:
                        # remove leading and trailing whitespace and "" for ebnf / <> for bnf
                        rhsSymbolClean = rhsSymbol.strip()
                        if rhsSymbolClean.startswith("<") and rhsSymbolClean.endswith(">") and not rhsSymbolClean =="<>":
                            rhsSymbolClean = rhsSymbolClean[1:-1]
                            if rhsSymbolClean not in self.nonTerminals:
                                self.nonTerminals.append(rhsSymbolClean)
                        
                        if rhsSymbolClean.startswith('"') and rhsSymbolClean.endswith('"') and not rhsSymbolClean =='""':
                            rhsSymbolClean = rhsSymbolClean[1:-1]
                            if rhsSymbolClean not in self.terminals:
                                self.terminals.append(rhsSymbolClean)

               
    def printNonTerminals(self):
        for nonTerminal in self.nonTerminals:
            print(nonTerminal)

    def printTerminals(self):
        for terminal in self.terminals:
            print(terminal)
        
    def printProductions(self): 
        for key in self.productions.keys(): 
            nonTerminal = key
            productions = self.productions[key]
            stringo = nonTerminal + " -> "

            for production in productions: 
                for symbol in production: 
                    if symbol in self.nonTerminals: 
                        symbol = "<" + symbol + ">"
                    elif symbol in self.terminals:
                        symbol = '"' + symbol + '"'
                    stringo = stringo + " " + symbol 
                stringo = stringo + " | "
            stringo=stringo[:-3]
            print(stringo)
    
    def printProductionsNonTerminal(self, nonTerminal):
        stringo = nonTerminal + " -> "
        for production in self.productions[nonTerminal]: 
            for symbol in production: 
                if symbol in self.nonTerminals: 
                    symbol = "<" + symbol + ">"
                elif symbol in self.terminals:
                    symbol = '"' + symbol + '"'
                stringo = stringo + " " + symbol
            stringo = stringo + " | "
        stringo=stringo[:-3]        
        print(stringo)