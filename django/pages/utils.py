# Har bir til uchun type mapping
TYPE_MAP = {
    "python": {
        "int": "int",
        "float": "float",
        "string": "str",
        "bool": "bool",
        "list": "List",
        "dict": "Dict"
    },
    "javascript": {
        "int": "number",
        "float": "number",
        "string": "string",
        "bool": "boolean",
        "list": "Array",
        "dict": "Object"
    },
    "csharp": {
        "int": "int",
        "float": "double",
        "string": "string",
        "bool": "bool",
        "list": "List",
        "dict": "Dictionary"
    },
    "cpp": {
        "int": "int",
        "float": "double",
        "string": "string",
        "bool": "bool",
        "list": "vector",
        "dict": "map"
    }
}


def get_type(t, lang="python"):
    """Recursive type converter"""
    mapping = TYPE_MAP[lang]

    if isinstance(t, str):  # oddiy type
        return mapping.get(t, t)

    if isinstance(t, list):  # list ichida type bor
        inner = get_type(t[0], lang)  # birinchi element asosida
        if lang == "python":
            return f"List[{inner}]"
        elif lang == "javascript":
            return f"{inner}[]"  # masalan number[]
        elif lang == "csharp":
            return f"List<{inner}>"
        elif lang == "cpp":
            return f"vector<{inner}>"

    if isinstance(t, dict):  # dict uchun
        k, v = list(t.items())[0]
        key_type = get_type(k, lang)
        val_type = get_type(v, lang)
        if lang == "python":
            return f"Dict[{key_type}, {val_type}]"
        elif lang == "javascript":
            return f"Record<{key_type}, {val_type}>"
        elif lang == "csharp":
            return f"Dictionary<{key_type}, {val_type}>"
        elif lang == "cpp":
            return f"map<{key_type}, {val_type}>"

    return "Any"


def get_code_snippet(task):
    inputs, outputs = task.inputs, task.outputs
    lang = task.language

    # Inputlar bo‘yicha type yozish
    if lang == "python":
        args = ", ".join([f"{name}: {get_type(tp, lang)}" for name, tp in inputs.items()])
        ret = ", ".join([get_type(o, lang) for o in outputs])
        return f"""class Solution:
    def result(self, {args}) -> {ret}:
        pass
"""

    elif lang == "javascript":
        args = ", ".join(inputs.keys())
        ret = ", ".join([get_type(o, lang) for o in outputs])
        return f"""class Solution {{
    result({args}) {{
        // return {ret}
    }}
}}
"""

    elif lang == "csharp":
        args = ", ".join([f"{get_type(tp, lang)} {name}" for name, tp in inputs.items()])
        ret = ", ".join([get_type(o, lang) for o in outputs])
        return f"""public class Solution {{
    public {ret} Result({args}) {{
        // return ...
    }}
}}
"""

    elif lang == "cpp":
        args = ", ".join([f"{get_type(tp, lang)} {name}" for name, tp in inputs.items()])
        ret = ", ".join([get_type(o, lang) for o in outputs])
        return f"""class Solution {{
public:
    {ret} result({args}) {{
        // return ...
    }}
}};
"""

    return "// Language not supported"


def describtion_to_html(content):
    result = ""
    if content is None:
        return "<center><h2 style=\"text-align: center\">Hech nima yo'q</h2></center>"
    for qism in content:
        if qism['type'] == "text":
            result += f"<p>{qism['text']}</p>"
        elif qism['type'] == "code":
            result += f"<div class=\"code-container\"><button class=\"copy-btn\" onclick=\"copyCode(this)\">Copy</button><pre><code class=\"language-{qism['language']}\">{qism['code']}</code></pre></div>"
        elif qism['type'] == "photo":
            result += f"<img src=\"{qism['photo']}\" alt=\"image\">"
        else:
            result += f"<p>{qism}</p>"

    return result