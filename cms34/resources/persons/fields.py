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


class XF_PersonSelect(XF_StreamSelect):
    stream_name = 'persons'
    model = 'Person'


class XF_Person(XF_PersonSelect):
    name = 'person'
    label = u'Персона'
    multiple = False


class XF_Persons(XF_PersonSelect):
    name = 'persons'
    label = u'Персоны'
    multiple = True


xf_first_name = XF_FirstName()
xf_last_name = XF_LastName()
xf_patronymic = XF_Patronymic()
xf_post = XF_Post()
xf_person = XF_Person()
xf_persons = XF_Persons()
