#!/usr/bin/python

import sys, dfa

def main():
    print("Halo, dunia!")
    dfa.matches(sys.stdin.read())

if __name__ == "__main__":
    main()
