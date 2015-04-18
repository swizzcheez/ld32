
from . import views

def configure(app, **ctx):
    views.configure(app, **ctx)

def setup(mgr, **ctx):
    pass

