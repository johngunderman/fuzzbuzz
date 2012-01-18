#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from value import Value

def get(o, name):
    try:
        return o[name]
    except KeyError:
        return getattr(o, name)

class AttrChain(Value):

    def __init__(self, objs, lookup_chain):
        cobjs = objs
        cvalue = None
        for attr in lookup_chain:
            cvalue = attr((objs, cobjs)).value
            #import pdb
            #pdb.set_trace()
            cobjs = cvalue
        type = None                          ## TODO TYPES
        value = cvalue
        super(AttrChain, self).__init__(objs, type, value)

class Attribute(Value):

    def __init__(self, gcobjs, obj, call_chain=None):
        gobjs, cobjs = gcobjs
        obj = obj(cobjs).value
        if call_chain is not None:
            for params in call_chain(gobjs).value:
                assert hasattr(obj, '__call__')
                obj = obj.__call__(*params)
        value = obj
        type = None                          ## TODO TYPES
        super(Attribute, self).__init__(gobjs, type, value)

class FCall(Value):

    def __init__(self, objs, parameters):
        type = None                          ## TODO TYPES
        value = [param(objs).value for param in parameters]
        super(FCall, self).__init__(objs, type, value)

class CallChain(Value):

    def __init__(self, objs, calls):
        type = None
        value = [call(objs).value for call in calls]
        super(CallChain, self).__init__(objs, type, value)

class Object(Value):

    def __init__(self, objs, name):
        type = None                          ## TODO TYPES
        if isinstance(objs, dict): value = objs[name]
        else: value = getattr(objs, name)
        super(Object, self).__init__(objs, type, value)

class SymbolObject(Value):

    def __init__(self, objs, name, id):
        type = None                          ## TODO TYPES
        value = objs[(name, id)]
        super(SymbolObject, self).__init__(objs, type, value)
