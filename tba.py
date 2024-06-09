#!/usr/bin/python

import sys, dfa, pda

def main():
    if "--one" in sys.argv:
        print(dfa.matches(sys.stdin.read().strip()))
        return
    
    print(pda.matches(sys.stdin.read().strip()))

if __name__ == "__main__":
    main()
