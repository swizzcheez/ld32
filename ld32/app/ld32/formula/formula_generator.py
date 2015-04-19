
import random
from sympy import *

##############################################################################

class FormulaGenerator(object):
    registry = {}

    def __init__(self, formula_id):
        self.formula_id = formula_id

    def make(self):
        formula = self.base_formula()
        self.permute_formula(formula)
        return formula

    def base_formula(self):
        return None

    def eq_do(self, eq, fn):
        return Eq(*tuple(fn(side) for side in eq.args))

    def permute_formula(self, formula):
        pass

    @staticmethod
    def register(name):
        def registrar(cls):
            cls.registry[name] = cls
            return cls
        return registrar

##############################################################################

class RandomFormulaGenerator(FormulaGenerator):
    BASE_SEED = 22313243284327432843278423

    def make(self, *_args, **_kw):
        state = random.getstate()
        try:
            random.seed(self.BASE_SEED)
            random.seed(self.formula_id)
            return super(RandomFormulaGenerator, self).make(*_args, **_kw)
        finally:
            random.setstate(state)

##############################################################################

@FormulaGenerator.register('simple')
class SimpleFormulaGenerator(RandomFormulaGenerator):
    def base_formula(self):
        want = int(random.random() * 10 + 1)
        eq = Eq(S('x'), want)
        if random.random() < 0.5:
            n = int(random.random() * 4 + 1)
            eq = self.eq_do(eq, lambda s: s * n)
        o = int(random.random() * 10 + 1)
        return self.eq_do(eq, lambda s: s + o)

##############################################################################

@FormulaGenerator.register('dual')
class DualFormulaGenerator(RandomFormulaGenerator):
    def base_formula(self):
        want = int(random.random() * 10 + 1)
        eq = Eq(S('x'), S('y') + want)
        if random.random() < 0.5:
            n = int(random.random() * 4 + 1)
            eq = self.eq_do(eq, lambda s: s * n)
        o = int(random.random() * 10 + 1)
        return self.eq_do(eq, lambda s: s + o)

##############################################################################

