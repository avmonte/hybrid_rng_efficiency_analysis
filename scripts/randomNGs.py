import time

from scripts.common import get_qo_arev_truly_random_number

LCG_COEF = 3
LCG_CONST = 7
LCG_MOD = 10


class lcg:
    _seed = None

    @classmethod
    def seed(cls, seed=None):
        cls._seed = int(time.time() * 1000) if seed is None else seed

    @classmethod
    def random(cls):
        if cls._seed is None:
            cls.seed()

        cls._seed = (LCG_COEF * cls._seed + LCG_CONST) % LCG_MOD
        return cls._seed / LCG_MOD

    @classmethod
    def uniform(cls, a, b):
        return a + (b - a) * cls.random()


class entropy:
    @classmethod
    def seed(cls, seed=None):
        pass  # Whoops

    @classmethod
    def random(cls):
        get_qo_arev_truly_random_number()

    @classmethod
    def uniform(cls, a, b):
        return a + (b - a) * cls.random()
