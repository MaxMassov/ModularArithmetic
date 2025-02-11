# -*- coding: utf-8 -*-

cimport numpy as cnp
import numpy as np
from np_mint cimport np_mint

cpdef cnp.ndarray[object, ndim=2] modular_matrix_inv(cnp.ndarray[object, ndim=2] A):
    """
    Compute the inverse of a square matrix in modular arithmetic using Gaussian elimination.
    
    Args:
        A (np.ndarray): A square matrix of np_mint objects (dtype=object).
    
    Returns:
        np.ndarray: The inverse matrix in modular arithmetic (dtype=object).
    
    Raises:
        ValueError: If the matrix is singular in modular arithmetic.
    """
    cdef int n = A.shape[0]
    cdef cnp.ndarray[object, ndim=2] inv_matrix = np.empty((n, n), dtype=object)

    # Initialize inv_matrix as the identity matrix
    for i in range(n):
        for j in range(n):
            if i == j:
                inv_matrix[i, j] = np_mint(1, A[i, i].mod)
            else:
                inv_matrix[i, j] = np_mint(0, A[i, i].mod)

    cdef np_mint inv_elem, factor

    # Gaussian elimination
    for i in range(n):
        if A[i, i].value == 0:
            raise ValueError("Matrix is singular in modular arithmetic")

        # Calculate the inverse of the diagonal element
        inv_elem = (<np_mint>A[i, i]).inv()

        # Normalize row i
        for k in range(n):
            A[i, k] = A[i, k] * inv_elem
            inv_matrix[i, k] = inv_matrix[i, k] * inv_elem

        # Eliminate column i in other rows
        for j in range(n):
            if i != j:
                factor = A[j, i]
                for k in range(n):
                    A[j, k] = A[j, k] - factor * A[i, k]
                    inv_matrix[j, k] = inv_matrix[j, k] - factor * inv_matrix[i, k]

    return inv_matrix
