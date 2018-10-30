# -*- coding: utf-8 -*-
"""
astree.py - Abstract Syntax Tree Structure

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""


class ASTKind:
    """Abstract Syntax Tree Kind Class

    This class normalizes the node types generated by different parsers.
    
    Args:
        kind <>: The raw kind
        type_ <str>: The tpye of parser
            - 'cc': Kind generated by libclang
    """

    def __init__(self, kind, type_):
        if type_ == 'cc':
            self._name = kind.name

    def __repr__(self):
        return self._name

    @property
    def name(self):
        return self._name


class ASTNode:
    """Abstract Syntax Tree Node Class

    Args:
        None
    """

    def __init__(self):
        self._parent = None
        self._children = []
        self._id = None
        self._data = None
        self._kind = None
        self._raw = None

    def __repr__(self):
        return f'<covec.utils.ast.ASTNode>\n{self.id}\n{self.data}\n{self.kind}'

    @property
    def parent(self):
        """Return Node parent"""
        return self._parent

    @parent.setter
    def parent(self, node):
        """Set parent of Node"""
        if isinstance(node, ASTNode):
            self._parent = node
        else:
            raise ValueError(f'{node} is not a ASTNode')

    @property
    def children(self):
        """Return children of Node"""
        return self._children

    @children.setter
    def children(self, nodes):
        """Set children of Node"""
        if hasattr(nodes, "__iter__"):
            for n in nodes:
                if isinstance(n, ASTNode):
                    self._children.append(n)
                else:
                    raise ValueError(f'{n} is not a ASTNode')
        else:
            raise ValueError(f'{nodes} is not Iterable')

    @property
    def id(self):
        """Return Node id"""
        return self._id

    @id.setter
    def id(self, value):
        """Set id of Node"""
        self._id = str(value)

    @property
    def data(self):
        """Return Node data"""
        return self._data

    @data.setter
    def data(self, value):
        """Set data of Node"""
        self._data = str(value)

    @property
    def kind(self):
        """Return type of Node"""
        return self._kind.name

    @kind.setter
    def kind(self, value):
        self._kind = value

    @property
    def raw(self):
        """
        Return raw class of Node,
        raw class is a raw data created by each language parser,
        for c/c++, raw means clang.cindex.Cursor.
        """
        return self._raw

    @raw.setter
    def raw(self, value):
        """set raw data of node"""
        self._raw = value
