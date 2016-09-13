# -*- coding: utf8 -*-
from iktomi.utils import cached_property

from ...model import (
    ModelFactory,
    hybrid_factory_method,
    MF_Img,
)
from ...mixed import (
    xf_id,
)
from .fields import (
    xf_first_name,
    xf_last_name,
    xf_patronymic,
    xf_post,
)


class MFY_Person(ModelFactory):
    model = 'Person'
    title = u'Персона'
    base_path = 'person'

    fields = [
        xf_id,
        xf_first_name,
        xf_last_name,
        xf_patronymic,
        xf_post,
        MF_Img('img_orig'),
    ]

    # @hybrid_factory_method.factory
    # @cached_property
    # def title(self):
    #     return u'Персона'
    # 
    # @title.model
    # @property
    # def title(self):
    #     return u' '.join([self.last_name, self.first_name, self.patronymic])

    @hybrid_factory_method.model
    def related_events(self, env):
        """
        Query all EventsListSections for any children events related to
        this object.
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


class PersonsListSection(ModelFactory):
    title = u'Список персон'

    fields = [xf_id]
