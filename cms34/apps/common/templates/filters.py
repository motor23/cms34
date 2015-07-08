import jinja2

__all__ = (
    'remove_from_url',
    'append_to_url',
    'filesizeformat',
    'nl2br',
    'make_breaks',
)

def remove_from_url(url, key):
    scheme, netloc, path, params, query, fragment = urlparse.urlparse(url)
    qs = urlparse.parse_qs(query, True)
    qs.pop(key, None)
    query = urllib.urlencode(qs, True)
    return urlparse.urlunparse((scheme, netloc, path, params, query, fragment))


def append_to_url(url, key, value):
    scheme, netloc, path, params, query, fragment = urlparse.urlparse(url)
    qs = urlparse.parse_qs(query, True)
    qs[key] = value
    query = urllib.urlencode(qs, True)
    return urlparse.urlunparse((scheme, netloc, path, params, query, fragment))


def filesizeformat(value, binary=False):
    if value is not None:
        return jinja2.filters.do_filesizeformat(value, binary)
    return 0


def nl2br(value):
    return jinja2.Markup(value.replace('\n', '<br/>'))

def make_breaks(value):
    return jinja2.Markup(jinja2.Markup("<br/>").join(value.split('\n')))


all_filters = dict((k, v) for k, v in locals().items() if k in __all__)

