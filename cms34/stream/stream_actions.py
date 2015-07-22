# -*- coding: utf8 -*-
from iktomi.cms.stream_actions import GetAction

class PreviewAction(GetAction):

    item_lock = True
    allowed_for_new = False
    cls = 'preview'
    action = 'preview'
    title = u'Предпросмотр'
    mode = 'internal'

    @property
    def app(self):
        return self

    def url(self, env, item):
        preview_app = env.app.preview_app
        preview_env = preview_app.create_environment(request=env.request)
        preview_app.i18n.set_active_lang(preview_env, env.lang)
        try:
            return preview_env.url_for_obj(item)
        finally:
            preview_env.finalize()

    def external_url(self, env, data, item):
        return '#'

    def is_available(self, env, item):
        return GetAction.is_available(self, env, item) and \
                getattr(env, 'version', None) != 'front' and \
                self.url(env, item)

    def preview(self, env, data):
        return None

    __call__ = preview


