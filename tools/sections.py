"""Render the seven academic subpages from their editable Markdown documents."""

import re


def _sections(text, level=2):
    """Split on an exact Markdown heading level; deeper headings stay in the body."""
    parts = re.split(r"(?m)^" + "#" * level + r"[ \t]+([^\n]+?)\s*$", text)
    return parts[0], list(zip(parts[1::2], parts[2::2]))


def _heading(markdown, title, level=2):
    return markdown("#" * level + " " + title.strip())


def _figures(body):
    # Standalone Markdown image followed by an optional italicized caption.
    pattern = r"(?s)<p>\s*(<img\s[^>]*?>)\s*</p>(?:\s*<p><em>((?:(?!</p>).)*?)</em></p>)?"
    def replace(match):
        caption = ("<figcaption>" + match[2] + "</figcaption>") if match[2] else ""
        return '<figure class="research-figure">' + match[1] + caption + "</figure>"
    return re.sub(pattern, replace, body)


def _publications(content, heading):
    prefix = "C" if "conference" in heading.casefold() else "J"
    count = 0
    def label(match):
        nonlocal count
        count += 1
        return match[0] + f'<strong class="citation-id">[{prefix}{count}]</strong> '
    return re.sub(r"<li(?:\s[^>]*)?>", label, content)


def _people(text, markdown):
    intro, members = _sections(text, 3)
    output = [markdown(intro)] if intro.strip() else []
    for name, info in members:
        body = markdown(info)
        portrait = ""
        image = re.match(r"^\s*<p>\s*(<img\s[^>]*?>)\s*</p>", body)
        if image:
            portrait = '<div class="member-portrait">' + image[1] + "</div>"
            body = body[image.end():]
        output.append('<div class="member">' + portrait + '<div class="member-info">'
                      + _heading(markdown, name, 3) + body + "</div></div>")
    return "".join(output)


def render_section(page, source, markdown):
    """Return the article body, excluding the page title handled by the site shell."""
    source = re.sub(r"<!--.*?-->", "", source, flags=re.S)
    intro, groups = _sections(source)
    home = markdown(intro) if intro.strip() else ""
    if page == "Research":
        home = _figures(home)
    output = [f'<div class="academic-section section-{page.lower()}">',
              '<div class="section-intro">' + home + "</div>" if home.strip() else ""]
    for title, body in groups:
        html = _people(body, markdown) if page == "People" else (markdown(body) if body.strip() else "")
        if page == "Research":
            html = _figures(html)
        elif page == "Publications":
            html = _publications(html, title)
        output.append('<section class="academic-group">' + _heading(markdown, title) + html + "</section>")
    output.append("</div>")
    return "\n".join(output)
