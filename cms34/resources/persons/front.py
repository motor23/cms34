from webob.exc import HTTPNotFound
from iktomi.web import match
from cms34.front import VP_Query, VP_Response, view_handler
from .. import ResourceView

class VP_PersonsQuery(VP_Query):
    model = 'Person'
    order_field = 'order'
    order_asc = True


class V_Person(ResourceView):

    name='person'
    plugins = [VP_Response, VP_PersonsQuery]

    @classmethod
    def cases(cls, sections, section):
        return [match('/', name='index') | cls.h_index]

    @view_handler
    def h_index(self, env, data):
        person = self.query.get_or_404(id=self.section.id)
        return self.response.template('index', dict(person=person))


class V_PersonsList(ResourceView):

    name='persons_list'
    plugins = [VP_Response, VP_PersonsQuery]

    @classmethod
    def cases(cls, sections, section):
        return [match('/', name='index') | cls.h_index,
                sections.h_section(section)]

    @view_handler
    def h_index(self, env, data):
        free_persons = self.query.query.filter_by(
                                         parent_id=self.section.id,
                                         type='person')

        dirs = env.sections.get_sections(
                                         parent_id=self.section.id,
                                         type='dir')
        groups = []
        for group in dirs:
            persons = self.query.query.filter_by(
                                        parent_id=group.id,
                                        type='person')
            groups.append((group, persons))
        return self.response.template('index', dict(free_persons=free_persons,
                                                    groups=groups))

    def breadcrumbs(self, children=[]):
        children = filter(lambda x: x[0].type=='person', children)
        return ResourceView.breadcrumbs(self, children)
