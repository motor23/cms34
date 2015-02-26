def prop_getter(param, factory_param=None):
    def method(self, factory=None):
        value = getattr(self, param)
        if factory_param is None:
            assert value is not None, \
                u'Field name="%s": You must specify %s' % (self.name, param)
        elif value is None:
            value = getattr(factory, factory_param, None)
            assert value is not None, \
                   u'Field name="%s": You must specify %s or factory.%s' % \
                                    (self.name, param, factory_param)
        return value
    return method


