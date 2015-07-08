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



class CachedPropertyAttributeError(Exception): pass


class cached_property(object):
    '''Turns decorated method into caching property (method is called once on
    first access to property).'''

    def __init__(self, method, name=None):
        self.method = method
        self.name = name or method.__name__
        self.__doc__ = method.__doc__

    def __get__(self, inst, cls):
        if inst is None:
            return self
        try:
            result = self.method(inst)
        except AttributeError, exc:
            import traceback
            print traceback.format_exc(100)
            raise CachedPropertyAttributeError(exc)
        setattr(inst, self.name, result)
        return result


class property(object):

    def __init__(self, method, name=None):
        self.method = method
        self.name = name or method.__name__
        self.__doc__ = method.__doc__

    def __get__(self, inst, cls):
        result = self.method(inst)
        setattr(inst, self.name, result)
