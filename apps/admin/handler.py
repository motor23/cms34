# -*- coding: utf8 -*-
from webob.exc import HTTPNotFound
from iktomi.cms.views import auth_required
from iktomi import web
from iktomi.web.filters import static_files, method
from iktomi.web.shortcuts import Rule
from iktomi.cms.flashmessages import flash_message_handler
from iktomi.cms.views import AdminAuth

import models

from . import views as h


def create_handler(app, add_handler=web.cases(), add_auth_handler=web.cases()):

    h_auth = AdminAuth(models.admin.AdminUser, storage=app.cache)

    return flash_message_handler | web.cases(
        static_files(app.cfg.CMS34_STATIC_DIR, app.cfg.CMS34_STATIC_URL),
        static_files(app.cfg.CMS_STATIC_DIR, app.cfg.CMS_STATIC_URL),
        static_files(app.cfg.PRIVATE_MEDIA_DIR, app.cfg.PRIVATE_MEDIA_URL),
        static_files(app.cfg.ADMIN_FORM_TMP_DIR, app.cfg.ADMIN_FORM_TMP_URL),
        static_files(app.cfg.SHARED_MEDIA_DIR, app.cfg.SHARED_MEDIA_URL),
        static_files(app.cfg.ADMIN_MEDIA_DIR, app.cfg.ADMIN_MEDIA_URL),

        # For preview
        # static_files(app.cfg.FRONT_STATIC, app.cfg.FRONT_STATIC_URL),

        Rule('/pack.js', h.packer.js_packer),
        Rule('/pack.css', h.packer.css_packer),

        h_auth.login(),
        h_auth.logout(),

        h_auth | auth_required |
        web.cases(
            Rule('/', h.index, method='GET'),
            method('POST') | web.cases(
                Rule('/_update_lock/<string:item_id>/<string:edit_session>',
                     h.update_lock),
                Rule('/_force_lock/<string:item_id>',
                     h.force_lock),
                Rule('/_release_lock/<string:item_id>/<string:edit_session>',
                     h.release_lock),
            ),
            app.streams.to_app(),
            add_auth_handler,
        ),
        add_handler,
        HTTPNotFound,  # XXX does not work without this
    )
