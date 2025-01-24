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

cdef inline INT_t gcd(INT_t a, INT_t b):
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
    def set_int2mint(cls, value: bool):
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

    @staticmethod
    def _check_value(method: Callable):
        """
        Decorator that checks if the method called with a relevant value.

        Args:
            method (function): A np_mint method between two values.

        Returns:
            wrapper (function): A function that checks if the method called 
                with a relevant value.
        """
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            """
            Function that checks if the method called with a relevant value.

            Args:
                value (np_mint|int|float|bool): the value to which the method will be applied.

            Returns:
                np_mint: A new instance of the modular integer
                    which is equal to result of applying
                    method to self value and given value.

            Raises:
                TypeError: If more or less than one arrgument is given.
                ValueError: If the given np_mint value is not from the same
                    modular system as self.
                TypeError: If the value is instance of int|float|bool,
                    but int to np_mint conversion disabled, 
                    and the value is not being used as an argument of the 
                    following methods: __mul__, __rmul__, __pow__, __floordiv__, 
                    __truediv__, __rfloordiv__, __rtruediv__, __lshift__.
            """
            value = None
            if len(args) == 1:
                value = args[0]
            elif len(kwargs) == 1:
                value = kwargs.values()[0]
            if value is None:
                raise TypeError(f"""Method {method.__name__}() takes one argument 
                                ({len(args) + len(kwargs)} given).""")
            if isinstance(value, np_mint):
                if self.mod != value.mod:
                    raise ValueError(
                            """You cannot directly operate on numbers from 
                                different modular systems without first aligning 
                                them to a common modulus."""
                        )
                return method(self, value)
            if isinstance(value, (float, bool)):
                value = int(value)
            if isinstance(value, (int, np.integer)):
                if method.__name__ in ["__mul__", "__rmul__", "__pow__", 
                                       "__floordiv__", "__truediv__",
                                       "__rfloordiv__", "__rtruediv__", 
                                       "__lshift__"]:
                    return method(self, value)
                if _DISABLE_INT2MINT_CONVERSION:
                    raise TypeError(f"""Int to modular int conversion was disabled, 
                                    so the {method.__name__}() cannot be done.""")
                return method(self, self.__class__(value, self.mod))
            return NotImplemented
        return wrapper