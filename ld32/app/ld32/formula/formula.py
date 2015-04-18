
from fractions import Fraction
import random, weakref

class Node(object):
    code = None
    id = None
    allowed = ()

    def __call__(self, **updates):
        args = []
        kwargs = {}
        self.setup_clone_args(args, kwargs)
        kwargs.update(updates)
        return type(self)(*args, **kwargs)

    def setup_clone_args(self, args, kwargs):
        pass

    def relabel(self, seq=None, inner=False, parent=None):
        if seq is None:
            seq = dict()
        if self.id is None:
            n = seq.setdefault(self.code, 1)
            seq[self.code] = n + 1
            self.id = '%s%d' % (self.code, n)
        self.inner = inner
        self.parent = parent

    def entity(self):
        entity = dict(type_code=self.code, inner=self.inner, id=self.id)
        self.setup_entity(entity)
        return entity

    def setup_entity(self, entity):
        pass

    def find(self, id):
        if self.id == id:
            return self

    @classmethod
    def normalize(cls, what):
        if isinstance(what, cls.allowed):
            return what
        elif isinstance(what, str) and not isinstance(what, Variable):
            return cls.normalize(Variable(what))
        elif (isinstance(what, (int, float, Fraction))
              and not isinstance(what, Scalar)):
            return cls.normalize(Scalar(what))
        else:
            return cls.normalize(cls.allowed[0](what))

##############################################################################

class Variable(Node, str):
    code = 'v'

    def setup_entity(self, entity):
        super().setup_entity(entity)
        entity['name'] = str(self)

    def setup_clone_args(self, args, kwargs):
        super().setup_clone_args(args, kwargs)
        args.append(self)

##############################################################################

class Scalar(Node, Fraction):
    code = 's'

    def setup_entity(self, entity):
        super().setup_entity(entity)
        entity['n'] = self.numerator
        entity['d'] = self.denominator

    def setup_clone_args(self, args, kwargs):
        super().setup_clone_args(args, kwargs)
        args.append(self)

##############################################################################

class Factor(Node):
    code = 'f'

    def __init__(self, item, exponent=1):
        self.item = self.normalize(item)
        self.exponent = self.normalize(exponent)

    def relabel(self, seq, inner=False, parent=None, **_kw):
        super().relabel(seq, inner=inner, parent=parent, **_kw)
        ref = weakref.ref(self)
        inner = inner or isinstance(self.item, Expression)
        self.item.relabel(seq, inner=inner, parent=ref, **_kw)
        self.exponent.relabel(seq, inner=inner, **_kw)

    def setup_entity(self, entity):
        super().setup_entity(entity)
        entity['item'] = self.item.entity()
        if self.exponent != 1:
            entity['exponent'] = self.exponent.entity()

    def setup_clone_args(self, args, kwargs):
        super().setup_clone_args(args, kwargs)
        kwargs['item'] = self.item()
        kwargs['exponent'] = self.exponent()

    def find(self, id):
        result = super().find(id)
        if result is None:
            result = self.item.find(id)
        if result is None:
            result = self.exponent.find(id)
        return result

##############################################################################

class Container(Node, list):
    contents_label = 'contents'

    def __init__(self, *contents, **kw):
        super().__init__(**kw)
        self.extend(self.normalize(item) for item in contents)

    def relabel(self, seq, parent=None, **kw):
        super().relabel(seq, parent=parent, **kw)
        ref = weakref.ref(self)
        for node in self:
            node.relabel(seq, parent=ref, **kw)

    def setup_entity(self, entity):
        super().setup_entity(entity)
        entity[self.contents_label] = [item.entity() for item in self]

    def setup_clone_args(self, args, kwargs):
        super().setup_clone_args(args, kwargs)
        args.extend(node() for node in self)

    def find(self, id):
        result = super().find(id)
        if result is None:
            for node in self:
                result = node.find(id)
                if result is not None:
                    break
        return result

##############################################################################

class Term(Container):
    code = 't'
    allowed = (Factor,)
    contents_label = 'factors'

    def __init__(self, *factors, scalar=1):
        super().__init__(*factors)
        self.scalar = Scalar(scalar)

    def setup_entity(self, entity):
        super().setup_entity(entity)
        entity['scalar'] = self.scalar.entity()

    def relabel(self, seq, parent=None, **kw):
        super().relabel(seq, parent=parent, **kw)
        parent = weakref.ref(self)
        self.scalar.relabel(seq, parent=parent, **kw)

##############################################################################

class Expression(Container):
    code = 'ex'
    allowed = (Term,)
    contents_label = 'terms'

# Needs to be here to avoid circular reference.
Factor.allowed = (Expression, Variable, Scalar)

##############################################################################

class Equation(Container):
    code = 'eq'
    comparator = '='
    allowed = (Expression,)
    contents_label = 'expressions'

    def setup_entity(self, entity):
        super().setup_entity(entity)
        entity['comparator'] = self.comparator

##############################################################################

