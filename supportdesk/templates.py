from collections.abc import Mapping
from html import escape


def render_issue(issue: Mapping[str, object]) -> str:
    title = escape(str(issue["title"]))
    body = escape(str(issue["body"]))
    return (
        "<!doctype html><html><head><meta charset='utf-8'>"
        f"<title>{title}</title></head><body>"
        f"<h1>{title}</h1><p>{body}</p></body></html>"
    )
