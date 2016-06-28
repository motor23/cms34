# -*- coding: utf-8 -*-
from datetime import datetime
from webob.exc import HTTPBadRequest
from iktomi.web import match
from iktomi.utils import cached_property
from cms34.front.view import view_handler, iframe_json
from cms34.resources import ResourceView
from cms34.front.plugins import VP_Response, VP_Query
from cms34.resources.forms.front import ConstructedForm
from cms34.apps.common.handlers import no_preview
from cms34.apps.common.flood import check_flood
from cms34.apps.common.caching import cache
from cms34.apps.common.guarded_urls import GuardedMatch


class LetterForm(ConstructedForm):
    @classmethod
    def _init_fields(cls, form_tree):
        fields = []
        for field in form_tree:
            if field is None:
                # field is unpublished
                continue
            front_view_cls = field.front_view_cls
            if hasattr(field, 'fields'):
                subfields = cls._init_fields(field.fields)
                front_field_view = front_view_cls(title=field.title,
                                                  fields=subfields,
                                                  field_obj=field)
            else:
                front_field_view = front_view_cls(name=field.name,
                                                  label=field.title,
                                                  field_obj=field)

            fields.append(front_field_view)
        return fields

    @cached_property
    def json_prepared(self):
        """
        Export list of tuples, to save the order.
        """
        data = []
        for block in self.fields:
            data.append((block.title, block.json_prepared))
        return data

    @classmethod
    def init(cls, env, form_tree):
        cls.fields = cls._init_fields(form_tree)
        return cls(env)


class VP_LetterSectionQuery(VP_Query):
    model = 'LettersSection'
    order_field = 'id'
    order_asc = True
    limit = 20


class V_LettersSection(ResourceView):
    name = 'letters'
    title = u'Обращение'

    plugins = [VP_Response, VP_LetterSectionQuery]

    SUCCESS_TPL = u'Ваше обращение поступило на почтовый сервер и ' \
                  u'будет рассмотрено отделом по работе с обращениями ' \
                  u'граждан. Номер Вашего обращения: {id}.'
    FLOOD_TPL = u'Извините, отправка писем с Вашего IP-адреса ' \
                u'заблокирована до %02d:%02d %s.'

    form = LetterForm

    def _get_form(self):
        return self.form.init(self.env, self.section.form)

    def _get_model(self):
        return self.env.shared_models.Letter

    @classmethod
    def cases(cls, sections, section):
        return [
            match('/', name='rules') | cache(False) | cls.h_rules,
            GuardedMatch('/form/', name='form', methods=('GET', 'POST')) |
            cache(False) | cls.h_form,
            sections.h_section(section),
        ]

    @view_handler
    def h_rules(self, env, data):
        rules = getattr(self.section, 'rules', None)
        if rules and rules.markup:
            return self.response.template('rules', dict(letter=self.section))
        return self.response.redirect_to(self.root.form, qs=None)

    def _check_flood(self, env, activity='subscribe'):
        allowed_at = check_flood(env, activity, True)
        env.db.commit()
        if allowed_at is not None:
            message = self.FLOOD_TPL % (allowed_at.hour,
                                        allowed_at.minute,
                                        env.lang.date(allowed_at))
            return message

    @view_handler
    def h_form(self, env, data):
        letter_model = self._get_model()
        form = self._get_form()
        is_iframe = 'iframe' in env.request.POST

        if env.request.method == 'POST':
            response_data = {'valid': None, 'errors': None, 'message': None}

            if form.accept(env.request.POST):
                preview = getattr(env.app.cfg, 'PREVIEW', None)
                if preview:
                    raise HTTPBadRequest("Form submit is forbidden in preview")
                flood_msg = self._check_flood(env, self.name)
                if flood_msg:
                    response_data['message'] = flood_msg
                    response_data['valid'] = True
                    return env.json(response_data)

                letter = letter_model(dt=datetime.now(),
                                      section_id=self.section.id,
                                      letter_json=form.json_prepared)
                env.db.add(letter)
                env.db.commit()
                letter_id = '{}_{}'.format(self.env.cfg.APP_ID, letter.id)
                response_data['success'] = True
                response_data['message'] = self.SUCCESS_TPL.format(
                    id=letter_id)

            response_data['valid'] = form.is_valid
            response_data['errors'] = form.errors

            to_json = iframe_json if is_iframe else env.json
            return to_json(response_data)
        else:
            return self.response.template('form', dict(
                letter=self.section,
                form=form,
            ))

    @classmethod
    def _url_for_index(cls, root):
        return root.rules
