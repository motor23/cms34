# -*- coding: utf8 -*-
from cms34.model import (
    ModelFactory,
    mf_id,
    mf_title,
    mf_body,
    mf_slug,
)


class Page(ModelFactory):
    title = u'Страница'

    fields = [
        mf_id,
        mf_slug,
        mf_title,
        mf_body,
    ]


class PagesSection(ModelFactory):
    title = u'Страницы'
    table = None

