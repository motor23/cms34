# -*- coding: utf-8 -*-
import re
import logging
import copy
import lxml.html
from webob import Response
from iktomi.utils.html import Cleaner
from iktomi.cms.stream_actions import GetAction
from iktomi import web
from iktomi.cms.publishing.model import AdminWithState as WithState

logger = logging.getLogger(__name__)


class HtmlBodyHandler(GetAction):
    for_item = False
    available = [WithState.PRIVATE, WithState.PUBLIC]

    links_block_model = 'EventLinksBlock'
    files_block_model = 'EventFilesBlock'

    media_templates = {
        'photo': 'photolink',
        'photoset': 'photosetlink',
        'video': 'videolink',
        'file': 'filelink'
    }

    @property
    def app(self):
        return web.cases(
            web.match('/doc-link-block/<int:id>',
                      'doc_link_block') | self.doc_link_item,
            web.match('/files-block/<int:id>',
                      'files_block') | self.files_item,
            web.match('/media-link-block/<int:id>',
                      'media_block') | self.media_item,
        )

    def doc_link_item(self, env, data):
        model = getattr(env.models, self.links_block_model)
        doclink_block = env.db.query(model).get(data.id)
        return env.render_to_response('doclink', {
            'doclink_block': doclink_block})

    def files_item(self, env, data):
        model = getattr(env.models, self.files_block_model)
        block = env.db.query(model).get(data.id)
        return env.render_to_response('fileslink', {
            'files_block': block})

    def media_item(self, env, data):
        Media = env.models.Media
        media_item = env.db.query(Media) \
            .filter_by(id=data.id).first()
        if not media_item:
            return Response()
        type = media_item.type
        template = self.media_templates[type]
        return env.render_to_response(template, {
            'media': media_item,
        })


class EventHtmlBodyHandler(HtmlBodyHandler):
    pass


class SectionHtmlBodyHandler(HtmlBodyHandler):
    links_block_model = 'SectionLinksBlock'
    files_block_model = 'SectionFilesBlock'
