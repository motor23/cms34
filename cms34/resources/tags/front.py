from webob.exc import HTTPNotFound
from iktomi.web import match

from .. import ResourceView


class V_RegionSection(ResourceView):
    name='dir'

    @classmethod
    def cases(cls, resources, section):
        return [match('/', name='index') | HTTPNotFound,
                resources.h_section(section)]

    @classmethod
    def _url_for_index(cls, root):
        return None

