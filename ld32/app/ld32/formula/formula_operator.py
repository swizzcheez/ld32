
from .formula import *

##############################################################################

class FormulaOperator(object):
    registry = {}

    def __init__(self):
        pass

    def apply_to(self, formula):
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

##############################################################################

@FormulaOperator.register('sub_term')
class SubTermOperator(FormulaOperator):
    def __init__(self, term_id, **_kw):
        super(SubTermOperator, self).__init__(**_kw)
        self.term_id = self.expect('t', term_id)

    def apply_to(self, formula):
        term = formula.find(self.term_id)
        if term.inner:
            raise TypeError('Not an outer term')
        # Remove from containing expression, add to all other epxressions.
        ex = term.parent()
        ex.remove(term)
        eq = ex.parent()
        for expr in eq:
            if expr is not ex:
                expr.append(term(scalar=-term.scalar))

##############################################################################

