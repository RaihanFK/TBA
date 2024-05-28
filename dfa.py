table: list[dict[str, int]] = [{'<': 2}, {}, {}]

tags = ["a", "abbr", "address", "area", "article", "aside", "audio", "b", "base", "bdi", "bdo",
        "blockquote", "body", "br", "button", "canvas", "caption", "cite", "code", "col", "colgroup", "data",
        "datalist", "dd", "del", "dfn", "div", "dl", "dt", "em", "embed", "fieldset", "figcaption",
        "figure", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "head", "header",
        "hgroup", "hr", "html", "i", "iframe", "img", "input", "ins", "kbd", "label", "legend",
        "li", "link", "main", "map", "mark", "math", "menu", "meta", "meter", "nav", "noscript",
        "object", "ol", "optgroup", "option", "output", "p", "picture", "portal", "pre", "progress", "q",
        "rp", "rt", "ruby", "s", "samp", "script", "search", "section", "select", "slot", "small",
        "source", "span", "strong", "style", "sub", "sup", "svg", "table", "tbody", "td", "template",
        "textarea", "tfoot", "th", "thead", "time", "title", "tr", "track", "u", "ul", "var", "video", "wbr"]

initial_state = 0
final_states = [1]

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

    table[state]['>'] = 1

def matches(string: str) -> bool:
    state = initial_state

    for ch in string:
        if ch not in table[state]:
            return False

        state = table[state][ch]

    return state in final_states

for tag in tags:
    add_tag(tag)
    add_tag(f"/{tag}")

for tag in tags:
    assert matches(f"<{tag}>")
    assert matches(f"</{tag}>")
    assert not matches(f"{tag}")
    assert not matches(f"<{tag}")
    assert not matches(f"</{tag}")
    assert not matches(f"{tag}>")
    assert not matches(f"{tag}/>")
    assert not matches(f"<//{tag}>")

assert not matches("")
assert not matches("<")
assert not matches(">")
assert not matches("/")
assert not matches("</")
assert not matches("/>")
assert not matches("<>")
assert not matches("</>")
