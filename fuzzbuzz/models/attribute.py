#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from value import Value, UnboundValueError

class AttrChain(Value):

    def __init__(self, lookup_chain):
        self.lookup_chain = lookup_chain
        self.__type = None                          ## TODO TYPES

    def value(self, objs):
        cobjs = objs
        cvalue = None
        for attr in self.lookup_chain:
            cvalue = attr.value(objs, cobjs)
            cobjs = cvalue
        return cvalue

class Attribute(Value):

    def __init__(self, obj, call_chain=None):
        self.obj = obj
        self.call_chain = call_chain
        self.__type = None                          ## TODO TYPES

    def value(self, gobjs, cobjs):
        obj = self.obj.value(cobjs)
        if self.call_chain is not None:
            for params in self.call_chain.value(gobjs):
                assert hasattr(obj, '__call__')
                obj = obj.__call__(*params)
        return obj

class FCall(Value):

    def __init__(self, parameters):
        self.parameters = parameters
        self.__type = None                          ## TODO TYPES

    def value(self, objs):
        return [param.value(objs) for param in self.parameters]

class CallChain(Value):

    def __init__(self, calls):
        self.calls = calls
        self.__type = None                          ## TODO TYPES

    def value(self, objs):
        return [call.value(objs) for call in self.calls]

class Object(Value):

    def __init__(self, name):
        self.name = name
        self.__type = None                          ## TODO TYPES

    def value(self, objs):
        if self.name not in objs:
            raise UnboundValueError
        return objs[self.name]

class SymbolObject(Value):

    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.__type = None                          ## TODO TYPES

    def value(self, objs):
        if (self.name, self.id) not in objs:
            raise UnboundValueError
        return objs[(self.name, self.id)]
