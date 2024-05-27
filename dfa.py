table: list[dict[str, int]] = [{}, {}, {}]

initial_state = 0
final_states = []

table[0]['<'] = 2
table[1]['/'] = 2

def add_tag(name: str) -> None:
    assert len(name) > 0
    state = 2

    for i in range(len(name)):
        if name[i] in table[state]:
            state = table[state][name[i]]
            continue
        
        table[state][name[i]] = len(table)
        state = len(table)
        table.append({})

    table[state]['>'] = len(table)
    table.append({})
    final_states.append(len(table) - 1)

def matches(string: str) -> bool:
    state = initial_state

    for ch in string:
        if ch not in table[state]:
            return False

        state = table[state][ch]

    return state in final_states

TAG = add_tag
TAG("html")
TAG("html5")
TAG("html35")
TAG("h1")
TAG("p")
TAG("body")
TAG("title")

assert not matches("")
assert not matches("<")
assert not matches(">")
assert not matches("<h>")

assert matches("<html>")
assert not matches("<h1tml>")

assert matches("<html5>")
assert not matches("html5")

assert matches("<html35>")
assert not matches("html35>html")

assert matches("<h1>")
assert not matches("<h1")
assert not matches("h1>")
assert not matches("<h1>tml>")

assert matches("<p>")
assert not matches("<hp>")

assert matches("<body>")
assert matches("<title>")
