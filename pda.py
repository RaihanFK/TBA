import dfa
from pprint import pprint

TOKEN_HTML = {
    "html": 'H1',
    "/html": 'H2',
}

TOKEN_BODY = {
    "body": 'B1',
    "/body": 'B2',
}

TOKEN_HEAD = {
    "head": 'H3',
    "/head": 'H4',
}

TOKEN_TITLE = {
    "title": 'T1',
    "/title": 'T2',
}

TOKEN_H1 = {
    "h1": 'V1',
    "/h1": 'V2',
}

TOKEN_P = {
    "p": 'P1',
    "/p": 'P2',
}

stack = ['#', 'R']
ptokens = [TOKEN_HTML, TOKEN_BODY, TOKEN_HEAD, TOKEN_TITLE, TOKEN_H1, TOKEN_P]
ptable = {
    TOKEN_HTML["html"]: {
        "pop": [],
        "push": ['H'],
    },
    TOKEN_HTML["/html"]: {
        "pop": ['H', 'R'],
        "push": [],
    },
    TOKEN_HEAD["head"]: {
        "pop": ['H'],
        "push": ['H', 'D'],
    },
    TOKEN_HEAD["/head"]: {
        "pop": ['D'],
        "push": ['D'],
    },
    TOKEN_BODY["body"]: {
        "pop": ['D'],
        "push": ['B'],
    },
    TOKEN_BODY["/body"]: {
        "pop": ['B'],
        "push": [],
    },

    TOKEN_TITLE["title"]: { "pop": ['D'], "push": ['D', 'T'] },
    TOKEN_TITLE["/title"]: { "pop": ['T'], "push": [] },

    TOKEN_P["p"]: { "pop": ['B'], "push": ['B', 'P'] },
    TOKEN_P["/p"]: { "pop": ['P'], "push": [] },

    TOKEN_H1["h1"]: { "pop": ['B'], "push": ['B', 'V'] },
    TOKEN_H1["/h1"]: { "pop": ['V'], "push": [] },
}

def find_ptoken(name: str) -> str | None:
    global ptokens

    for tok in ptokens:
        if name in tok:
            return tok[name]
    
    return None

def tokenize(html: str) -> list[str]:
    def __tokenize_impl(html: str, start=0, end=1) -> tuple[str, str]:
        if end > len(html):
            return (dfa.TOKEN_NONE, html)

        portion = html[start:end]
        if dfa.matches(portion):
            return (find_ptoken(portion[1:-1]), html[end-1:])

        return __tokenize_impl(html, start, end + 1)
    
    tokens = []

    while html:
        token, html = __tokenize_impl(html)
        html = html[1:]

        if token:
            tokens.append(token)

    return tokens

# TODO:
def matches(html):
    global stack
    __stack = stack.copy()

    tokens = tokenize(html)
    for tok in tokens:
        if tok not in ptable:
            return False

        for expected in ptable[tok]["pop"]:
            if stack.pop() != expected:
                return False
        
        for extended in ptable[tok]["push"]:
            stack.append(extended)

    accepted = stack.pop() == '#'
    stack = __stack
    return accepted

print(matches("""<html>
    <head>
        <title>Title</title>
    </head>
    <body>
        <p>Paragraph</p>
    </body>
</html>"""))
