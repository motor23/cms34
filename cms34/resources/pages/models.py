# -*- coding: utf8 -*-
from cms34.model import (
    ModelFactory,
    mf_id,
    mf_title,
    mf_body,
)


class MFY_Page(ModelFactory):
    title = u'Страница'
    model = 'Page'

    fields = [
        mf_id,
        mf_body,
    ]
