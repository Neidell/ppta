#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Grammar import Grammar
from FSM     import FiniteStateMachine, drawFSM

grammars = {
    2: {
        "grammar": {
            "Vt": ['1', '0', '(', ')', '~', '&'],
            "Vn": ['K', 'L', 'Q', 'T', 'S', 'M', 'R', 'U', 'N', 'O', 'P', 'F'],
            "P" : ['S>(M', 'M>0R|1R', 'R>&L|~O|)U', 'K>1M', 'L>0K', 'Q>0R', 'T>1Q|)U', 'N>1M', 'O>0N', 'P>1R', 'F>0P|)U'],
        },
        "startState": "S",
        "endStates": ["U"]
    },
    3: {
        "grammar": {
            "Vt": ['a', 'b', 'c', 'd', '~', '&', '@'],
            "Vn": ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
            "P" : ['A>cC', 'C>aE|cF|bG', 'B>dC', 'D>dC', 'E>~B|@I', 'G>~D|@I', 'F>&C|@I', 'H>bE|aI', 'J>aG|bI'],
        },
        "startState": "A",
        "endStates": ["I"]
    },
    5: {
        "grammar": {
            "Vt": ['{', '}', '[', ']', '@'],
            "Vn": ['S', 'C', 'E', 'A', 'D', 'B', 'F', 'H'],
            "P" : ['S>{A|[C', 'A>{D', 'B>[A|{D', 'C>{E', 'D>}D|]H', 'E>}E|]F', 'F>@H', 'H>@F']
        },
        "startState": "S",
        "endStates": ["F", "H"]
    }
}

gramarToUse = 2

def main():
    currentGrammar = grammars[gramarToUse]

    G = Grammar(currentGrammar["grammar"])

    if G.grammarType[0] != 3:
        print "Not a regular grammar!\n"
        return

    FSM = FiniteStateMachine(G, currentGrammar["startState"], currentGrammar["endStates"]) 

    drawFSM(FSM, "FSM_initial")

    FSM.removeUnreachableStates()

    drawFSM(FSM, "FSM_no_unreachable_states")

    FSM.minimize()

    drawFSM(FSM, "FSM_minimised")

    FSM.printRules()

if __name__ == "__main__":
    main()