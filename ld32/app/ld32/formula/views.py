
import flask
from flask.ext import restful
from .formula_generator import FormulaGenerator
from .formula_operator import FormulaOperator

def configure(app, formula_prefix='/formula', **ctx):
    app.register_blueprint(blueprint, url_prefix=formula_prefix)
    app.register_blueprint(static_blueprint)
    api = restful.Api(app, prefix=formula_prefix)
    api.add_resource(FormulaResource,
            '/<formula_type>/<formula_id>',
            '/<formula_type>/<formula_id>/',
            '/<formula_type>/<formula_id>/<path:opstr>')

class FormulaResource(restful.Resource):
    '''
    Generate a formula represntation from some type and a randomizer.
    '''

    def get(self, formula_type, formula_id, *ops, opstr=''):
        cls = FormulaGenerator.registry.get(formula_type)
        if cls is None:
            restful.abort(404, message='Invalid formalu type %r' % formula_type)
        seq = {}
        formula = cls(formula_id).make()
        formula.relabel(seq)
        for part in opstr.split('/'):
            if part:
                opparts = part.split(';')
                opname = opparts[0]
                op_cls = FormulaOperator.registry.get(opname)
                if op_cls is None:
                    restful.abort(404,
                                  message='Invalid operation %r' % opname)
                operator = op_cls(*opparts[1:])
                formula = operator.apply_to(formula) or formula
                formula.relabel(seq)
        return dict(
            view_url = flask.url_for('formula.render',
                          formula_type=formula_type,
                          formula_id=formula_id,
                          opstr=opstr,
                          _external=True),
            formula = formula.entity()
        )

blueprint = flask.Blueprint('formula', __name__,
                            template_folder='templates')
static_blueprint = flask.Blueprint('static_formula', __name__,
                            static_folder='static',
                            static_url_path='/static/formula')

@blueprint.route('/render/<formula_type>/<formula_id>')
@blueprint.route('/render/<formula_type>/<formula_id>/')
@blueprint.route('/render/<formula_type>/<formula_id>/<path:opstr>')
def render(formula_type, formula_id, opstr=''):
    data_url = flask.url_for('formularesource',
                             formula_type=formula_type,
                             formula_id=formula_id,
                             opstr=opstr,
                             _external=True)
    return flask.render_template('formula/test-render.html', url=data_url)

