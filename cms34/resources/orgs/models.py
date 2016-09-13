# -*- coding: utf8 -*-
from itertools import groupby
from cms34.model import hybrid_factory_method
from cms34.model import ModelFactory
from cms34.mixed import xf_id
from cms34.mixed import xf_title
from cms34.mixed import xf_body
from fields import xf_members


class MFY_Org(ModelFactory):
    title = u'Организация'
    model = 'Org'

    fields = [
        xf_id,
        xf_title,
        xf_body,
        xf_members,
    ]

    @hybrid_factory_method.model
    def related_events(self, env):
        """
        Query all EventsListSections for any children events related to this 
        object.
        :return: [(section, [events]), ...]
        """
        result = []
        Event = getattr(self.models, 'Event', None)
        EventsListSection = getattr(self.models, 'EventsListSection', None)
        Event_Section = getattr(self.models, 'Event_Section', None)
        if not all([Event, Event_Section, EventsListSection]):
            return result

        event_list_sections = env.db.query(EventsListSection)
        for section in event_list_sections:
            events = env.db.query(Event) \
                .filter(Event.section_id == section.id) \
                .join(Event_Section) \
                .filter(Event_Section.section_id == self.id) \
                .order_by(Event.dt.desc()) \
                .limit(3) \
                .all()
            if events:
                result.append((section, events))
        return result


class MFY_OrgsListSection(ModelFactory):
    title = u'Список организаций'
    model = 'OrgsListSection'

    fields = [xf_id]
