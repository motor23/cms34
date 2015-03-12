# -*- coding: utf8 -*-
from iktomi.utils import cached_property

from ...model import (
    ModelFactory,
    hybrid_factory_method,
    MF_Img,
)
from ...mixed import (
    xf_id,
)
from .fields import (
    xf_first_name,
    xf_last_name,
    xf_patronymic,
    xf_post,
)

class Person(ModelFactory):
    base_path = 'persons'

    fields = (
        xf_id,
        xf_first_name,
        xf_last_name,
        xf_patronymic,
        xf_post,
        MF_Img('img_orig'),
    )

    @hybrid_factory_method.factory
    @cached_property
    def title(self):
        return u'Персона'

    @title.model
    @property
    def title(self):
        return u' '.join([self.last_name, self.first_name, self.patronymic])


class PersonsListSection(ModelFactory):
    title = u'Список персон'

class PersonSection(ModelFactory):
    title = u'Персона'

