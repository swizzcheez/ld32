'''
>>> S.x * 5
'''

def cached(fn):
    def getter(taret, cls=None, name=fn.__name__):
        if cls is None:
            return fn
        else:
            obj = fn(target)
            setattr(target, name, obj)
            return obj

class System(object):
    def __getitem__(self, args):
        if type(args) is tuple:
            return tuple(self.make(arg) for arg in args)
        else:
            return self.make(args)

    def __getattr__(self, name):
        return self[name]

    def make(self, arg):
        if arg is None or isinstance(arg, Node):
            return arg
        if isinstance(arg, str):
            return Variable(self, arg)
        else:
            return Constant(self, arg)

    @cached
    def ZERO(self):
        return self[0]

    @cached
    def ONE(self):
        one = Constant.__new__(Constant)
        one.value = 1
        one.exponent = one
        return one
S = System()

class Node(object):
    factors = ()

    def __init__(self, system):
        self.system = system

    def ordered_factors(self):
        return self.factors

    @property
    def parts(self):
        return self.get_parts()

    def get_parts(self):
        return ()

class Term(Node):
    def __init__(self, system, *factors):
        super().__init__(system)
        self.factors = factors

    def __str__(self):
        return ''.join(map(str, self.ordered_factors()))

    def __repr__(self):
        return '*'.join(map(repr, self.ordered_factors()))

    def get_parts(self):
        return self.ordered_factors()

class Factor(Node):
    def __init__(self, system, exponent=None):
        super().__init__(system)
        if exponent is None:
            self.exponent = None
        else:
            self.exponent = system[exponent]

    @property
    def factors(self):
        return (self,)

    def __mul__(self, other):
        o = self.system[other]
        return self.do_mul(self, o, o)

    def __rmul__(self, other):
        o = self.system[other]
        return self.do_mul(o, self, o)

    @classmethod
    def do_mul(cls, left, right, other):
        if isinstance(other, Factor):
            return Term(left.system, left, other)
        elif isinstance(other, Term):
            return Term(left.system, *(left.factors + right.factors))

class Variable(Factor):
    def __init__(self, system, name, exponent=None):
        super().__init__(system, exponent)
        self.name = name

    def __str__(self):
        return str(self.name)

    def __repr___(self):
        return repr(self.name)

    def get_parts(self):
        return (self.value, self.exponent)

    @classmethod
    def do_mul(cls, left, right, other):
        if left == right:
            return Variable(left.name, left.exponent + right.exponent)
        else:
            return super().do_mul(left, right, other)

class Constant(Factor):
    def __init__(self, system, value):
        super().__init__(system, system.ONE)
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr___(self):
        return repr(self.value)

    def get_parts(self):
        return (self.value,)

    @classmethod
    def do_mul(cls, left, right, other):
        if isinstance(other, Constant):
            return Constant(self.system, left.value * right.value)
        else:
            return super().do_mul(cls, left, right, other)

