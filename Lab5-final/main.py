from grammar import Grammar
from LR0_item import LRitem
from LR0_parser import LR0
from LR0_canonical_collection import CanonicalCollection
from LR0_table import LRTable
from State import State
import random
def GrammarPrints(grammar):
    print("\nGrammar from file: ", grammar.filename)
    print("\nProductions:")
    grammar.printProductions()
    print("\nNon-terminals:")
    grammar.printNonTerminals()
    print("\nTerminals:")
    grammar.printTerminals()
    print("\nIs CFG?")
    if grammar.isCFG: print("Yes it is!\n")
    else: print("Nope, it's not.\n")

def testGrammar():
    # read choices from user
    choice = input("Enter \n- 1 for g1.txt, \n- 2 for g2.txt: ")
    annoyance= ["You're annoying me. ", "You're really annoying me. ", "You're really really annoying me. ", "Please stop. ", "I'm going to stop responding if you don't stop. ", "You wanted it"]
    while choice != "1" and choice != "2":
        rand = random.randint(0, len(annoyance)-1)
        print(annoyance[rand])
        if rand == len(annoyance)-1: return
        choice = input("Enter 1 for g1.txt, 2 for g2.txt: ")

    if choice == "1":
        filename = "rules\\g1.txt" # Syntax.in from course
        grammar = Grammar(filename)
        GrammarPrints(grammar)

    if choice == "2":
        filename = "rules\\g2.txt" # Syntax.in from GitHub 1b
        grammar = Grammar(filename)
        GrammarPrints(grammar)
    
    print("That's all folks!")

def testCannonicalCollection():
    # read choices from user
    choice = input("Enter \n- 1 for g1.txt, \n- 2 for g2.txt: ")
    annoyance= ["You're annoying me. ", "You're really annoying me. ", "You're really really annoying me. ", "Please stop. ", "I'm going to stop responding if you don't stop. ", "You wanted it"]
    while choice != "1" and choice != "2":
        rand = random.randint(0, len(annoyance)-1)
        print(annoyance[rand])
        if rand == len(annoyance)-1: return
        choice = input("Enter 1 for g1.txt, 2 for g2.txt: ")

    if choice == "1":
        filename = "rules/g1.txt" # Syntax.in from course
        grammar = Grammar(filename)
        canonical = CanonicalCollection(grammar)
        states = canonical.states
        canonical.printStates(states)

        # assert len(states) == 9

        correctStates= list()
        # s0:
        # (S'->[].['S'])
        # (S->[].['A', 'a'])
        # (A->[].['a', 'A'])
        # (A->[].['b', 'A'])
        # (A->[].['c'])
        correctStates.append(State([LRitem("S'", list(), ['S']), LRitem("S", list(), ['A', 'a']), LRitem("A", list(), ['a', 'A']), LRitem("A", list(), ['b', 'A']), LRitem("A", list(), ['c'])]))

        # s1:
        # (S'->['S'].[])
        correctStates.append(State([LRitem("S'", ['S'], list())]))

        # s2:
        # (S->['A'].['a'])
        correctStates.append(State([LRitem("S", ['A'], ['a'])]))

        # s3:
        # (A->['a'].['A'])
        # (A->[].['a', 'A'])
        # (A->[].['b', 'A'])
        # (A->[].['c'])
        correctStates.append(State([LRitem("A", ['a'], ['A']), LRitem("A", list(), ['a', 'A']), LRitem("A", list(), ['b', 'A']), LRitem("A", list(), ['c'])]))

        # s4:
        # (A->['b'].['A'])
        # (A->[].['a', 'A'])
        # (A->[].['b', 'A'])
        # (A->[].['c'])
        correctStates.append(State([LRitem("A", ['b'], ['A']), LRitem("A", list(), ['a', 'A']), LRitem("A", list(), ['b', 'A']), LRitem("A", list(), ['c'])]))

        # s5:
        # (A->['c'].[])
        correctStates.append(State([LRitem("A", ['c'], list())]))

        # s6:
        # (S->['A', 'a'].[])
        correctStates.append(State([LRitem("S", ['A', 'a'], list())]))

        # s7:
        # (A->['a', 'A'].[])
        correctStates.append(State([LRitem("A", ['a', 'A'], list())]))

        # s8:
        # (A->['b', 'A'].[])
        correctStates.append(State([LRitem("A", ['b', 'A'], list())]))
        
        # Changed g1, so this is no longer correct
        # assert states == correctStates
        # print(states)

    if choice == "2":
        filename = "rules/g2.txt" # Syntax.in from GitHub 1b
        grammar = Grammar(filename)
        lr0 = LR0(grammar)
        states = lr0.canonicalCollection(grammar)
        lr0.printStates(states)
    
    print("That's all folks!")

def readFirstWord(filename):
    word_list = []
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            word_list.append(line.split()[0])
    return word_list

def main():
    # filename = "rules\\g1.txt" # Syntax.in from course
    # source = "rules\\seq.txt"
    filename = "rules/g2.txt" # Syntax.in from GitHub 1b
    source = "rules/pif.out"
    grammar = Grammar(filename)
    canonical = CanonicalCollection(grammar)
    table = LRTable(canonical)
    parser = LR0(table)
    inputList = readFirstWord(source)
    print(inputList)
    parseResult = parser.parse(inputList)
    print(parseResult)


if __name__ == "__main__":
    # testGrammar()
    # testCannonicalCollection()
    main()