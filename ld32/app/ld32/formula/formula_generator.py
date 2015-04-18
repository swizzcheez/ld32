
from .formula import *

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
    def make(self, *_args, **_kw):
        state = random.getstate()
        try:
            random.seed(self.formula_id)
            return super(RandomFormulaGenerator, self).make(*_args, **_kw)
        finally:
            random.setstate(state)

##############################################################################

@FormulaGenerator.register('simple')
class SimpleFormulaGenerator(RandomFormulaGenerator):
    def base_formula(self):
        return Equation('x', Term(Term('x'), Term(1), scalar=2))

##############################################################################

