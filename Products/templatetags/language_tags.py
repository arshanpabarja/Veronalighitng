from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def switch_language_url(context, lang_code):
    request = context["request"]

    path = request.path

    if lang_code == "en":
        if not path.startswith("/en"):
            return "/en" + path
        return path

    if lang_code == "fa":
        if path.startswith("/"):
            return path[3:] or "/"
        return path

    return path