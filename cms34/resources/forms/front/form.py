# -*- coding: utf-8 -*-
from iktomi.utils import cached_property
from iktomi.cms.forms import Form


class ConstructedForm(Form):
    template = 'forms/constructed_form.html'
    fields = []

    @cached_property
    def json_prepared(self):
        """
        Not all values (e.g. FileFields) can be JSON serialized as is.
        Every field knows how it can be stored as json.
        We are forced to use python data here instead of `self.fields` to
        avoid problems with multiple value fields like FieldBlock or FieldList.
        """
        return {name: self.get_field(name).json_prepared for
                name, value in self.python_data.items() if value is not None}
