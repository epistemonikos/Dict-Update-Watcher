# -*- coding: utf-8 -*-

class DictUpdateWatcher(object):
    def __init__(self, dict_):
        self._changed = []
        if isinstance(dict_, dict):
            for key, value in dict_.iteritems():
                if isinstance(value, dict):
                    setattr(self, key, DictUpdateWatcher(value))
                else:
                    setattr(self, key, value)
            self._value = None
            self._changed = []
        else:
            raise Exception("Dict object required")
        
    
    def __getattribute__(self, name):
        element = object.__getattribute__(self, name)
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
            if isinstance(value, DictUpdateWatcher):
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
    