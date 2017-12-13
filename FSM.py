#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from subprocess import call
from itertools import groupby
from Grammar import Grammar

class FiniteStateMachine:

    def __init__(self, G, startState, finalStates):
        self.G = G

        self.Q = G.Vn        # состояния
        self.T = G.Vt        # сигналы
        self.F = []          # функции переходов
        self.H = startState  # начальное состояние
        self.Z = finalStates # конечное состояние

        self.Q_ = []         # states after determination
        self.F_ = []         # rules after determination
        self.Z_ = []         # final states after determination

        self.states = {}

        self.updateGrammarWithFinalState()
        self.createRulesFromGrammar()

        self.createStates()

    def updateGrammarWithFinalState(self):
        #добавляем новые правила
        if self.Z[0] not in self.Q:
            self.G.Vn += self.Z[0]
        else:
            return

        for i, p in enumerate(self.G.P):
            name,rule = p.split(">")

            for subRule in rule.split("|"):
                if re.match("^[" + ''.join(self.G.Vt) + "]+$", subRule):
                    self.G.P[i] = p.replace(subRule, subRule + self.Z[0])

    def createRulesFromGrammar(self):
        # формируем функции переходов
        for p in self.G.P:
            name,rule = p.split(">")

            for subRule in rule.split("|"):
                self.F.append({
                    "startState": name,
                    "endState": subRule[1],
                    "signal": subRule[0]
                })

    def createStates(self):
        # формируем список вершин с соответствующими им переходами
        for f in self.F:
            if not f["startState"] in self.states:
                self.states[f["startState"]] = []
            
            self.states[f["startState"]].append({
                "endState": f["endState"],
                "signal": f["signal"]
            })

    def printRules(self):
        #выводим функции переходов до и после детерминации
        print "\n === FSM Rules === \n"
        for f in self.F:
            print "f({},{}) -> {}".format(f["startState"], f["signal"], f["endState"])

    def exploreState(self, state):

        # добавляем новое состояние с список состояний "после детерминации"
        if state not in self.Q_:
            self.Q_.append(state)

        def sign_key(a): 
            return a["signal"]

        # собираем все правила ведущие из текущего состояния и группируем их по сигналу
        stateRules = [f for f in self.F if f["startState"] in state]
        groupedStateRules = [list(g[1]) for g in groupby(sorted(stateRules, key=sign_key), sign_key)]        

        # итерируемся по каждой группе правил
        for group in groupedStateRules:
            newState = ""

            # формируем новое состояние автомата как объединение состояний в которые мы переходим из текущего по одинаковому сигналу
            for rule in group:
                if rule["endState"] not in newState:
                    newState += rule["endState"]

            # добавляем новое правило список правил "после детерминации"
            self.F_.append({
                "startState": state,
                "signal": group[0]["signal"],
                "endState": newState,
            })

            # рекурсивно переходим по новому правилу в следующее состояние
            if newState not in self.Q_:
                self.exploreState(newState)

        # print groupedStateRules

    def determinate(self):
        # добавляем начальное состояние и конечное состояний "после детерминации"     
        self.Q_.append(self.H)
        self.Z_ += self.Z

        self.exploreState(self.H)

        self.Q = self.Q_
        self.F = self.F_
        self.Z = self.Z_

        self.Q_ = []
        self.F_ = []
        self.Z_ = []

    def traverse(self, state):

        # добавляем новое состояние с список состояний "после детерминации"
        if state not in self.Q_:
            self.Q_.append(state)

        def sign_key(a): 
            return a["signal"]

        # собираем все правила ведущие из текущего состояния и группируем их по сигналу
        stateRules = [f for f in self.F if f["startState"] in state]

        # итерируемся по каждой группе правил
        for rule in stateRules:
            newState = rule["endState"]

            # рекурсивно переходим по новому правилу в следующее состояние
            if newState not in self.Q_:
                self.traverse(newState)


    def removeUnreachableStates(self):
        self.Q_.append(self.H)
        self.Z_ += self.Z

        # выполняем обход графа и удаляем состояния, через которые не было прохода

        self.traverse(self.H)

        unreachableStates = list(set(self.Q) - set(self.Q_))

        for rule in self.F:
            if rule["startState"] not in unreachableStates:
                self.F_.append(rule)

        self.Q = [s for s in self.Q if s not in unreachableStates]
        self.F = self.F_

        self.Q_ = []
        self.F_ = []
        self.Z_ = []

    def minimize(self):
        def is_final_state(a):
            return a in self.Z

        def state_outputs(a):
            output = []

            for rule in self.F:
                if rule["startState"] == a and rule["endState"] in group_prev:
                    output.append(rule["signal"])

            return sorted(output)

        # группируем состояния, начиная с конечных

        group = []
        group_prev = []

        groupedStates = [list(g[1]) for g in groupby(sorted(self.Q, key=is_final_state), is_final_state)]
        groupedStates_prev = []
        
        while len(groupedStates_prev) != len(groupedStates):
            groupedStates_prev = groupedStates[:]

            group_prev = groupedStates[1]
            group = [list(g[1]) for g in groupby(sorted(groupedStates[0], key=state_outputs), state_outputs)]

            if len(group) > 1:
                groupedStates[0 : (len(group)-1)] = tuple(group)

        # объединяем состояния из полученных групп в новые
        
        for group in groupedStates:
            newState = ''.join(group)

            # заменяем старые состояния в правилах на новые
            for rule in self.F:
                if rule["startState"] in group:
                    rule["startState"] = newState
                if rule["endState"] in group:
                    rule["endState"] = newState

            for st in group:
                self.Q.remove(st)

            self.Q.append(newState)

        # находим и удаляем одинаковые правила из списка

        duplicateIndexes = []

        for i, curRule in enumerate(self.F):
            for j, rule in enumerate(self.F[i+1:]):
                if (curRule["startState"] == rule["startState"] and 
                    curRule["endState"]   == rule["endState"] and 
                    curRule["signal"]     == rule["signal"]):
                    
                    duplicateIndexes.append(i + j)


        for i in sorted(duplicateIndexes, reverse=True): 
            del self.F[i]

def drawFSM(FSM, fileName):
    gvProg = ''

    gvProg += 'digraph finite_state_machine {\n'
    gvProg += '   rankdir=LR;\n'
    gvProg += '   size="8,5"\n'

    print FSM.Q

    for state in FSM.Q:
        if state in FSM.H:
            gvProg += '   node [shape = point ]; qi\n'
            gvProg += '   node [shape = circle, label="{}", fontsize=12] {};\n'.format(state, state)
            gvProg += '   qi -> S;\n'
        elif state in FSM.Z:
            gvProg += '   node [shape = doublecircle, label="{}", fontsize=12] {};\n'.format(state, state)
        else:
            gvProg += '   node [shape = circle, label="{}", fontsize=12] {};\n'.format(state, state)

    for rule in FSM.F:
        gvProg += '   {}   -> {}  [ label = "{}" ];\n'.format(rule["startState"], rule["endState"], rule["signal"])

    gvProg += '}\n'

    with open("./output/" + fileName + ".gv", "w") as the_file:
        the_file.write(gvProg)

    call(["dot", "-Tpng", "./output/" + fileName + ".gv", "-o", "./output/" + fileName + ".png"])
