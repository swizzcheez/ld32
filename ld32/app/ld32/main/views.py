
import flask


def configure(app, warmup_prefix='', **ctx):
    app.register_blueprint(blueprint, url_prefix=warmup_prefix)

blueprint = flask.Blueprint('warmup', __name__,
                            template_folder='templates',
                            static_folder='static',
                            static_url_path='/static/warmup')

@blueprint.route('/')
def welcome(render=flask.render_template):
    return render('welcome.html')

@blueprint.route('/game')
def game(render=flask.render_template):
    return render('game.html')

@blueprint.route('/scores')
def scores(render=flask.render_template):
    return render('scores.html')

