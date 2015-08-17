from webob.exc import HTTPNotFound
from iktomi.web import match
from cms34.front import VP_Response, view_handler
from .. import ResourceView


class V_Person(ResourceView):

    name='person'
    plugins = [VP_Response]

    @classmethod
    def cases(cls, sections, section):
        return [match('/', name='index') | cls.h_index]

    @view_handler
    def h_index(self, env, data):
        return self.response.template('index', dict(person=self.section))


class V_PersonsList(ResourceView):

    name='persons_list'
    plugins = [VP_Response]

    @classmethod
    def cases(cls, sections, section):
        return [match('/', name='index') | cls.h_index,
                sections.h_section(section)]

    @view_handler
    def h_index(self, env, data):
        free_persons = env.sections.get_sections(
                                         parent_id=self.section.id,
                                         type='person')

        dirs = env.sections.get_sections(
                                         parent_id=self.section.id,
                                         type='dir')
        groups = []
        for group in dirs:
            persons = env.sections.get_sections(
                                        parent_id=group.id,
                                        type='person')
            groups.append((group, persons))
        return self.response.template('index', dict(free_persons=free_persons,
                                                    groups=groups))

    def breadcrumbs(self, children=[]):
        if children and children[0][0].type=='dir':
            children = children[1:]
        return ResourceView.breadcrumbs(self, children)
