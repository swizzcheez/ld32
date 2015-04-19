
import flask
from sympy import *
from flask.ext import restful
from .formula_generator import FormulaGenerator
from .formula_operator import FormulaOperator
from .formula import SymbolEntityMap

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
        entity_map = SymbolEntityMap()
        history = []
        formula = cls(formula_id).make()
        entity_map(formula)
        for part in opstr.split('/'):
            if part:
                opparts = part.replace('$2F', '/').split(';')
                opname = opparts[0]
                op_cls = FormulaOperator.registry.get(opname)
                if op_cls is None:
                    restful.abort(404, message='Invalid operation %r' % opname)
                history.append(formula)
                op = op_cls(*opparts[1:], history=history)
                formula = op.apply_to(formula)
                entity_map(formula)
        return dict(
            view_url = flask.url_for('formula.render',
                          formula_type=formula_type,
                          formula_id=formula_id,
                          opstr=opstr,
                          _external=True),
            formula = entity_map(formula),
            operations = self.operations_for(formula),
        )

    def operations_for(self, formula):
        ops = {}

        # Provide no operations if we're down to the simple case.
        if self.is_minimal(formula):
            return ops

        for opname in FormulaOperator.registry:
            op_cls = FormulaOperator.registry[opname]
            if op_cls.can_apply_to(formula):
                arguments = []
                op_cls.setup_arguments(arguments)
                ops[opname] = dict(
                    arguments = arguments,
                )
        return ops

    def is_minimal(self, eq):
        return (eq.is_Equality
            and ((eq.args[0].is_Symbol and eq.args[1].is_Number)
                 or (eq.args[1].is_Symbol and eq.args[0].is_Number)))

    def sym2entity(self, sym, seq, **ctx):
        if isinstance(sym, (list, tuple)):
            return [
                self.sym2entity(node, seq, **ctx)
                for node in sym
            ]
        else:
            entity = dict()
            child_ctx = dict(ctx)
            for base in type(sym).__mro__:
                name = base.__name__.lower()
                fn = getattr(self, 'repr_' + name, None)
                if fn is not None:
                    fn(entity, ctx, child_ctx)
            entity.children = [
                self.sym2entity(arg, seq, **ctx)
            ]
            node_id = seq.get(id(sym))
            if node_id is None:
                node_id = seq.setdefault(name, 1)
                seq[name] = node_id + 1
                seq[id(sym)] = node_id
            entity['id'] = '%s:%d' % (entity['type_code'], node_id)
            entity['inner'] = ctx.get('inner', False)
            entity['value'] = repr(sym)
            return entity

    def repr_equality(self, sym, seq, **ctx):
        return dict(
            type_code='eq',
            comparator='=',
            expressions=[self.sym2entity(arg, seq, **ctx) for arg in sym.args],
        )

    def repr_symbol(self, sym, seq, **ctx):
        return dict(
            type_code='v',
            name=str(sym),
        )

    def repr_integer(self, sym, seq, **ctx):
        return dict(
            type_code='s',
            n=int(sym),
            d=1,
        )

    def repr_rational(self, sym, seq, **ctx):
        return dict(
            type_code='s',
            n=sym.p,
            d=sym.q,
        )

    def repr_mul(self, sym, seq, **ctx):
        scalar, factors = sym.as_two_terms()
        return dict(
            type_code='t',
            scalar=self.sym2entity(scalar, seq, **ctx),
            factors=self.sym2entity(factors.args or [factors], seq, **ctx)
        )
    def repr_add(self, sym, seq, **ctx):
        return dict(
            type_code='ex',
            terms=self.sym2entity(sym.args, seq, **ctx)
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

