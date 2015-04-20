
import flask
from flask.ext import restful
from . import models
import uuid

def configure(app, ld32_prefix='', **ctx):
    app.register_blueprint(blueprint, url_prefix=ld32_prefix)
    api = restful.Api(app)
    api.add_resource(LevelResource, '/level')

blueprint = flask.Blueprint('main', __name__,
                            template_folder='templates',
                            static_folder='static',
                            static_url_path='/static/main')

@blueprint.route('/')
def welcome(render=flask.render_template):
    return render('welcome.html')

@blueprint.route('/game')
def game(render=flask.render_template):
    return render('game.html')

@blueprint.route('/scores')
def scores(render=flask.render_template):
    return render('scores.html')

class LevelResource(restful.Resource):
    def get(self):
        level = int(flask.request.args.get('level', 1))
        game_id = flask.request.args.get('game_id')
        factory = models.AlienFactory(level, game_id)
        next_level_url = flask.url_for('levelresource',
                                        game_id=factory.game_id,
                                        level=level + 1)

        return dict(
            level = level,
            game_id = factory.game_id,
            next_level_url=next_level_url,
            aliens = factory(),
        )

