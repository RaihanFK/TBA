#!/usr/bin/python

import sys, dfa, pda

def printcc(result: bool) -> None:
    match result:
        case True: print("Accepted")
        case False: print("Declined")

def main() -> None:
    if "--one" in sys.argv:
        result = dfa.matches(sys.stdin.read().strip())
        printcc(result)
        exit(0)

    result = pda.matches(sys.stdin.read().strip())
    printcc(result)
    exit(0)

if __name__ == "__main__":
    main()
