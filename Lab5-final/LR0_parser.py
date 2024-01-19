from LR0_item import LRitem
from State import State


class LR0():

    def __init__(self, lrTable):
        # self.enhancedGrammar = enhancedGrammar
        self.InputStack = list()
        self.WorkingStack = list()
        self.OutputStack = list()
        self.table = lrTable

    def shift(self):
        state = self.WorkingStack[-1][1]
        tableEntry = self.table[state]

        topOfInputStack = self.InputStack[-1]

        self.InputStack.pop()
        gotoResult = tableEntry.targetStates[topOfInputStack]

        if gotoResult == None:
            return False

        self.WorkingStack.append([topOfInputStack, gotoResult])
        return True

    def reduce(self):
        state = self.WorkingStack[-1][1]
        tableEntry = self.table[state]
        reductionIndex = tableEntry.reductionIndex
        production = self.table.enhancedGrammar.indexedProductions[reductionIndex]
        rhsProductions = list()

        for i in range(len(self.WorkingStack) - 1, 0, -1):
            rhsProductions.insert(0, self.WorkingStack[i][0])

            if rhsProductions == production[1]:
                mMinusP = self.WorkingStack[i - 1][1]
                gotoResult = self.table[mMinusP].targetStates[production[0]]
                self.WorkingStack = self.WorkingStack[:i]
                self.WorkingStack.append([production[0], gotoResult])
                self.OutputStack.insert(0, reductionIndex)
                return True

        return False

    def parse(self, inputList):
        self.WorkingStack.append(["$", self.table.startingState])
        inputList.reverse()
        self.InputStack = inputList
        self.OutputStack = list()
        while True:
            state = self.WorkingStack[-1][1]
            if self.table[state].actionType == "SHIFT":
                if not self.shift():
                    print("Parsing Horror... sorry, Error")
                    return False
            elif self.table[state].actionType == "REDUCE":
                if not self.reduce():
                    print("Parsing Horror... sorry, Error")
                    return False
            elif self.table[state].actionType == "ACCEPT":
                return self.OutputStack
            else:
                print("Parsing Horror... sorry, Error")
                return False
