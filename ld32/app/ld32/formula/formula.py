
class SymbolEntityMap(dict):
    next_id = 1

    def __call__(self, sym, **ctx):
        entity = self.get(id(sym))
        if entity is not None:
            return entity

        entity = dict(ctx, repr=repr(sym), extra=[])
        child_ctx = dict(ctx)
        self[id(sym)] = entity
        self[id(entity)] = entity

        cls_name = entity['type'] = type(sym).__name__.lower()
        sym_id = self.next_id
        self.next_id = sym_id + 1
        entity_id = entity['id'] = sym_id
        self[entity_id] = entity

        entity['children'] = [
            self(arg, **child_ctx)
            for arg in sym.args
        ]

        for base in reversed(type(sym).__mro__):
            base_name = base.__name__.lower()
            fn = getattr(self, 'add_' + base_name, None)
            if fn is not None:
                fn(entity, sym, ctx, child_ctx)


        return entity

    def add_rational(self, entity, sym, ctx, child_ctx):
        entity['n'] = sym.p
        entity['d'] = sym.q

    def add_equality(self, entity, sym, ctx, child_ctx):
        self.setup_equation(sym)

    def setup_equation(self, sym, **ctx):
        self(sym)['extra'].append('eq')
        for arg in sym.args:
            self.setup_expression(arg, outer=True, **ctx)

    def setup_expression(self, sym, outer=False, **ctx):
        self(sym)['extra'].append('ex')
        if outer:
            self(sym)['extra'].append('ex-outer')
        else:
            self(sym)['extra'].append('ex-inner')
        if sym.args:
            for arg in sym.args:
                self.setup_term(arg, outer=outer, **ctx)
        else:
            self.setup_term(sym, outer=outer, **ctx)

    def setup_term(self, sym, outer=False, **ctx):
        self(sym)['extra'].append('t')
        if outer:
            self(sym)['extra'].append('t-outer')
        else:
            self(sym)['extra'].append('t-inner')
        if sym.args:
            for arg in sym.args:
                self.setup_factor(arg, outer=outer, **ctx)
        else:
            self.setup_factor(sym, outer=outer, **ctx)

    def setup_factor(self, sym, outer=False, **ctx):
        self(sym)['extra'].append('f')
        if outer:
            self(sym)['extra'].append('f-outer')
        else:
            self(sym)['extra'].append('f-inner')
