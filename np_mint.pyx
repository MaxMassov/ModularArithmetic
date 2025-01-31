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

    def _preprocess_value(self, method, value):
        """
        Function that checks if the method called with a relevant value.

        Args:
            value (np_mint|int|float|bool): the value to which the method will be applied.

        Returns:
            np_mint: A new instance of the modular integer
                which is equal to result of applying
                method to self value and given value.

        Raises:
            ValueError: If the given np_mint value is not from the same
                modular system as self.
            TypeError: If the value is instance of int|float|bool,
                but int to np_mint conversion disabled, 
                and the value is not being used as an argument of the 
                following methods: __mul__, __rmul__, __pow__, __floordiv__, 
                __truediv__, __rfloordiv__, __rtruediv__, __lshift__.
        """
        if isinstance(value, np_mint):
            if self.mod != value.mod:
                raise ValueError(
                        """You cannot directly operate on numbers from 
                            different modular systems without first aligning 
                            them to a common modulus."""
                    )
            return value
        if isinstance(value, (float, bool)):
            value = int(value)
        if isinstance(value, (int, np.integer)):
            if method in ["__mul__", "__rmul__", "__pow__", 
                                    "__floordiv__", "__truediv__",
                                    "__rfloordiv__", "__rtruediv__", 
                                    "__lshift__"]:
                return value
            if _DISABLE_INT2MINT_CONVERSION:
                raise TypeError(f"""Int to modular int conversion was disabled, 
                                so the {method}() cannot be done.""")
            return self.__class__(value, self.mod)
        return NotImplemented

    def __add__(self, value):
        """
        Implements the addition of 2 modular integers or 
        a modular integer and an integer|float|bool.
        """
        processed_value = self._preprocess_value("__add__", value)
        if processed_value is NotImplemented:
            return NotImplemented
        return self.__class__(self.value + processed_value.value, self.mod)

    def __iadd__(self, value):
        """Implements += behaviour logic."""
        self = self.__add__(value)
        return self

    def __radd__(self, value):
        """
        Implements the addition of an integer|float|bool and a modular integer.
        """
        return self.__add__(value)

    def __sub__(self, value):
        """
        Implements the subtraction of of 2 modular integers or 
        a modular integer and an integer|float|bool.
        """
        processed_value = self._preprocess_value("__sub__", value)
        if processed_value is NotImplemented:
            return NotImplemented
        return self.__class__(self.value - processed_value.value, self.mod)
    
    def __isub__(self, value):
        """Implements -= behaviour logic."""
        self = self.__sub__(value)
        return self

    def __rsub__(self, value):
        """
        Implements the subtraction of an integer|float|bool and a modular integer.
        """
        processed_value = self._preprocess_value("__rsub__", value)
        if processed_value is NotImplemented:
            return NotImplemented
        return self.__class__(processed_value.value - self.value, self.mod)

    def __mul__(self, value):
        """
        Implements the multiplication of 2 modular integers or 
        a modular integer and an integer|float|bool.
        """
        processed_value = self._preprocess_value("__mul__", value)
        if processed_value is NotImplemented:
            return NotImplemented
        if isinstance(processed_value, (int, np.integer)):
            if processed_value == 0:
                return self.__class__(0, self.mod)
            return self.__class__(self.value * processed_value, self.mod * processed_value)
        return self.__class__(self.value * processed_value.value, self.mod)  
    
    def __imul__(self, value):
        """Implements *= behaviour logic."""
        self = self.__mul__(value)
        return self

    def __rmul__(self, value):
        """
        Implements the multiplications of an integer|float|bool and a modular integer.
        """
        return self.__mul__(value)