
from . import warmup

def configure(app, **ctx):
    warmup.configure(app, **ctx)

def setup(mgr, **ctx):
    warmup.setup(mgr, **ctx)

