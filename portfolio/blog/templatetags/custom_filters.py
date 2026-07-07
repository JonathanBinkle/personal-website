from django import template
from django.template.defaultfilters import stringfilter
import markdown


register = template.Library()


@register.filter(name="md2html")
@stringfilter
def md2html(md):
    # https://python-markdown.github.io/extensions/
    return markdown.markdown(
        md,
        extensions=[
            "markdown.extensions.fenced_code",
            "markdown.extensions.footnotes",
            "markdown.extensions.tables",
            "markdown.extensions.toc",
            "markdown.extensions.codehilite",
        ],
    )
