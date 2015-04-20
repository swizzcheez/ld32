
import flask
from flask.ext import restful
import .models

def configure(app, formula_prefix='/monster', **ctx):
    app.register_blueprint(blueprint, url_prefix=formula_prefix)
    app.register_blueprint(static_blueprint)
    api = restful.Api(app, prefix=formula_prefix)
    api.add_resource(MonsterResource, '/<species>/<monster_id>')

class MonsterResource(restful.Resource):
    def get(self, species, monster_id):
        factory_cls = models.Monster.registry.get(species)
        if factory_cls is None:
            restful.abort(404, message='Invalid species %r' % species)
        monster = factory_cls.make(monster_id)

