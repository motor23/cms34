# -*- coding: utf-8 -*-
from iktomi.cms.stream_handlers import DeleteItemHandler, insure_is_xhr


class RecursiveDeleteFlagItemHandler(DeleteItemHandler):
    def mark_as_deleted(self, env, item):
        """
        Mark given item as deleted, write message to it's log and remove
        it from tray.
        """
        item.delete()
        log = self.stream.create_log_entry(env, item, 'delete')
        if log is not None:
            env.db.add(log)
        self.clear_tray(env, item)

    def _get_edit_url(self, env, item):
        for stream in env.streams.values():
            url = stream.get_edit_url(env, item)
            if url is not None:
                return url

    def _list_referrers(self, env, item):
        """
        Base version of this method checks all properties of all models that
        points to this item. It is very slow, because it also checks inherited
        relations. This version returns only children for given item and do not
        try to find relations of other models.
        """
        sections = env.db.query(env.models.Section).filter_by(parent_id=item.id)
        refs = {}
        for section in sections:
            url = self._get_edit_url(env, section)
            if url is not None:
                refs[section] = url
        return refs

    def delete_item_handler(self, env, data):
        insure_is_xhr(env)
        item, edit_session, lock_message, filter_form = \
            data.item, data.edit_session, data.lock_message, data.filter_form
        stream = self.stream

        self.insure_is_available(env, item)

        stream_url = stream.url_for(env).qs_set(filter_form.get_data())
        item_url = stream.url_for(env, 'item', item=item.id).qs_set(
            filter_form.get_data())
        delete_url = stream.url_for(env, 'delete', item=item.id) \
            .qs_set(filter_form.get_data())

        all_referrers = self._list_referrers(env, item)
        section_referrers = {ref: url for (ref, url) in all_referrers.items() if
                             getattr(ref, 'parent_id', None) == item.id}
        other_referrers = {ref: url for (ref, url) in all_referrers.items() if
                           ref not in section_referrers}

        if env.request.method == 'POST':
            self.stream.insure_has_permission(env, 'd')

            for section in section_referrers.keys():
                self.mark_as_deleted(env, section)
            self.mark_as_deleted(env, item)

            env.db.commit()

            return env.json({'result': 'success',
                             'location': stream_url})

        data = dict(item=item,
                    item_url=item_url,
                    form_url=delete_url,
                    section_referers=section_referrers,
                    other_referers=other_referrers,
                    title=u'Удаление объекта «%s»' % item,
                    stream=stream,
                    stream_url=stream_url,
                    menu=stream.module_name)
        return env.render_to_response('recursive_delete', data)

    __call__ = delete_item_handler

    def is_available(self, env, item):
        return env.version == 'admin' and super(RecursiveDeleteFlagItemHandler,
                                                self).is_available(env, item)
