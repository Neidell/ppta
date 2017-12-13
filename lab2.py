#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Grammar import Grammar
from FSM     import FiniteStateMachine, drawFSM

grammar = {
        "Vt": ['0', '1', '*', '$', '/'],
        "Vn": ['K', 'L', 'M', 'N', 'Q', 'P', 'R', 'S'],
        "P" : ['K>1L|0N', 'L>0M|0P|/Q', 'N>1R|1M|*S', 'Q>1P', 'P>*L|$', 'M>$', 'S>0R', 'R>/N|$']
    }


def main():
    G = Grammar(grammar)

    if G.grammarType[0] != 3:
        print "Not a regular grammar!\n"
        return

    FSM = FiniteStateMachine(G, "K", ["V"])

    drawFSM(FSM, "FSM_initial")

    FSM.removeUnreachableStates()

    FSM.determinate()

    drawFSM(FSM, "FSM_determinated")

    FSM.printRules()

if __name__ == "__main__":
    main()