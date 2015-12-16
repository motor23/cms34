# -*- coding: utf-8 -*-
import os
from iktomi.utils import cached_property
from iktomi.cms.forms.convs import ValidationError, Char
from iktomi.unstable.db.files import TransientFile
from iktomi.unstable.forms.files import (
    FileFieldSetConv as BaseFileFieldSetConv
)


class FileFieldSetConv(BaseFileFieldSetConv):
    @cached_property
    def file_manager(self):
        return self.env.app.shared_file_manager


def size_validator(max_file_size):
    def _validate(conv, value):
        if isinstance(value, TransientFile):
            if os.path.getsize(value.path) > max_file_size:
                raise ValidationError(u'Размер файла выше допустимого.')
        return value

    return _validate


def extension_validator(valid_extensions):
    def _validate(conv, value):
        if isinstance(value, TransientFile):
            filename, ext = os.path.splitext(value.path)
            ext = ext.replace('.', '')
            if ext.lower() not in valid_extensions:
                raise ValidationError(u'Недопустимое расширение файла.')

        return value

    return _validate


class PhoneConv(Char):
    regex = r'^(\+\d{1,2})?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{2}[\s.-]?\d{2}$'


class ZipcodeConv(Char):
    regex = r'^[0-9]{6}$'
