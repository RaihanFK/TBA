from functools import reduce

TOKEN_NONE = ""
table: list[dict[str, int]] = [{'<': 2}, {}, {}]

tnames = ["a", "abbr", "address", "area", "article", "aside", "audio", "b", "base", "bdi", "bdo",
        "blockquote", "body", "br", "button", "canvas", "caption", "cite", "code", "col", "colgroup", "data",
        "datalist", "dd", "del", "dfn", "div", "dl", "dt", "em", "embed", "fieldset", "figcaption",
        "figure", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "head", "header",
        "hgroup", "hr", "html", "i", "iframe", "img", "input", "ins", "kbd", "label", "legend",
        "li", "link", "main", "map", "mark", "math", "menu", "meta", "meter", "nav", "noscript",
        "object", "ol", "optgroup", "option", "output", "p", "picture", "portal", "pre", "progress", "q",
        "rp", "rt", "ruby", "s", "samp", "script", "search", "section", "select", "slot", "small",
        "source", "span", "strong", "style", "sub", "sup", "svg", "table", "tbody", "td", "template",
        "textarea", "tfoot", "th", "thead", "time", "title", "tr", "track", "u", "ul", "var", "video", "wbr"]

tnames = ["button", "html"]

initial_state = 0
final_states = [1]

def generate_tags(names: list[str]) -> list[dict[str, str]]:
    tags = []

    def __get_unique_token(name: str):
        nonlocal tags
        char = name[0]
        num = reduce(lambda n, tag: n + (tag["name"][0] == char), tags, 1)
        return f"{char}{num}"

    for name in names:
        tags.append({
            "name": name,
            "token": __get_unique_token(name)
        })

    return tags

def get_tag_token(tags: list[dict[str, str]], name: str) -> str:
    for tag in tags:
        if tag["name"] == name:
            return tag["token"]

    return TOKEN_NONE

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

tags = generate_tags(tnames)

for tag in tags:
    add_tag(tag["name"])
    add_tag(f"/{tag["name"]}")

for tag in tags:
    assert matches(f"<{tag["name"]}>")
    assert matches(f"</{tag["name"]}>")
    assert not matches(f"{tag["name"]}")
    assert not matches(f"<{tag["name"]}")
    assert not matches(f"</{tag["name"]}")
    assert not matches(f"{tag["name"]}>")
    assert not matches(f"{tag["name"]}/>")
    assert not matches(f"<//{tag["name"]}>")

assert not matches("")
assert not matches("<")
assert not matches(">")
assert not matches("/")
assert not matches("</")
assert not matches("/>")
assert not matches("<>")
assert not matches("</>")
