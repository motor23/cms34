# -*- coding: utf-8 -*-
from common.streams.std import (
    StreamFactory,
    StdBlock,
    StdBaseField,
    StdStreamSelect,
    StdText,
    std_object_block,
    std_title,
    std_dt,
    std_publish_dt,
)
from common.streams.fields import FieldList, FieldSet
from common.streams.convs import ModelDictConv

class PollQuestion(StdText):
    name='title'
    label=u'Вопрос'

class PollAnswer(StdText):
    name='title'
    label=u'Ответ'

poll_question = PollQuestion()
poll_answer = PollAnswer()


class PollBlock(StdBlock):
    name = 'poll_block'
    label = u'Опрос'
    fields = (
        std_title,
        std_dt,
        std_publish_dt,
    )
    index_fields = sort_fields = filter_fields = item_fields = fields


class Questions(StdBaseField):
    name = 'questions'
    question_model = 'PollQuestion'
    answer_model = 'PollAnswer'
    label = u'Вопросы'
    answers_label = u'Ответы'

    def item_field(self, factory, models):
        answers_fieldset = FieldSet(None,
                conv=ModelDictConv(model=getattr(models, self.answer_model)),
                fields=poll_answer.item_field(factory, models),
        )

        answers_list = FieldList('answers',
                                 order=True,
                                 label=self.answers_label,
                                 field=answers_fieldset,)

        fieldset = FieldSet(None,
            conv=ModelDictConv(model=getattr(models, self.question_model)),
            #XXX
            fields=poll_question.item_field(factory, models) + (
                   answers_list,)
        )
        return FieldList(self.name,
                         order=True,
                         label=self.label,
                         field=fieldset,),


class QuestionsBlock(StdBlock):
    name = 'questions_block'
    label = u'Вопросы'
    item_fields = (
        Questions(),
    )


poll_block = PollBlock()
questions_blocks = QuestionsBlock()


class PollsStreamFactory(StreamFactory):
    Model = 'Poll'
    title = u'Опросы'
    limit = 40
    preview = True

    fields = (
        std_object_block,
        poll_block,
        questions_blocks,
    )
    item_fields = index_field = sort_fields = filter_fields = fields


