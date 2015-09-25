# -*- coding: utf8 -*-
from markupsafe import Markup
from cms34.model import ExpandableMarkup
from .markup import MarkupExpander, Tag, Link

__all__ = ['replacer', 'replace_tags']


def fix_links(root, item=None, env=None):
    for tag in root.xpath('//a'):
        # Open every link in new window
        # tag.attrib['target'] = '_blank'

        # Replace titles started with "Link:"
        title = tag.attrib.get('title')
        if title and title.startswith('Link:') and tag.text:
            tag.attrib['title'] = tag.text


replacer = MarkupExpander()

replacer.add_filter(Tag(
    name='iktomi_media',
    collection='medias',
    template=lambda target: 'tags/media_{}'.format(target.type),
))

replacer.add_filter(Tag(
    name='iktomi_doclink',
    collection='links_blocks',
    template=lambda target: 'tags/doclink',
))
replacer.add_filter(Tag(
    name='iktomi_files',
    collection='files_blocks',
    template=lambda target: 'tags/files_block',
))

replacer.add_filter(Link(
    template=lambda type: 'tags/{}'.format(type),
    models={
        'person': 'Person',
        'event': 'Event',
        'page': 'Page',
        'term': 'Glossary',
        'file': 'File',
    },
))

replacer.add_filter(fix_links)


def replace_tags(env, item, body):
    """Compatibility layer for old replace mechanism."""

    if isinstance(body, ExpandableMarkup):
        return Markup(replacer.expand(body.markup, item=item, env=env))
    return body
