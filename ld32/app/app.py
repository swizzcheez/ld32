#!/usr/bin/env python

import flask
from flask.ext import script
import os
import ld32

def configure(app=None, __name__=__name__, **ctx):
    if app is None:
        app = flask.Flask(__name__)
        app.debug = os.environ.get('LD32_DEBUG', False)

    app.config.page = {
        'static_css':
        [
            'ext/bootstrap-3.3.4-dist/css/bootstrap.min.css',
            'site/site.css',
            'formula/formula.css',
        ],
        'static_js':
        [
            'ext/jquery/jquery-2.1.3.min.js',
            'ext/angular-1.4/angular.js',
            'ext/angular-1.4/angular-route.js',
            'ext/angular-1.4/angular-resource.js',
            'site/site.js',
            'site/ng/oo.js',
            'site/ng/stage.js',
            'main/ng/app.js',
            'formula/ng/formula.js',
        ],
    }

    ld32.configure(app, **ctx)

    return app

def setup(init_fn, **ctx):

    def init_app():
        return configure(**ctx)

    mgr = script.Manager(init_app)

    mgr.add_command('runserver',
            flask.ext.script.Server(
                host=os.environ.get('LD32_HOST'),
                port=int(os.environ.get('LD32_PORT', 5000)))
    )

    @mgr.command
    def list_routes():
        import urllib
        app = flask.current_app

        output = []
        for rule in app.url_map.iter_rules():
            methods = ','.join(rule.methods)
            line = "{:50s} {:20s} {}".format(rule.endpoint, methods, rule)
            output.append(line)

        for line in sorted(output):
            print(line)

        ld32.setup(mgr, **ctx)

    return mgr

if __name__ == '__main__':
    setup(configure).run(default_command='runserver')

