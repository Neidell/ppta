#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

class Grammar:
    def __init__(self, grammarParams):
        self.Vt = grammarParams["Vt"]
        self.Vn = grammarParams["Vn"]
        self.P  = grammarParams["P"]

        self._vt = re.escape(''.join(self.Vt))
        self._vn = re.escape(''.join(self.Vn))

        print self._vt
        print self._vn


        self.grammarType = None

        self.grammarCheckers = [
            (3, self.checkRegularGrammar), 
            (2, self.checkContextFreeGrammar), 
            (1, self.checkContextSensitiveGrammar)
        ]

        for num,gramChecker in self.grammarCheckers:
            res,descr = gramChecker()

            if res:
                self.grammarType = (num,descr)
                break

        if not self.grammarType:
            self.grammarType = 0, "Phase structure"



    def checkRegularGrammar(self):
        ret = (False, "")

        for p in self.P:
            name,rule = p.split(">")

            if len(name) != 1 or name not in self.Vn:
                return (False, "")

            for subRule in rule.split("|"):

                if re.match("^[" + self._vt + "]+["+ self._vn + "]+$", subRule):
                    if not ret[0]:
                        ret = (True, "Right regular grammar")
                    if ret[1] == "Left regular grammar":
                        return (False, "")
                elif re.match("^[" + self._vn + "]+[" + self._vt + "]+$", subRule) :
                    if not ret[0]:
                        ret = (True, "Left regular grammar")
                    if ret == "Right regular grammar":
                        return (False, "")
                elif re.match("^([" + self._vn + "]+|[" + self._vt + "]+)$", subRule):
                    continue
                else:
                    return (False, "")

        return ret

    def checkContextFreeGrammar(self):

        for p in self.P:
            name,rule = p.split(">")

            if len(name) != 1 or name not in self._vn:
                return (False, "")

            for subRule in rule.split("|"):
                if not re.match("^[" + self._vt + self._vn + "]*$", subRule):
                    return (False, "")

        return (True, "Context free")

    def checkContextSensitiveGrammar(self):
        for p in self.P:
            name,rule = p.split(">")

            if not re.match("^[" + self._vt + self._vn + "]+$", name):
                    return (False, "")

            for subRule in rule.split("|"):
                if len(name) > len(subRule):
                    return (False, "")

                if not re.match("^[" + self._vt + self._vn + "]*$", subRule):
                    return (False, "")

        return (True, "Context sensitive")

