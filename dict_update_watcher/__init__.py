# -*- coding: utf-8 -*-
import copy
import pprint


class DictUpdateWatcher(object):
    def __init__(self, dict_={}):
        self._changed = []
        self._ommit = []
        if isinstance(dict_, dict):
            for key, value in dict_.items():
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
        self.__dict__[key] = value
        if key != '_changed':
            self._changed.append(key)

    def __delattr__(self, key):
        # self.__dict__.__delattr__(key)
        del self.__dict__[key]
        self._changed.append(key)

    def __repr__(self):
        return pprint.pformat(self.get_dict(recursive=True))

    def updated_fields(self, pwd=None, ommit=None):
        if not ommit:
            ommit = self._ommit
        # TODO: refactor
        ommit_dict = {}
        for o in ommit:
            ommit_split = o.split('.')
            if not ommit_dict.get(ommit_split[0]):
                ommit_dict[ommit_split[0]] = []
            to_insert_value = ".".join(ommit_split[1:])
            if to_insert_value:
                ommit_dict[ommit_split[0]].append(to_insert_value)
        list_ = []
        for key, value in self.__dict__.items():
            if key in ommit_dict and ommit_dict[key] == []:
                continue
            if key == '_changed' or key == '_ommit':
                continue
            if pwd:
                pwd_current = "%s.%s" % (pwd, key)
            else:
                pwd_current = key
            if isinstance(value, DictUpdateWatcher):
                if len(value._changed) > 0:
                    for changed_element in value._changed:
                        list_.append("%s.%s" % (pwd_current, changed_element))
                    for not_changed_element in value.__dict__:
                        # if pwd not in map(lambda x: '%s.%s' % (pwd, x), self._changed):
                        if key in ommit_dict:
                            received_values = value.updated_fields(pwd_current, ommit=ommit_dict[key])
                        else:
                            received_values = value.updated_fields(pwd_current)
                        for _value in received_values:
                            if len(_value.split('.')) > 1 and _value.split('.')[-2] not in value._changed:
                                list_.append(_value)
                else:
                    if key in ommit_dict:
                        list_.extend(value.updated_fields(pwd_current, ommit=ommit_dict[key]))
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

    def get(self, name, default=None):
        fields = name.split('.')
        to_return_value = self
        try:
            for field in fields:
                to_return_value = to_return_value.__getattribute__(field)
            if to_return_value is None and default is not None:
                return default
            return to_return_value
        except:
            return default

    def set(self, name, value):
        name_splited = name.split('.')
        element = self
        for i, name_part in enumerate(name_splited):
            if i == len(name_splited)-1:
                break
            child = element.get(name_part)
            if not child:
                element.set(name_part, DictUpdateWatcher())
            element = element.get(name_part)
        element.__setattr__(name_splited[-1], value)

    def unset(self, name):
        name_splited = name.split('.')
        element = self
        for i, name_part in enumerate(name_splited):
            if i == len(name_splited)-1:
                break
            child = element.get(name_part)
            if not child:
                element.unset(name_part)
            element = element.get(name_part)
        element.__delattr__(name_splited[-1])

    def get_dict(self, recursive=True):
        dict_ = copy.deepcopy(self.__dict__)
        for key in ['_value', '_changed', '_ommit']:
            try:
                del dict_[key]
            except:
                pass
        if recursive:
            for key, value in dict_.items():
                if isinstance(value, DictUpdateWatcher):
                    dict_[key] = value.get_dict(recursive)
                else:
                    dict_[key] = value
        return dict_

    def keys(self):
        return list(self.get_dict().keys())

    def values(self):
        return list(self.get_dict().values())

    def __cmp__(self, other):
        if not isinstance(other, DictUpdateWatcher):
            return 1
        dict_self = self.__dict__
        dict_other = other.__dict__
        dict_self_keys = list(dict_self.keys()).sort()
        dict_other_keys = list(dict_other.keys()).sort()
        if dict_self_keys != dict_other_keys:
            return 1
        current_cmp_result = 0
        for key, value in dict_self.items():
            round_value = 1
            if dict_other.get(key, {}) == value:
                round_value = 0
            current_cmp_result += round_value
        return current_cmp_result

    def __eq__(self, other):
        return sorted(self.__dict__.keys()) == sorted(self.__dict__.keys())
