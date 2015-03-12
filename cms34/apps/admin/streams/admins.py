# -*- coding: utf-8 -*-

from iktomi.forms import shortcuts, Field
from models.admin import AdminUser as Model, AdminGroup
from iktomi.cms.forms import ModelForm, convs, widgets
from iktomi.cms.stream import ListFields, handlers, Stream as BaseStream

permissions = {'admin': 'rwxcd'}

ROLES = [
    ('wheel',   u'Полный доступ'),
    ('admin',   u'Администратор'),
    ('publisher', u'Выпускающий редактор'),
    ('editor',  u'Редактор'),
    ('struct',  u'Редактор структуры'),
]

title = u"Редакторы"

list_fields = ListFields(('login', u'Логин'),
                         ('name', u'Имя'),
                         ('email', u'email'))


def clean_password(conv, value):
    form = conv.field.form
    if not value and (not form.item or form.item.id is None):
        raise convs.ValidationError(u'Обязательное поле')
    return value


class ItemForm(ModelForm):

    fields = [
        Field('name',
              conv=convs.Char(convs.length(3, 250), required=False),
              label=u"Имя"),
        Field('email',
              conv=convs.Char(convs.length(0, 200), required=False),
              label=u"E-mail"),
        Field('login',
              conv=convs.Char(
                  convs.DBUnique(
                      model=Model,
                      message=u'Объект с таким значением уже существует'),
                  convs.length(3, 250),
              ),
              label=u"Логин"),
        shortcuts.PasswordSet('password',
                              filters=(clean_password,),
                              widget=widgets.FieldSetWidget(
                                  template='widgets/fieldset-line'),
                              label=u'пароль',
                              confirm_label=u'подтверждение'),
        Field('groups', label=u'Роли',
              conv=convs.ListOf(
                  convs.ModelChoice(model=AdminGroup,
                                    title_field='ru_title')),
              widget=widgets.CheckBoxSelect())
    ]

    def update__password(self, obj, name, value):
        if value is not None:
            obj.set_password(value)

    def update__roles(self, obj, name, value):
        if obj.roles is not None and 'wheel' in obj.roles and \
                'wheel' not in value:
            value.append('wheel')
        if (not obj.roles or 'wheel' not in obj.roles) and 'wheel' in value:
            value.remove('wheel')
        obj.roles = value


class EditItemHandler(handlers.EditItemHandler):
    def get_item_form(self, stream, env, item, initial, draft):
        form = super(EditItemHandler, self).get_item_form(
            stream, env, item, initial, draft)
        password_field = form.get_field('password')
        if item is None:
            password_field.conv.required = True
        return form


class Stream(BaseStream):
    core_actions = [handlers.StreamListHandler(),
                    EditItemHandler(),
                    handlers.DeleteItemHandler(),
                    ]
