def trunc_whitespace(app, doctree, docname):
    from docutils.nodes import Text, paragraph
    if not app.config.japanesesupport_trunc_whitespace:
        return
    for node in doctree.traverse(Text):
        if isinstance(node.parent, paragraph):
            lines = node.astext().splitlines()
            newlines = [lines[0] if lines else '']
            for i in xrange(1, len(lines)):
                line = lines[i]
                prev = lines[i-1]
                if prev and ord(prev[-1]) > 255 and line and ord(line[0]) > 255:
                    newlines[-1] += line
                else:
                    newlines.append(line)
            newtext = '\n'.join(newlines)
            node.parent.replace(node, Text(newtext))

def setup(app):
    app.add_config_value('japanesesupport_trunc_whitespace', True, True)
    app.connect("doctree-resolved", trunc_whitespace)
