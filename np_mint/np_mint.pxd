cimport numpy as cnp
from cpython.object cimport PyObject

ctypedef cnp.int64_t INT_t

cdef class np_mint:
    cdef readonly INT_t value
    cdef readonly INT_t mod
    cdef readonly INT_t vm_gcd
    cdef readonly cnp.dtype dtype
    cdef PyObject* _ptr[1]  # Pointer array to store a reference to self

    cdef np_mint inv(self)  # Declaring inv as a cdef method
    cdef _preprocess_value(self, method: str, value)

cdef class Partial:
    cdef readonly INT_t mod