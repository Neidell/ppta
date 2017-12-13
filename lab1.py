#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Grammar import Grammar

grammarList = [
    {
        "Vt": ['~', 'c', 'd'],
        "Vn": ['S', 'A'],
        "P" : ['S>ccAd', 'A>ccAd|~']
    },
    {
        "Vt": ['~', 'a', 'b'],
        "Vn": ['S', 'A', 'B'],
        "P" : ['S>A|B', 'A>a|Aa', 'B>b|Bb|Ab']
    },
    {
        "Vt": ['~', 'a', 'b'],
        "Vn": ['S', 'A', 'B'],
        "P" : ['S>A|B', 'A>a|Aa', 'B>b|BbA|Ab']
    },
    {
        "Vt": ['~', 'a', 'b', 'c'],
        "Vn": ['S', 'A', 'B', 'C', 'D'],
        "P" : ['S>aSBC|abc', 'bC>bc', 'CB>BC', 'cC>cc', 'B>~']
    },
    {
        "Vt": ['~', 'a', 'b', 'c'],
        "Vn": ['S', 'A', 'B', 'C', 'D'],
        "P" : ['S>aSBC|abc', 'bC>bc', 'CBD>BC', 'cC>cc', 'BB>~']
    }]

def main():
    for grammar in grammarList:
        G = Grammar(grammar)

        print G.grammarType[1]

    return

if __name__ == "__main__":
    main()

