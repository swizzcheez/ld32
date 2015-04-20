
import random, uuid, math
from sympy import S
from sympy.printing.jscode import jscode

class AlienFactory(object):
    registry = []

    def __init__(self, level, game_id=None):
        self.level = level
        if game_id is None:
            game_id = str(uuid.uuid4())
        self.game_id = game_id

    def __call__(self):
        count = int(math.log2(self.level) + 1)
        options = sorted(self.registry[:])
        state = random.getstate()
        try:
            random.seed(self.game_id + str(self.level))
            return [self.make_alien(options, self.level, index).entity()
                    for index in range(count)]
        finally:
            random.setstate(state)

    def make_alien(self, options, level, index):
        level -= index
        while options[-1][0] > level:
            options.pop()
        cls = options[-1][1]
        return cls(self.level)

    @classmethod
    def register(a_cls, min_level):
        def registrar(cls):
            a_cls.registry.append([min_level, cls])
        return registrar

class Alien(object):
    def __init__(self, level):
        self.level = level
        self.x = int(100  * (random.random() - 0.5))
        self.y = int(250  * random.random())
        self.fx = S('x0')
        self.fy = S('y0')
        self.setup()

    def setup(self):
        pass

    def entity(self):
        return dict(
            x = self.x,
            y = self.y,
            color = self.color,
            formula = '[%s,%s]' % (jscode(self.fx), jscode(self.fy)),
        )

@AlienFactory.register(1)
class StationaryAlien(Alien):
    color = 'red'

@AlienFactory.register(3)
class DroppingAlien(Alien):
    color = 'blue'

    def setup(self):
        super().setup()
        speed = min(150, 25 * self.level)
        self.fy += S('%d * t' % speed)

@AlienFactory.register(5)
class LinearAlien(Alien):
    color = 'green'

    def setup(self):
        super().setup()
        speed = min(50, 10 * self.level)
        self.fy += S('%d * t' % speed)
        self.fx += S('%d * t' % speed)

