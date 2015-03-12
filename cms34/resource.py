
class Resource(object):

    name = None

    def __init__(self, section):
        self.section = section
        assert self.name

    def url_for_index(self):
        raise NotImplementedError()

    def url_for_obj(self, obj):
        raise NotImplementedError()


