
from sympy import *

##############################################################################

class FormulaOperator(object):
    registry = {}

    def __init__(self, *values, history=()):
        self.args = tuple(S(value) for value in values)
        self.kwargs = {}
        self.history = history

    def apply_to(self, formula):
        if isinstance(formula, Equality):
            return self.modify_eq(formula, *self.args, **self.kwargs)
        else:
            raise TypeError('Cannot apply %r to %r' % (self, formula))

    def eq_do(self, eq, fn):
        return Eq(*tuple(fn(side) for side in eq.args))

    def modify_eq(self, eq):
        return eq

    @classmethod
    def setup_arguments(cls, arguments):
        pass

    @staticmethod
    def register(name):
        def registrar(cls):
            cls.registry[name] = cls
            return cls
        return registrar

    @staticmethod
    def expect(prefix, value):
        if value.startswith(prefix):
            return value
        else:
            raise TypeError('%r is not of type prefix %r' % (value, prefix))

    @classmethod
    def can_apply_to(cls, formula):
        return True

##############################################################################

@FormulaOperator.register('sub_term')
class SubTermOperator(FormulaOperator):
    def modify_eq(self, eq, term):
        return Eq(*tuple((expr - term) for expr in eq.args))

    @classmethod
    def setup_arguments(cls, arguments):
        super().setup_arguments(arguments)
        arguments.append(dict(selects=['t-outer']))

##############################################################################

@FormulaOperator.register('div_factor')
class SubTermOperator(FormulaOperator):
    def modify_eq(self, eq, factor):
        return Eq(*tuple((expr / factor) for expr in eq.args))

    @classmethod
    def setup_arguments(cls, arguments):
        super().setup_arguments(arguments)
        arguments.append(dict(selects=['f-outer']))

##############################################################################

@FormulaOperator.register('sub')
class SubTermOperator(FormulaOperator):
    def modify_eq(self, eq, var):
        if eq.args[0] == var:
            expr = eq.args[1]
        else:
            expr = eq.args[0]
        repl = { var : expr }
        result = self.eq_do(self.history[0], lambda e: e.xreplace(repl))
        print(self.history[0], var, expr)
        print(Eq(*tuple(e.subs(var, expr) for e in self.history[0].args)))
        return result

    @classmethod
    def can_apply_to(cls, formula):
        if super().can_apply_to(formula):
            if not formula.is_Equality:
                return False
            if formula.args[0].is_Symbol:
                return True
            if formula.args[1].is_Symbol:
                return True
        return False

    @classmethod
    def setup_arguments(cls, arguments):
        super().setup_arguments(arguments)
        arguments.append(dict(selects=['v']))

##############################################################################

