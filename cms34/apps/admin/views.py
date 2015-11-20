# -*- coding: utf-8 -*-
from iktomi.cms.ajax_file_upload import FileUploadHandler
from iktomi.cms.packer import StaticPacker
from iktomi.cms.stream_handlers import insure_is_xhr

__all__ = ['index', 'tinymce_compressor']

packer = StaticPacker()


def index(env, data):
    insure_is_xhr(env)

    return env.render_to_response('index', dict(
        title=u'Редакторский интерфейс сайта',
        menu='index',
        dashboard=env.dashboard(env),
    ))
