#!/usr/bin/python

import sys, dfa

def main():
    print(dfa.matches(sys.stdin.read().strip()))

if __name__ == "__main__":
    main()
