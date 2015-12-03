# -*- coding: utf-8 -*-
import os
from iktomi.utils import cached_property
from iktomi.cms.forms import FieldBlock as FieldBlockBase
from iktomi.forms import Field, convs
from iktomi.unstable.forms.convs import Email as EmailConv
from iktomi.unstable.forms.files import FileFieldSet
from .convs import FileFieldSetConv, size_validator, extension_validator
from .widgets import (
    CF_TextInputWidget,
    CF_EmailWidget,
    CF_TextAreaWidget,
    CF_RadioWidget,
    CF_CheckboxWidget,
    CF_SelectWidget,
    CF_FileWidget,
    CF_FieldBlockWidget,
)

"""
Adapter classes to iktomi fields.
`CF_` prefix means 'Constructed form'.
"""


class CF_FormField(Field):
    def __init__(self, *args, **kwargs):
        """
        `Required` argument will be passed to converter, but it should not be
        passed to Field init.
        """
        self.field_obj = kwargs.setdefault('field_obj', None)
        super(CF_FormField, self).__init__(*args, **kwargs)

    size_classnames = {}
    validator_lengths = {}

    def set_size(self):
        if self.field_obj is not None:
            size = self.field_obj.size
            # Update widget
            classname = self.size_classnames.get(size)
            self.widget.add_css_class(classname)

    @cached_property
    def required(self):
        return self.field_obj.required

    @cached_property
    def json_prepared(self):
        return self.clean_value

    def __call__(self, **kwargs):
        """
        Need to adjust field size after field is bound to form.
        """
        _field = super(CF_FormField, self).__call__(**kwargs)
        _field.set_size()
        return _field


class CF_FileFieldSet(FileFieldSet):
    def __init__(self, *args, **kwargs):
        """
        Required argument will be passed to converter, but it should not be
        passed to Field init.
        """
        self._required = kwargs.pop('required', False)
        self.field_obj = kwargs.setdefault('field_obj', None)
        super(CF_FileFieldSet, self).__init__(*args, **kwargs)


class CF_TextField(CF_FormField):
    widget = CF_TextInputWidget()

    size_classnames = {
        'small': 'input_small',
        'medium': 'input_medium',
        'large': 'input_large'
    }

    validator_lengths = {
        'small': 50,
        'medium': 100,
        'large': 250,
    }

    def set_size(self):
        super(CF_TextField, self).set_size()
        # Update converter
        if self.field_obj is not None:
            size = self.field_obj.size
            max_length = self.validator_lengths.get(size, max(
                self.validator_lengths.values()))
            self.conv = self.conv(convs.length(1, max_length))


class CF_EmailTextField(CF_TextField):
    widget = CF_EmailWidget()
    conv = EmailConv(convs.length(3, 100))


class CF_TextareaField(CF_FormField):
    widget = CF_TextAreaWidget()
    conv = convs.Char(convs.length(1, 2000))

    size_classnames = {
        'small': 'textarea_small',
        'medium': 'textarea_medium',
        'large': 'textarea_large'
    }


class CF_EnumChoiceConv(convs.EnumChoice):
    def to_python(self, value):
        value = self.conv.accept(value, silent=True)
        if self.field.multiple:
            value = [val for val in value if val in self.field.options]
        else:
            if value not in self.field.options:
                return None
        return value


class CF_EnumField(CF_FormField):
    conv = CF_EnumChoiceConv

    @cached_property
    def options(self):
        return [_.title for _ in self.field_obj.options]


class CF_RadioField(CF_EnumField):
    widget = CF_RadioWidget()


class CF_CheckboxField(CF_EnumField):
    multiple = True
    conv = CF_EnumChoiceConv(conv=convs.ListOf(convs.Char()))
    widget = CF_CheckboxWidget()

    @cached_property
    def json_prepared(self):
        return u', '.join(self.clean_value)


class CF_SelectField(CF_EnumField):
    widget = CF_SelectWidget()


class CF_FileField(CF_FileFieldSet, CF_FormField):
    _max_file_size = 5 * 1024 * 1024
    _valid_extensions = ['txt', 'doc', 'docx', 'pptx', 'xlsx', 'rtf', 'xls',
                         'pps', 'ppt', 'pdf', 'jpg', 'bmp', 'png', 'tif', 'pcx',
                         'mp3', 'wma', 'avi', 'mp4', 'mkv', 'wmv', 'mov', 'flv']

    widget = CF_FileWidget()
    conv = FileFieldSetConv(size_validator(_max_file_size),
                            extension_validator(_valid_extensions))

    @cached_property
    def max_file_size(self):
        return self._max_file_size

    @cached_property
    def valid_extensions(self):
        return self._valid_extensions

    @cached_property
    def json_prepared(self):
        return os.path.relpath(self.clean_value.path, self.form.env.cfg.ROOT)


class CF_FieldBlock(FieldBlockBase):
    widget = CF_FieldBlockWidget()
