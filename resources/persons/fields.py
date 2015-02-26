# -*- coding: utf8 -*-
from ...mixed.fields import (
    XF_String,
    XF_Text,
    XF_StreamSelect,
)


class XF_FirstName(XF_String):
    name = 'first_name'
    label = u'Имя'

class XF_LastName(XF_String):
    name = 'last_name'
    label = u'Фамилия'

class XF_Patronymic(XF_String):
    name = 'patronymic'
    label = u'Отчество'

class XF_Post(XF_Text):
    name = 'post'
    label = u'Должность'

class XF_Persons(XF_StreamSelect):
    name = 'persons'
    label = u'Персоны'
    stream_name = 'persons'
    model = 'Person'
    multiple = True


xf_first_name = XF_FirstName()
xf_last_name = XF_LastName()
xf_patronymic = XF_Patronymic()
xf_post = XF_Post()
xf_persons = XF_Persons()

