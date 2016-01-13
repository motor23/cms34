# -*- coding: utf8 -*-
import re
import lxml.html
import copy

from iktomi.cms.forms import convs, widgets
from iktomi.utils.html import Cleaner

from .item_fields import IF_Simple
from ..model.html_fields import ExpandableMarkup

__all__ = (
    'IF_Html',
    'IF_ExpHtml',
)


class IF_Html(IF_Simple):
    name = 'html'
    label = u'Текст'
    allowed_elements = ('a', 'p', 'li', 'ul', 'ol', 'i', 'b',
                        'blockquote', 'hr', 'h1', 'h2', 'h3', 'br',
                        'table', 'tr', 'td')
    allowed_protocols = ('http', 'https', 'ftp')
    allowed_attributes = ('href', 'src', 'alt', 'colspan',
                          'title', 'class', 'rel')
    button_blocks = widgets.WysiHtml5.button_blocks
    stylesheets = ()

    def create_conv(self, models, factory=None):
        return convs.Html(
            allowed_elements=self.allowed_elements,
            allowed_protocols=self.allowed_protocols,
            allowed_attributes=self.allowed_attributes,
            button_blocks=self.button_blocks,
            stylesheets=self.stylesheets,
            required=self.required)

    def create_widget(self, models, factory=None):
        return widgets.WysiHtml5(
            button_blocks=self.button_blocks,
            stylesheets=self.stylesheets,
        )


class ExpandableHtmlConv(convs.Html):
    '''
        Converter for ExpandableHtml column type, used
        for markup which should be preprocessed on front-end.
    '''

    def to_python(self, value):
        value = convs.Html.to_python(self, value)
        return ExpandableMarkup(value)

    def from_python(self, value):
        # if isinstance(value, ExpandableMarkup):
        if value.__class__.__name__ == 'ExpandableMarkup':
            value = value.markup
        return convs.Html.from_python(self, value)


# XXX assignment is here since the form is common
_transcript_class_match = re.compile(
    r'^(person|theme|index|assignment)_(\d+)$').match

text_align_classes = ['text-align-right', 'text-align-center']

_p_cls_test = lambda x: x == 'transcript-p-hidden' or \
                        _transcript_class_match(x) or \
                        x in text_align_classes


class EnhancedCleaner(Cleaner):
    a_without_href = False

    def extra_clean(self, doc):
        super(EnhancedCleaner, self).extra_clean(doc)
        wrap_inlines(
            doc,
            blocks=['iktomi_doclink', 'iktomi_media', 'iktomi_files', 'table',
                    'p', 'blockquote'],
        )

        for tag in doc.xpath('//p[not(text())]/br[1]'):
            parent = tag.getparent()
            if parent is not None:
                for child in parent.getchildren():
                    if child.tag != 'br':
                        break
                else:
                    tag.drop_tag()
                    parent.drop_tag()


def wrap_inlines(doc, tag='p', blocks=()):
    children = list(doc)
    i = 0
    el = None

    if doc.text:
        el = lxml.html.Element(tag)
        el.text, doc.text = doc.text, ''

    while i < len(children):
        item = children[i]
        if item.tag not in blocks:
            if el is None:
                el = lxml.html.Element(tag)
            el.append(copy.deepcopy(item))
            item.tail = ''
            item.drop_tree()
        else:
            break
        i += 1
    if el is not None:
        doc.insert(0, el)

    def fold_block(current, rest):
        el = None
        if current.tail and not current.tail.isspace():
            el = lxml.html.Element('p')
            el.text, current.tail = current.tail, ''
        for item in rest:
            if item.tag not in blocks:
                if el is None:
                    el = lxml.html.Element('p')
                el.append(copy.deepcopy(item))
                item.tail = ''
                item.drop_tree()
            else:
                break
        if el is not None:
            current.addnext(el)
            return True

    while True:
        i = 0
        children = list(doc)
        while i < len(children):
            if children[i].tag in blocks:
                if fold_block(children[i], children[i + 1:]):
                    break
            i += 1
        if i >= len(children):
            break


class IF_ExpHtml(IF_Html):
    allowed_elements = ('a', 'p', 'li', 'ul', 'ol', 'i', 'b', 'u',
                        'blockquote', 'hr', 'h1', 'h2', 'h3', 'h4', 'br',
                        'table', 'tr', 'td', 'iktomi_doclink', 'iktomi_media',
                        'iktomi_files', 'table', 'td', 'tr')
    allowed_attributes = ('data-align', 'item_id', 'id',
                          'class', 'href', 'colspan')
    allowed_protocols = ('model', 'http')
    allowed_classes = dict(convs.Html.allowed_classes,
                           p=_p_cls_test,
                           hr=('block-links', 'block-media', 'block-files'))
    button_blocks = [
        ('justify', ['justifyCenter', 'justifyRight']),
        ('inline', ['bold', 'italic', 'underline']),
        ('block', ['headings', 'sup', 'sub', 'blockquote']),
        ('lists', ['insertunorderedlist', 'insertorderedlist',
                   'outdent', 'indent']),
        ('advanced', ['createLinkAdvanced', 'doclink', 'table', 'extrachars']),
        ('history', ['undo', 'redo']),
        ('html', ['html']),
    ]
    stylesheets = ('/cms34-static/css/wysihtml5-content.css',
                   '/cms34-static/css/wysihtml5-blocks.css',)

    def create_conv(self, models, factory=None):
        return ExpandableHtmlConv(
            Cleaner=EnhancedCleaner,
            allowed_elements=self.allowed_elements,
            allowed_protocols=self.allowed_protocols,
            allowed_attributes=self.allowed_attributes,
            allowed_classes=self.allowed_classes,
            button_blocks=self.button_blocks,
            stylesheets=self.stylesheets,
            required=self.required)
