# -*- coding: utf8 -*-
from webob.exc import HTTPNotFound
from iktomi import web
from iktomi.web.filters import static_files, method
from iktomi.web.shortcuts import Rule
from iktomi.cms.flashmessages import flash_message_handler
from iktomi.cms.auth.views import AdminAuth, auth_required
from iktomi.cms.item_lock.views import ItemLockView
from ..common.handlers import h_app

import models

from . import views as h


def create_handler(app):
    h_auth = AdminAuth(models.admin.AdminUser, storage=app.cache)
    item_lock = ItemLockView()
    ext_handlers = []
    if app.preview_enabled:
        h_preview = h_app('/preview', name='preview', app=app.preview_app)
        ext_handlers.append(h_preview)

    return flash_message_handler | web.cases(
        static_files(app.cfg.CMS34_STATIC_DIR, app.cfg.CMS34_STATIC_URL),
        static_files(app.cfg.CMS_STATIC_DIR, app.cfg.CMS_STATIC_URL),
        static_files(app.cfg.STATIC_DIR, app.cfg.STATIC_URL),
        static_files(app.cfg.PRIVATE_MEDIA_DIR, app.cfg.PRIVATE_MEDIA_URL),
        static_files(app.cfg.ADMIN_FORM_TMP_DIR, app.cfg.ADMIN_FORM_TMP_URL),
        static_files(app.cfg.SHARED_MEDIA_DIR, app.cfg.SHARED_MEDIA_URL),
        static_files(app.cfg.ADMIN_MEDIA_DIR, app.cfg.ADMIN_MEDIA_URL),

        Rule('/pack.js', h.packer.js_packer),
        Rule('/pack.css', h.packer.css_packer),

        h_auth.login(),
        h_auth.logout(),

        h_auth | auth_required |
        web.cases(
            Rule('/', h.index, method='GET'),
            item_lock.app,
            app.streams.to_app(),
            web.cases(*ext_handlers),
        ),
        HTTPNotFound,  # XXX does not work without this
    )
