# -*- coding: utf-8 -*-
from iktomi.cms.ajax_file_upload import FileUploadHandler
from iktomi.cms.packer import StaticPacker
from iktomi.cms.stream_handlers import insure_is_xhr
from iktomi.cms.views import (update_lock, PostNote,
                              force_lock, release_lock)

__all__ = ['index', 'tinymce_compressor', 'update_lock', 'force_lock',
           'release_lock']

packer = StaticPacker()


def index(env, data):
    insure_is_xhr(env)

    return env.render_to_response('index', dict(
        title=u'Редакторский интерфейс сайта',
        menu='index',
        dashboard=env.dashboard(env),
    ))

