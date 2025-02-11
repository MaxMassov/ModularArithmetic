# -*- coding: utf-8 -*-
# cython: language_level=3, boundscheck=False, wraparound=False

from np_mint cimport np_mint, INT_t

cdef class Partial:

    def __init__(self, INT_t mod):
        if mod <= 1:
            raise ValueError("Modulus must be at least 2")
        self.mod = mod

    def __call__(self, INT_t value):
        return np_mint(value, self.mod)

np_mint2 = Partial(2)
np_mint3 = Partial(3)
np_mint5 = Partial(5)
np_mint7 = Partial(7)