# -*- coding: utf8 -*-
from iktomi.utils import cached_property

from common.models.std import (
    Factory,
    add_id,
    add_dt,
    add_publish_dt,
    add_title,
    add_order,
    add_base_methods,
    AddO2MRelation,
    AddM2ORelation,
)


class PollAnswer(Factory):
    title = u'Ответ'
    fields = [add_id,
              add_title,
              add_order,
              AddM2ORelation('poll', 'PollQuestion'),
             ]

class AddAnswers(AddO2MRelation):
    ordered = True
    field_factory = PollAnswer

    def register(self, factory):
        self.field_factory('BaseModel').register()

    @cached_property
    def cls_name(self):
        return self.field_factory.__name__


add_answers = AddAnswers('answers')


class PollQuestion(Factory):
    title = u'Вопрос'
    fields = [add_id,
              add_title,
              add_order,
              AddM2ORelation('poll', 'Poll'),
              add_answers,]


MF_List(fields=[xx,xx,xx])

class AddQuestions(AddO2MRelation):
    ordered = True
    field_factory = PollQuestion

    def register(self, factory):
        self.field_factory('BaseModel').register()

    @cached_property
    def cls_name(self):
        return self.field_factory.__name__


add_questions = AddQuestions('questions')


class Poll(Factory):
    title = u'Опрос'

    fields = [
        add_id,
        add_dt,
        add_publish_dt,
        add_title,
        add_base_methods,
        add_questions,
    ]


