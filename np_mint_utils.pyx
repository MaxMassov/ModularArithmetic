# -*- coding: utf-8 -*-
# cython: language_level=3, boundscheck=False, wraparound=False

cimport numpy as cnp
import numpy as np
from np_mint cimport np_mint
from copy import deepcopy  # For creating a deep copy of the input matrix

cpdef cnp.ndarray[object, ndim=2] modular_matrix_inv(cnp.ndarray[object, ndim=2] A):
    """
    Compute the inverse of a square matrix in modular arithmetic using Gaussian elimination (non-inplace).
    
    Args:
        A (cnp.ndarray[np_mint, ndim=2]): A square matrix of np_mint objects.

    Returns:
        cnp.ndarray[np_mint, ndim=2]: The inverse matrix in modular arithmetic.
    """
    cdef int n = A.shape[0]
    A_copy = deepcopy(A)  # Create a deep copy of the matrix
    cdef cnp.ndarray[object, ndim=2] inv_matrix = np.empty((n, n), dtype=object)

    # Initialize inv_matrix as the identity matrix
    for i in range(n):
        for j in range(n):
            inv_matrix[i, j] = np_mint(1 if i == j else 0, A[0, 0].mod)

    cdef np_mint inv_elem, factor

    # Gaussian elimination on the copy of the matrix
    for i in range(n):
        if A_copy[i, i].value == 0:
            raise ValueError("Matrix is singular in modular arithmetic")

        inv_elem = (<np_mint>A_copy[i, i]).inv()

        for k in range(n):
            A_copy[i, k] = A_copy[i, k] * inv_elem
            inv_matrix[i, k] = inv_matrix[i, k] * inv_elem

        for j in range(n):
            if i != j:
                factor = A_copy[j, i]
                for k in range(n):
                    A_copy[j, k] = A_copy[j, k] - factor * A_copy[i, k]
                    inv_matrix[j, k] = inv_matrix[j, k] - factor * inv_matrix[i, k]

    return inv_matrix

cpdef np_mint modular_matrix_det(cnp.ndarray[object, ndim=2] A):
    """
    Compute the determinant of a square matrix in modular arithmetic using Gaussian elimination.
    
    Args:
        A (np.ndarray[np_mint, ndim=2]): A square matrix of np_mint objects.
    
    Returns:
        np_mint: The determinant of the matrix in modular arithmetic.
    """
    cdef int n = A.shape[0]
    cdef cnp.ndarray[object, ndim=2] matrix = A.copy()  # Work on a copy of the matrix
    cdef np_mint det = np_mint(1, A[0, 0].mod)  # Start with determinant = 1
    cdef int i, j, k
    cdef np_mint factor

    for i in range(n):
        if matrix[i, i].value == 0:
            # Find a row below with a non-zero element in column i
            for j in range(i + 1, n):
                if matrix[j, i].value != 0:
                    # Swap rows i and j
                    matrix[[i, j]] = matrix[[j, i]]
                    det = det * np_mint(-1, det.mod)  # Swapping rows changes the sign of the determinant
                    break
            else:
                return np_mint(0, det.mod)  # Singular matrix, determinant is 0

        # Multiply the diagonal element to the determinant
        det = det * matrix[i, i]

        # Normalize row i
        for j in range(i + 1, n):
            factor = matrix[j, i] * (<np_mint>matrix[i, i]).inv()
            for k in range(i, n):
                matrix[j, k] = matrix[j, k] - factor * matrix[i, k]

    return det
