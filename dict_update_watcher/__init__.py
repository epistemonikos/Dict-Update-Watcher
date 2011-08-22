# -*- coding: utf-8 -*-

class DictUpdateWatcher(object):
    def __init__(self, dict_ = {}):
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
    
    def get(self, name, default = None):
        fields = name.split('.')
        to_return_value = self
        try:
            for field in fields:
                to_return_value = to_return_value.__getattribute__(field)
            return to_return_value
        except:
            return default
    
    def get_dict(self):
        dict_ = self.__dict__
        del dict_['_value']
        del dict_['_changed']
        return dict_

    def keys(self):
        return self.get_dict().keys()
    
    def values(self):
        return self.get_dict().values()

    def __cmp__(self, other):
        if not isinstance(other, DictUpdateWatcher):
            return 1
        dict_self = self.__dict__
        dict_other = other.__dict__
        dict_self_keys = dict_self.keys().sort()
        dict_other_keys = dict_other.keys().sort()
        if dict_self_keys != dict_other_keys:
            return 1
        current_cmp_result = 0
        for key, value in dict_self.iteritems():
            # print key, value, dict_other.get(key, None)
            round_value = 1
            if dict_other.get(key, {}) == value:
                round_value = 0
            current_cmp_result += round_value
        return current_cmp_result