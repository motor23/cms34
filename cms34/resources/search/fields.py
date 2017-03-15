# -*- coding: utf-8 -*-

from iktomi.cms.forms import widgets
from cms34.mixed.fields import XF_Slug, IF_String
from iktomi.forms.convs import ValidationError


class IF_SearchSlug(IF_String):
    def create_widget(self, model, factory=None):
        return widgets.TextInput(template='widgets/readonly_textinput')


def global_slug_uniqueness(converter, value):
    """
    Slug should be unique globally.
    """
    current_item = converter.field.form.item
    env = converter.field.form.env
    slug_exists = env.db.query(env.models.Section) \
        .filter_by(slug=value) \
        .filter(env.models.Section.id != current_item.id,
                env.models.Section.state != env.models.Section.DELETED).count()

    if slug_exists:
        raise ValidationError(u'Такой раздел может быть только один.')

    return value


class XF_SearchSlug(XF_Slug):
    initial = 'search'
    permissions = 'rw'
    nullable = False
    validators = [global_slug_uniqueness]

    def _item_field(self, models, factory=None):
        return IF_SearchSlug(self.name,
                             label=self.label,
                             hint=self.hint,
                             max_length=self.max_length,
                             min_length=self.min_length,
                             initial=self.initial,
                             required=self.required,
                             permissions=self.permissions,
                             regex=self.regex,
                             error_regex=self.error_regex,
                             validators=self.validators)


xf_search_slug = XF_SearchSlug()
