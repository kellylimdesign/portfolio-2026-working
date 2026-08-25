import re, sys

def scope_css(css_text, prefix):
    """Prefix every top-level selector with `prefix `, recursing into @media/@supports.
    Leaves :root, @keyframes, @font-face untouched. Collects bare body/html rules
    separately (returned) instead of scoping them, since they can't be meaningfully
    scoped to a descendant container."""
    # strip comments FIRST — otherwise commas inside a comment preceding a
    # selector get treated as selector-list separators and get a prefix
    # spliced into them, which can invalidate the whole real selector list
    css_text = re.sub(r'/\*.*?\*/', '', css_text, flags=re.S)
    global_rules = []  # list of (selector, body) for body/html

    def process(text):
        out = []
        i, n = 0, len(text)
        while i < n:
            while i < n and text[i] in ' \t\r\n':
                i += 1
            if i >= n:
                break
            brace = text.find('{', i)
            if brace == -1:
                out.append(text[i:])
                break
            header = text[i:brace]
            depth = 1
            j = brace + 1
            while j < n and depth > 0:
                if text[j] == '{':
                    depth += 1
                elif text[j] == '}':
                    depth -= 1
                j += 1
            body = text[brace + 1:j - 1]
            header_s = header.strip()
            if header_s.startswith('@media') or header_s.startswith('@supports'):
                inner = process(body)
                out.append(f"{header}{{{inner}}}")
            elif header_s.startswith('@keyframes') or header_s.startswith('@font-face') or header_s.startswith('@page'):
                out.append(f"{header}{{{body}}}")
            elif header_s == ':root':
                out.append(f"{header}{{{body}}}")
            elif (header_s in ('body', 'html') or re.match(r'^(body|html)\s*,', header_s)
                  or header_s.startswith('.speaker-notes')):
                # body/html can't be meaningfully scoped to a descendant container.
                # .speaker-notes-* is JS-created and appended straight to <body>
                # (see each deck's script), i.e. OUTSIDE either phase container —
                # a scoped selector would never match those elements at all.
                global_rules.append((header_s, body))
                # omit from scoped output entirely; caller merges globals separately
            else:
                selectors = [s.strip() for s in header_s.split(',')]
                scoped = ", ".join(f"{prefix} {s}" for s in selectors if s)
                out.append(f"{scoped}{{{body}}}")
            i = j
        return "\n".join(out)

    scoped_css = process(css_text)
    return scoped_css, global_rules


if __name__ == "__main__":
    path, prefix, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    text = open(path).read()
    m = re.search(r'<style>(.*?)</style>', text, re.S)
    css = m.group(1)
    scoped, globals_ = scope_css(css, prefix)
    open(out_path, "w").write(scoped)
    print(f"{path}: scoped {len(scoped)} chars, {len(globals_)} global (body/html) rules found:")
    for sel, body in globals_:
        print(f"  {sel} {{ {body.strip()} }}")
