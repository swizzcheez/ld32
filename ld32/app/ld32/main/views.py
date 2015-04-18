
import flask


def configure(app, ld32_prefix='', **ctx):
    app.register_blueprint(blueprint, url_prefix=ld32_prefix)

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

