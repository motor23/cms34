from webob.exc import HTTPNotFound
from iktomi.web import match
from cms34.front import VP_Query, VP_Response, view_handler
from .. import ResourceView

class VP_OrgsQuery(VP_Query):
    model = 'Org'
    order = ('order', 'asc')
    limit = 20

    def create_query(self):
        return self.view.env.db.query(self.get_model())


class V_Org(ResourceView):

    name='org'
    plugins = [VP_Response, VP_OrgsQuery]

    @classmethod
    def cases(cls, sections, section):
        return [match('/', name='index') | cls.h_index]

    @view_handler
    def h_index(self, env, data):
        org = self.query.get_or_404(id=self.section.id)
        return self.response.template('index', dict(org=org))


class V_OrgsList(ResourceView):

    name='orgs_list'
    plugins = [VP_Response, VP_OrgsQuery]

    @classmethod
    def cases(cls, sections, section):
        return [match('/', name='index') | cls.h_index,
                sections.h_section(section)]

    @view_handler
    def h_index(self, env, data):
        orgs = env.sections.get_sections(
                                         parent_id=self.section.id,
                                         type='org')

        dirs = env.sections.get_sections(
                                         parent_id=self.section.id,
                                         type='dir')
        groups = []
        for group in dirs:
            orgs = env.sections.get_sections(
                                        parent_id=group.id,
                                        type='org')
            groups.append((group, orgs))
        return self.response.template('index', dict(orgs=orgs,
                                                    groups=groups))

    def breadcrumbs(self, children=[]):
        children = filter(lambda x: x[0].type=='org', children)
        return ResourceView.breadcrumbs(self, children)

