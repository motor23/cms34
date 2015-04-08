from webob.exc import HTTPNotFound
from iktomi.web import match
from cms34.front import VP_Query, VP_Response, view_handler
from .. import ResourceView

class VP_PersonsQuery(VP_Query):
    model = 'Person'
    order = ('order', 'asc')
    limit = 20

    def create_query(self):
        return self.view.env.db.query(self.get_model())


class V_Person(ResourceView):

    name='person'
    plugins = [VP_Response, VP_PersonsQuery]

    @classmethod
    def cases(cls, resources, section):
        return [match('/', name='index') | cls.h_index]

    @view_handler
    def h_index(self, env, data):
        person = self.query.get_or_404(id=self.section.id)
        return self.response.template('index', dict(person=person))


class V_PersonsList(ResourceView):

    name='persons_list'
    plugins = [VP_Response, VP_PersonsQuery]

    @classmethod
    def cases(cls, resources, section):
        return [match('/', name='index') | cls.h_index,
                resources.h_section(section)]

    @view_handler
    def h_index(self, env, data):
        persons = env.resources.get_sections(
                                         parent_id=self.section.id,
                                         type='person')

        dirs = env.resources.get_sections(
                                         parent_id=self.section.id,
                                         type='dir')
        groups = []
        for group in dirs:
            persons = env.resources.get_sections(
                                        parent_id=group.id,
                                        type='person')
            groups.append((group, persons))
        return self.response.template('index', dict(persons=persons,
                                                    groups=groups))

    def breadcrumbs(self, children=[]):
        children = filter(lambda x: x[0].type=='person', children)
        return ResourceView.breadcrumbs(self, children)
