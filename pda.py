import dfa

def tokenize(html: str) -> list[str]:
    html = html.strip()
    tokens = []

    while html:
        html = html[html.find('<'):]
        tag = html[:html.find('>')+1]
        tagname = html[1:html.find('>')]

        if not dfa.valid_tag(tagname):
            return []

        tokens.append(tag)
        html = html[html.find('>')+1:]

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

def is_alpha(x: str) -> bool:
    global pt
    return x in pt

def find_product(alpha: str, token: str) -> list[str]:
    global pt

    for product in pt[alpha]:
        if product[0] == token:
            return product
    
    return []

def matches(html):
    stack = ['#']

    tokens = tokenize(html)
    if not tokens:
        return False

    alpha = 'S'
    i = 1

    product = find_product(alpha, tokens[0])
    for p in product:
        if is_alpha(p):
            alpha = p
            break
    if not product:
        return False

    stack.extend(reversed(product[1:]))

    while i < len(tokens):
        # print(tokens[i])
        # print(alpha)
        # print(stack)
        # print()

        if is_alpha(stack[-1]):
            product = find_product(stack[-1], tokens[i])
            # print("www:w ", product)

            if product:
                for p in product:
                    if is_alpha(p):
                        alpha = p
                        break

                stack.pop()
                stack.extend(reversed(product))
                continue
            
            if has_epsilon(stack[-1]):
                # discard `alpha`
                stack.pop()

                # current / tokens[i] := </h1>
                # stack               := [... </h1> epsilon
                #                             ^ should always be it's tag closer
                if stack.pop() != tokens[i]:
                    return False
                
                i += 1
                continue

            if not product:
                return False

        if stack[-1] == tokens[i]:
            stack.pop()
            i += 1
            continue

        product = find_product(alpha, tokens[i])
        if not product and stack.pop() != tokens[i]:
            return False

        stack.extend(reversed(product))
        stack.pop()
        i += 1

    return stack.pop() == '#'

for n, expected in enumerate([True, False, True, False, False, False], start=1):
    with open(f"html/{n}.html", "r") as f:
        html = f.read()
        f.close()

        assert matches(html) == expected
