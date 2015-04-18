
from . import main, formula

def configure(app, **ctx):
    main.configure(app, **ctx)
    formula.configure(app, **ctx)

def setup(mgr, **ctx):
    main.setup(mgr, **ctx)
    formula.setup(mgr, **ctx)

