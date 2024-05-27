table: list[dict[str, int]] = [{'<': 1}, {}]

tags = [ "html", "body", "base", "head", "link", "meta", "style", "title", "address", "article", "aside", "footer", "header",
        "h1", "h2", "h3", "h4", "h5", "h6", "hgroup", "main", "nav", "section", "search", "blockquote", "dd", "div", "dl", "dt",
        "figcaption", "figure", "hr", "li", "menu", "ol", "p", "pre", "ul", "a", "abbr", "b", "bdi", "bdo", "br", "cite", "code",
        "data", "dfn", "em", "i", "kbd", "mark", "q", "rp", "rt", "ruby", "s", "samp", "small", "span", "strong", "sub", "sup",
        "time", "u", "var", "wbr", "area", "audio", "img", "map", "track", "video", "embed", "iframe", "object", "picture",
        "portal", "source", "svg", "math", "canvas", "noscript", "script", "del", "ins", "caption", "col", "colgroup", "table",
        "tbody", "td", "tfoot", "th", "thead", "tr", "button", "datalist", "fieldset", "form", "input", "label", "legend", "meter",
        "optgroup", "option", "output", "progress", "select", "textarea", "slot", "template" ]

initial_state = 0
final_states = []

def add_tag(name: str) -> None:
    assert len(name) > 0
    state = 1

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

for tag in tags:
    add_tag(tag)

for tag in tags:
    assert matches(f"<{tag}>")
    assert not matches(f"{tag}")
    assert not matches(f"<{tag}")
    assert not matches(f"{tag}>")
    assert not matches(f"<//{tag}>")

assert not matches("")
assert not matches("<")
assert not matches(">")
assert not matches("<h>")

assert matches("<html>")
assert not matches("<//html>")
assert not matches("<///html>")
assert not matches("<h1tml>")

assert matches("<h1>")
assert not matches("<h1")
assert not matches("h1>")
assert not matches("<h1>tml>")

assert matches("<p>")
assert not matches("<hp>")

assert matches("<body>")
assert matches("<title>")
