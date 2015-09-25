# -*- coding: utf-8 -*-

from iktomi.forms import widgets

class CF_FormWidget(widgets.Widget):
    def add_css_class(self, classname):
        if classname:
            class_list = self.classname.split() + classname.split()
            self.classname = ' '.join(class_list)


class CF_FieldBlockWidget(widgets.FieldBlockWidget):
    template = 'forms/widgets/cf_fieldset'


class CF_TextInputWidget(CF_FormWidget):
    template = 'forms/widgets/cf_textinput'
    classname = 'input'


class CF_EmailWidget(CF_TextInputWidget):
    template = 'forms/widgets/cf_email'


class CF_RadioWidget(CF_FormWidget):
    template = 'forms/widgets/cf_radio'
    classname = 'radio'


class CF_CheckboxWidget(CF_FormWidget):
    template = 'forms/widgets/cf_checkbox'
    classname = 'checkbox'


class CF_SelectWidget(CF_FormWidget):
    template = 'forms/widgets/cf_select'
    classname = 'select'


class CF_TextAreaWidget(CF_FormWidget):
    template = 'forms/widgets/cf_textarea'
    classname = 'textarea'


class CF_FileWidget(widgets.FieldSetWidget, CF_FormWidget):
    template = 'forms/widgets/cf_file'
    classname = 'file_input'
