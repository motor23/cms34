from sqlalchemy import (
    Column,
)
from sqlalchemy.dialects.mysql import MEDIUMTEXT as MediumText
from sqlalchemy.orm import relation, deferred
from jinja2 import Markup
from iktomi.db.sqla.types import Html

from .fields import MF_Base

__all__ = (
    'MF_Html',
    'MF_ExpHtml',
    'MF_Body',
    'mf_body',
    'ExpandableMarkup',
)

HtmlMediumText = Html(MediumText)

class MF_Html(MF_Base):
    name = 'html'
    default = ''

    def get_dict(self, models, factory=None):
        html = deferred(Column(HtmlMediumText,
                               nullable=self.nullable,
                               default=self.default))
        return {self.name: html}


class ExpandableMarkup(object):
    '''
        Wrapper for markup which should be preprocessed on front-end.
    '''

    def __init__(self, markup):
        if isinstance(markup, ExpandableMarkup):
            self.markup = markup.markup
        else:
            self.markup = Markup(markup)

    def __len__(self):
        return len(self.markup)

    def __unicode__(self):
        raise RuntimeError('ExpandableMarkup is not converted and ' +
                           'can not be displayed')
    __html__ = __str__ = __unicode__

    def __eq__(self, other):
        if isinstance(other, ExpandableMarkup):
            return self.markup == other.markup
        if isinstance(other, basestring):
            return self.markup == other
        return False


class ExpandableHtml(Html):
    '''
    Column type for markup which should be preprocessed on front-end.
    Made in purpose to ensure that source markup is not occasianally
    outputted on front.
    If it is outputted directly, RuntimeError is raised.
    Use it with corresponding form converter.
    '''

    markup_class = ExpandableMarkup

    def process_bind_param(self, value, dialect):
        if value is not None:
            return unicode(value.markup)


class MF_ExpHtml(MF_Base):

    def get_dict(self, models, factory=None):
        html = deferred(Column(ExpandableHtml(MediumText), nullable=False,
                        default=ExpandableMarkup('')))
        return {self.name: html}


class MF_Body(MF_ExpHtml):
    name = 'body'


mf_body = MF_Body()

