# coding: utf-8
import markupsafe
import urlparse

import lxml.html
import lxml.etree


class MarkupExpander(object):

    def __init__(self):
        self.replacements = []
        self.filters = []

    def add_replacement(self, pattern, replacement):
        self.replacements.append((pattern, replacement))

    def add_filter(self, filter):
        self.filters.append(filter)

    def apply_replacements(self, value):
        for pattern, replacement in self.replacements:
            value = value.replace(pattern, replacement)
        return value

    def apply_filters(self, value, **kwargs):
        try:
            root = lxml.html.fragment_fromstring(value, create_parent=True)
            for filter in self.filters:
                filter(root, **kwargs)
        except lxml.etree.XMLSyntaxError as e:
            return value
        else:
            return self.stringify(root)

    def expand(self, value, **kwargs):
        value = self.apply_replacements(value)
        value = self.apply_filters(value, **kwargs)
        return value

    @staticmethod
    def stringify(tag, encoding='utf-8'):
        head = tag.text or ''
        tail = ''.join([
            lxml.html.tostring(child, encoding=encoding)
            for child in tag.iterchildren()
        ])
        return ''.join([head, tail.decode(encoding)])


def replace_tag_with_text(tag, value):
    parent = tag.getparent()
    if parent is not None:
        fragments = lxml.html.fragments_fromstring(value)
        if fragments and isinstance(fragments[0], basestring):
            text = fragments.pop(0)
            index = parent.index(tag)
            if index > 0:
                element = parent.getchildren()[index - 1]
                element.tail = (element.tail or '') + text
            else:
                parent.text = (parent.text or '') + text
        for fragment in fragments:
            parent.insert(parent.index(tag), fragment)
        tag.drop_tree()


class Tag(object):
    name = None
    template = None
    collection = None

    def __init__(self, name=None, template=None, collection=None):
        self.name = self.name or name
        self.template = self.template or template
        self.collection = self.collection or collection

    def __call__(self, root, item=None, env=None):
        expr = '//{}'.format(self.name)
        for tag in root.xpath(expr):
            self.replace(tag, item=item, env=env)

    def replace(self, tag, item=None, env=None):
        try:
            id = int(tag.attrib.get('item_id'))
        except (TypeError, ValueError):
            pass
        else:
            collection = getattr(item, self.collection)
            target = next((b for b in collection if b.id == id), None)
            if target:
                if callable(self.template):
                    template = self.template(target)
                else:
                    template = self.template
                content = env.render_to_string(template, tag=tag, item=item, target=target)
                return replace_tag_with_text(tag, content)
        tag.drop_tree()


class Link(object):
    template = None
    models = None

    def __init__(self, template=None, models=None, tag=None):
        self.template = self.template or template
        self.models = self.models or models

    def __call__(self, root, item=None, env=None):
        expr = '//a[starts-with(@href, "model://")]'
        for tag in root.xpath(expr):
            self.replace(tag, item=item, env=env)

    def replace(self, tag, item=None, env=None):
        href = tag.attrib['href']
        parts = urlparse.urlparse(href)
        type, path = parts.netloc, parts.path[1:]
        try:
            id = int(path)
        except (TypeError, ValueError):
            pass
        else:
            model_name = self.models.get(parts.netloc)
            if model_name:
                model_cls = getattr(env.models, model_name)
                if model_cls:
                    target = env.db.query(model_cls).get(id)
                    if target:
                        if callable(self.template):
                            template = self.template(type)
                        else:
                            template = self.template
                        inner_html = markupsafe.Markup(MarkupExpander.stringify(tag))
                        content = env.render_to_string(template, tag=tag, item=item, target=target, inner_html=inner_html)
                        return replace_tag_with_text(tag, content)
        tag.drop_tree()
