# -*- coding: utf-8 -*-
import copy

class DictUpdateWatcher(object):
    def __init__(self, dict_ = {}):
        self._changed = []
        self._omit = []
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
    
    def updated_fields(self, pwd = None, omit = None):
        if not omit:
            omit = self._omit
        #TODO: refactor
        omit_dict = {}
        for o in omit:
            omit_split = o.split('.')
            if not omit_dict.get(omit_split[0]):
                omit_dict[omit_split[0]] = []
            to_insert_value = ".".join(omit_split[1:])
            if to_insert_value:
                omit_dict[omit_split[0]].append(to_insert_value)
        list_ = []
        for key, value in self.__dict__.iteritems():
            if key in omit_dict and omit_dict[key] == []:
                continue
            if key == '_changed' or key == '_omit':
                continue
            if pwd:
                pwd_current = "%s.%s" % (pwd,key)
            else:
                pwd_current = key
            if isinstance(value, DictUpdateWatcher):
                if len(value._changed) > 0:
                    for changed_element in value._changed:
                        list_.append("%s.%s" % (pwd_current, changed_element))
                    for not_changed_element in value.__dict__:
                        # if pwd not in map(lambda x: '%s.%s' % (pwd, x), self._changed):
                        if key in omit_dict:
                            received_values = value.updated_fields(pwd_current, omit = omit_dict[key])
                        else:
                            received_values = value.updated_fields(pwd_current)
                        for received_value in received_values:
                            if len(received_value.split('.')) > 1 and received_value.split('.')[-2] not in value._changed:
                                list_.append(received_value)                    
                else:
                    if key in omit_dict:
                        list_.extend(value.updated_fields(pwd_current, omit = omit_dict[key]))
                    else:
                        list_.extend(value.updated_fields(pwd_current))
                    list_.extend(value.updated_fields(pwd_current))
            else:
                if key in self._changed:
                    if pwd:
                        list_.append("%s.%s" % (pwd, key))
                    else:
                        list_.append("%s" % key)
                
                
        return list(set(list_))
    
    def get(self, name, default = None):
        fields = name.split('.')
        to_return_value = self
        try:
            for field in fields:
                to_return_value = to_return_value.__getattribute__(field)
            return to_return_value
        except:
            return default
    
    def set(self, name, value):
        self.__setattr__(name, value)
        
    
    def get_dict(self, recursive = False):
        dict_ = copy.deepcopy(self.__dict__)
        try:
            del dict_['_value']
        except:
            pass
        try:
            del dict_['_changed']
        except:
            pass
        try:
            del dict_['_omit']
        except:
            pass
        if recursive:
            for key, value in dict_.iteritems():
                if isinstance(value, DictUpdateWatcher):
                    dict_[key] = value.get_dict(recursive)
                else:
                    dict_[key] = value
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
            round_value = 1
            if dict_other.get(key, {}) == value:
                round_value = 0
            current_cmp_result += round_value
        return current_cmp_result