#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

class Type(object):
    def __new__(self):
        raise RuntimeError, 'Type cannot be instantiated'

class String(Type):
    def __new__(self, value):
        return str(value)

class Number(Type):
    def __new__(self, value):
        return int(value)

class Set(Type):
    def __new__(self):
        raise RuntimeError, 'Set cannot be instantiated'

class NoneType(Type):
    def __new__(self):
        return None
