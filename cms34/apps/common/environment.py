# -*- coding:utf8 -*-
import json
from jinja2 import Markup
from webob.exc import HTTPSeeOther
from iktomi import web
from iktomi.cms.app import AdminEnvironment
from iktomi.utils.storage import (
    StorageFrame,
    storage_cached_property,
    storage_method,
    storage_property,
)
from iktomi.web.route_state import RouteState
from ..common.i18n.translation import get_translations
from cms34.utils import cached_property


class Context(object):
    def __init__(self, env):
        self.env = env


class BaseEnvironment(AdminEnvironment):
    def __init__(self, app, request=None, route_state=None, **kwargs):
        StorageFrame.__init__(self, **kwargs)
        self.app = app
        self.cfg = app.cfg
        self.request = request
        if route_state:
            self._route_state = route_state
        elif request:
            self._route_state = RouteState(request)

    @cached_property
    def root(self):
        if self.request:
            return self.app.root.bind_to_env(self._root_storage)
        else:
            return self.app.root

    def finalize(self):
        pass

    @storage_cached_property
    def url_for(self):
        return self.root.build_url

    def url_for_static(self, path):
        return self.cfg.STATIC_URL + path


class Environment(BaseEnvironment):
    Context = Context

    def __init__(self, app, **kwargs):
        self.cfg = app.cfg
        BaseEnvironment.__init__(self, app, **kwargs)

    @cached_property
    def models(self):
        return self.app.models

    @cached_property
    def db(self):
        return self.app.db_maker()

    @cached_property
    def cache(self):
        return self.app.cache

    @cached_property
    def url_for(self):
        return self.root.build_url

    @storage_cached_property
    def template(storage):
        import traceback
        template = storage.app.template_engine()
        try:
            template.env.globals.update(storage.get_template_globals(storage))
        except Exception, exc:
            traceback.print_exc(100)
            raise Exception(exc)
        return template

    def get_template_globals(self, env):
        return dict(
            env=env,
            url_for=self.url_for,
            url_for_static=self.url_for_static,
            context=self.context,
            gettext=self.gettext,
            ngettext=self.ngettext,
        )

    @storage_property
    def render_to_string(storage):
        return storage.template.render_to_string

    @storage_property
    def render_to_response(storage):
        return storage.template.render_to_response

    def json(self, data):
        return web.Response(json.dumps(data), content_type="application/json")

    @storage_method
    def redirect_to(storage, name, qs, **kwargs):
        url = storage.url_for(name, **kwargs)
        if qs:
            url = url.qs_set(qs)
        return HTTPSeeOther(location=str(url))

    @storage_cached_property
    def context(storage):
        return storage.Context(storage)

    def finalize(self):
        self.db.close()

    def get_translations(self, lang):
        return get_translations(self.cfg.I18N_TRANSLATIONS_DIR, lang)

    @cached_property
    def _translations(self):
        return self.get_translations(self.site_lang)

    @storage_method
    def gettext(self, msgid):
        message = self._translations.gettext(unicode(msgid))
        if isinstance(msgid, Markup):
            message = Markup(message)
        return message

    @storage_method
    def ngettext(self, msgid1, msgid2, n):
        message = self._translations.ngettext(unicode(msgid1),
                                              unicode(msgid2), n)
        if isinstance(msgid1, Markup):
            message = Markup(message)
        return message
