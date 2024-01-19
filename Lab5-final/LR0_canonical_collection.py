from State import State
from LR0_item import LRitem
class CanonicalCollection():
    def __init__(self, enhancedGrammar):
        self.enhancedGrammar = enhancedGrammar
        self.stateTransitions = dict()
        self.states = self.generate()

    def goTo(self, s, symbol):
        result = list()
        for item in s.getItems():
            if len(item.getBeta())==0:
                continue
            if item.getBeta()[0]==symbol:
                result.append(item.constructNewDotShift())
        return s.closure(result, self.enhancedGrammar)

    def generate(self):
        states = list()
        statesCopy = list()
        # startingState = closure({[S'->.S]})
        self.startingState = State(list())

        Sprime = self.enhancedGrammar.startingSymbol
        Sproductions = self.enhancedGrammar.productions[Sprime]
        
        for production in Sproductions:
            self.startingState.addItem(LRitem(Sprime, list(), production))
    
        self.startingState.setItems(self.startingState.closure(self.startingState.getItems(), self.enhancedGrammar))
        states.append(self.startingState)

        # for each state s in states
        changed = True
        while (changed):
            changed = False
            statesCopy = states.copy()
            for s in states:
                # for each grammar symbol X
                for X in self.enhancedGrammar.getGrammarSymbols():
                    # if goto(s, X) is not empty and not in states
                    gotoResult = self.goTo(s, X)
                    if len(gotoResult)!=0:
                        if State(gotoResult) not in statesCopy:
                            # append goto(s, X) to states
                            newState = State(gotoResult)
                            statesCopy.append(newState)
                            changed = True

                        if s in self.stateTransitions.keys():
                            self.stateTransitions.get(s)[X] = self.getState(gotoResult, statesCopy)
                    
                        else:
                            result = dict()
                            result[X] = self.getState(gotoResult, statesCopy)
                            self.stateTransitions[s]=result
        
            states = statesCopy.copy()
        return states

    def getState(self, gotoResult, states):
        for state in states:
            if state.getItems()==gotoResult:
                return state
        return None
    
    def printStates(self, states):
        i = 0
        for s in states: 
            stringo = "s"+str(i)+": "
            for item in s.getItems():
                stringo += str(item) + ", "
            print(stringo[:-2])
            i+=1

