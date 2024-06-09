import dfa
from pprint import pprint

def tokenize(html: str) -> list[str]:
    def __tokenize_impl(html: str, start=0, end=1) -> tuple[str, str]:
        if end > len(html):
            return (dfa.TOKEN_NONE, html)

        portion = html[start:end]
        if dfa.matches(portion):
            return (portion, html[end-1:])

        return __tokenize_impl(html, start, end + 1)
    
    tokens = []

    while html:
        token, html = __tokenize_impl(html)
        html = html[1:]

        if token:
            tokens.append(token)

    return tokens

pt = {
    'S': [
        ["<html>", 'A', "</html>"]
    ],
    'A': [
        ["<head>", 'B', "</head>", 'C' ],
        ["<body>", 'D', "</body>"],
        [""]
    ],
    'B': [
        ["<title>", "</title>"],
        [""]
    ],
    'C': [
        ["<body>", 'D', "</body>"]
    ],
    'D': [
        ["<h1>", 'D', "</h1>"],
        ["<p>", 'D', "</p>"],
        [""]
    ],
}

def has_epsilon(alpha: str) -> bool:
    global pt
    return pt[alpha][-1][0] == ""

def matches(html):
    start = 'S'
    k = 4

    tokens = tokenize(html)
    stack = ['#']

    i = 0
    found = False
    for product in pt[start]:
        if tokens[i][:k] == product[0][:k]:
            found = True
            stack.extend(reversed(product))
            break
    if not found: return False

    while i < len(tokens):
        if stack[-1] == tokens[i]:
            stack.pop()
            i += 1
            continue

        if stack[-1] in pt:
            alpha = stack[-1]
            found = False

            for product in pt[alpha]:
                if tokens[i][:k] == product[0][:k]:
                    found = True
                    stack.pop()
                    stack.extend(reversed(product))
                    break
            
            if not found and has_epsilon(alpha):
                # discard `alpha`
                stack.pop()

                # current / tokens[i] := </h1>
                # stack               := [... </h1> epsilon
                #                             ^ should always be it's tag closer
                if stack.pop() != tokens[i]:
                    return False
                
                i += 1
                continue
            
            if not found:
                return False

            continue

        found = False
        for alpha, productions in pt.items():
            for product in productions:
                if tokens[i][:k] == product[0][:k]:
                    found = True
                    stack.extend(reversed(product))
                    break
            
            if found:
                break

    return stack.pop() == '#'

for n, expected in enumerate([True, False, True, False, False, False], start=1):
    with open(f"html/{n}.html", "r") as f:
        html = f.read()
        f.close()

        assert matches(html) == expected
