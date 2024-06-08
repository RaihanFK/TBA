import dfa
from pprint import pprint

def tokenize(html: str) -> list[str]:
    def __tokenize_impl(html: str, start=0, end=1) -> tuple[str, str]:
        if end > len(html):
            return (dfa.TOKEN_NONE, html)

        portion = html[start:end]
        if dfa.matches(portion):
            return (portion, html[end:])

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
    tokens = tokenize(html)
    return tokens

print(matches("""<html>
</html>"""))
