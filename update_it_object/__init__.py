# -*- coding: utf-8 -*-

class UpdateItObject(object):
    def __init__(self, element):
        self._changed = []
        if isinstance(element, dict):
            for key, value in element.iteritems():
                setattr(self, key, UpdateItObject(value))
            self._value = None
            self._leaf = False
        elif isinstance(element, (list, tuple)):
            self._value = [UpdateItObject(x) for x in element]
            self._leaf = False
        else:
            self._value = element
            self._leaf = True
        self._changed = []
    
    def __getattribute__(self, name):
        element = object.__getattribute__(self, name)
        if isinstance(element, UpdateItObject):
            if element._leaf:
                return element._value
        return element

    def __setattr__(self, key, value):
        if key == '_changed':
            self.__dict__[key] = value
            return None
        self.__dict__[key] = value
        self._changed.append(key)
    
    def updated_fields(self, pwd = None):
        list_ = []
        for key, value in self.__dict__.iteritems():
            if key == '_changed':
                continue
            if pwd:
                pwd_current = "%s.%s" % (pwd,key)
            else:
                pwd_current = key
            if isinstance(value, UpdateItObject):
                if len(value._changed) > 0:
                    for changed_element in value._changed:
                        list_.append("%s.%s" % (pwd_current, changed_element))
                else:
                    list_.extend(value.updated_fields(pwd_current))
        return list_
    
    def get(self, name):
        fields = name.split('.')
        to_return_value = self
        try:
            for field in fields:
                to_return_value = to_return_value.__getattribute__(field)
            return to_return_value
        except:
            return None
    