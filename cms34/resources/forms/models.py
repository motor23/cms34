# -*- coding: utf-8 -*-

from iktomi.utils import cached_property
from cms34.mixed.fields import xf_id, xf_order, xf_title
from cms34.model import (
    ModelFactory,
    MFP_SingleTableTypes,
    hybrid_factory_method
)
from .fields import (
    xf_field_size,
    xb_form_blocks,
    xf_required,
    xf_field_name,
    xf_field_type,
    xf_options_list,
)

from .front.fields import (
    CF_TextField,
    CF_EmailTextField,
    CF_TextareaField,
    CF_RadioField,
    CF_CheckboxField,
    CF_SelectField,
    CF_FileField,
)


class MFY_TextField(ModelFactory):
    name = 'FormTextField'
    title = u'Текстовое поле'

    @hybrid_factory_method.model
    @cached_property
    def front_view_cls(self):
        return CF_TextField


class MFY_EmailTextField(ModelFactory):
    name = 'FormEmailTextField'
    title = u'Email'

    @hybrid_factory_method.model
    @cached_property
    def front_view_cls(self):
        return CF_EmailTextField


class MFY_ParagraphTextField(ModelFactory):
    name = 'FormParagraphTextField'
    title = u'Параграф'

    @hybrid_factory_method.model
    @cached_property
    def front_view_cls(self):
        return CF_TextareaField


class MFY_RadioField(ModelFactory):
    name = 'FormRadioField'
    title = u'Радио'

    @hybrid_factory_method.model
    @cached_property
    def front_view_cls(self):
        return CF_RadioField


class MFY_CheckboxField(ModelFactory):
    name = 'FormCheckboxField'
    title = u'Флаги'

    @hybrid_factory_method.model
    @cached_property
    def front_view_cls(self):
        return CF_CheckboxField


class MFY_SelectField(ModelFactory):
    name = 'FormSelectField'
    title = u'Выпадающий список'

    @hybrid_factory_method.model
    @cached_property
    def front_view_cls(self):
        return CF_SelectField


class MFY_FileField(ModelFactory):
    name = 'FormFileField'
    title = u'Файл'

    @hybrid_factory_method.model
    @cached_property
    def front_view_cls(self):
        return CF_FileField


class MFY_FormField(ModelFactory):
    title = u'Поле'
    model = 'FormField'
    plugins = [MFP_SingleTableTypes]

    types = [
        ('text', MFY_TextField),
        ('email', MFY_EmailTextField),
        ('paragraph_text', MFY_ParagraphTextField),
        ('radio', MFY_RadioField),
        ('checkbox', MFY_CheckboxField),
        ('select', MFY_SelectField),
        ('file', MFY_FileField),
    ]

    type_choices = [(_, factory.title) for _, factory in types]

    fields = [
        xf_id,
        xf_order,
        xf_field_type,
        xf_required,
        xf_title,
        xf_field_name,
        xf_field_size,
        xf_options_list,
    ]


class MFY_Form(ModelFactory):
    title = u'Конструктор формы'
    model = 'Form'

    fields = [
        xf_id,
        xb_form_blocks,
    ]
