#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import collections, math

def build_tree(gen):
    stack = list()
    root = None
    for children, sym in gen:
        node = Node(sym)
        if not root:
            root = node
        if stack:
            stack[-1]['node'].addkid(node)
            stack[-1]['children'] -= 1
            if stack[-1]['children'] <= 0:
                stack.pop()
        if children:
            stack.append({'node':node, 'children':children})
    if stack:
        raise SyntaxError, 'Malformed input'
    return root

class Node(object):

    def __init__(self, label, children=None):
        self.label = label
        self.children = children if children is not None else list()

    def addkid(self, node, before=False):
        if before:  self.children.insert(0, node)
        else:   self.children.append(node)
        return self

    def get(self, label):
        if self.label == label: return self
        for c in self.children:
            if label in c: return c.get(label)

    def iter(self):
        queue = collections.deque()
        queue.append(self)
        while len(queue) > 0:
            n = queue.popleft()
            for c in n.children: queue.append(c)
            yield n

    def __getattr__(self, name):
        for c in self.children:
            if name == c.label:
                return c
        raise AttributeError

    def __contains__(self, b):
        if isinstance(b, str) and self.label == b: return 1
        elif not isinstance(b, str) and self.label == b.label: return 1
        elif (isinstance(b, str) and self.label != b) or self.label != b.label:
            return sum(b in c for c in self.children)
        raise TypeError, "Object %s is not of type str or Node" % repr(b)

    def __eq__(self, b, tolerance=6):
        if b is None: return False
        if not isinstance(b, Node):
            raise TypeError, "Must compare against type Node"
        mylabels = [n.label for n in self.iter()]
        theirlabels = [n.label for n in b.iter()]
        if len(mylabels) != len(theirlabels):
            return False
        for a, b in zip(mylabels, theirlabels):
            if isinstance(a, float) and isinstance(b, float):
                af, ae = math.frexp(a)
                bf, be = math.frexp(b)
                af = round(af, tolerance)
                bf = round(bf, tolerance)
                #print af, ae, '\t', bf, be
                if af != bf or ae != be:
                    return False
            elif a != b:
                return False
        return True

    def __ne__(self, b):
        return not self.__eq__(b)

    def __repr__(self):
        return super(Node, self).__repr__()[:-1] + " %s>" % str(self.label)

    def __str__(self):
        def string(s):
            if isinstance(s, Node): return str(s)
            return '0:%s' % str(s)
        s = "%d:%s" % (len(self.children), str(self.label))
        s = '\n'.join([s]+[string(c) for c in self.children])
        return s

    def dotty(self):
        def string(s):
            if isinstance(s, Node): return str(s.label)
            return str(s)
        node = '%(name)s [shape=rect, label="%(label)s"];'
        leaf = '%(name)s [shape=rect, label="%(label)s" style="filled" fillcolor="#dddddd"];'
        edge = '%s -> %s;'
        nodes = list()
        edges = list()

        i = 0
        queue = collections.deque()
        queue.append((i, self))
        i += 1
        while len(queue) > 0:
            c, n = queue.popleft()
            name = 'n%d' % c
            label = string(n)
            if not hasattr(n, 'children'): nodes.append(leaf % locals())
            elif not n.children: nodes.append(leaf % locals())
            else: nodes.append(node % locals())
            if not hasattr(n, 'children'): continue
            for c in n.children:
                edges.append(edge % (name, ('n%d' % i)))
                queue.append((i, c))
                i += 1
        return 'digraph G {\n' + '\n'.join(nodes) + '\n' + '\n'.join(edges) + '\n}\n'
