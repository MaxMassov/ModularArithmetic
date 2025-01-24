# -*- coding: utf-8 -*-
# cython: language_level=3, boundscheck=False, wraparound=False

cimport numpy as cnp
cnp.import_array()
from libc.stdlib cimport llabs
import numpy as np
from functools import wraps
import inspect
from typing import Callable
import re

INT_DTYPE = np.int64
ctypedef cnp.int64_t INT_t

cdef long long gcd(long long a, long long b):
    while b != 0:
        a, b = b, a % b
    return a

cdef bint _DISABLE_INT2MINT_CONVERSION = False

cdef class np_mint:
    """NumPy compatible modular integer class"""
    
    cdef readonly INT_t value
    cdef readonly INT_t mod
    cdef readonly INT_t vm_gcd
    cdef readonly cnp.dtype dtype

    def __cinit__(self, INT_t value, INT_t mod):
        """
        Initializes a mint instance.

        Args:
            value (int|float|bool): The integer number's value.
            mod (int|float): The modulus of the system. Must be an integer 
                greater than 1.

        Raises:
            TypeError: If either `value` or `modulus` is not an integer|float|bool. 
            ValueError: if `modulus` is less than 2.
        """
        if mod <= 1:
            raise ValueError("Modulus must be at least 2")
            
        self.value = value % mod
        self.mod = mod
        self.vm_gcd = gcd(llabs(self.value), self.mod)
        self.dtype = np.dtype(INT_DTYPE)

    @property
    def int2mint(self) -> bool:
        """Access to _DISABLE_INT2MINT_CONVERSION value."""
        return not _DISABLE_INT2MINT_CONVERSION

    @classmethod
    def set_int2mint(cls, value):
        """
        Set np_mint._DISABLE_INT2MINT_CONVERSION to the opposite of `value`
        
        Arguments:
            value (bool): new value of np_mint._DISABLE_INT2MINT_CONVERSION 
                (can be int, but must be equal to either 1 or 0).
        
        Raises:
            ValueError: If value is not a relevant value.
        """
        global _DISABLE_INT2MINT_CONVERSION
        if not isinstance(value, (bool, int, np.integer)) or value not in (True, False, 0, 1):
            raise ValueError("Value must be bool or an int equal to 0 or 1.")
        _DISABLE_INT2MINT_CONVERSION = not bool(value)

    @classmethod
    def change_int2mint(cls):
        """
        Toggle _DISABLE_INT2MINT_CONVERSION to its opposite value
        """
        global _DISABLE_INT2MINT_CONVERSION
        _DISABLE_INT2MINT_CONVERSION = not _DISABLE_INT2MINT_CONVERSION

    @classmethod
    def activate_int2mint(cls):
        """
        Set _DISABLE_INT2MINT_CONVERSION to False
        """
        global _DISABLE_INT2MINT_CONVERSION
        _DISABLE_INT2MINT_CONVERSION = False

    @classmethod
    def disable_int2mint(cls):
        """
        Set np_mint._DISABLE_INT2MINT_CONVERSION to True
        """
        global _DISABLE_INT2MINT_CONVERSION
        _DISABLE_INT2MINT_CONVERSION = True