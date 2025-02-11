import numpy as np
from np_mint import np_mint, modular_matrix_inv, modular_matrix_det

# Create modular integers
a = np_mint(5, 7)
b = np_mint(3, 7)
arr = np.array([[a, b], [b, a]])
print(np_mint(3, 5) * np.array([np_mint(3, 5), 5]))
print(np_mint(3, 5) + np.array([np_mint(3, 5), 5]))
print(modular_matrix_inv(arr))
print(modular_matrix_det(arr))

x = np.array([a])
print(f"x = {x.dtype}")  # 5
arr = np.array([a, b])
result = sum((a, b), np_mint(0, 7))
print(np.add.reduce(np.array([np_mint(5, 7), np_mint(3, 7)])))
print(f"Result: {result.__repr__()}")  # 1 (mod 7)

# Individual operations
print(f"a = {a}")  # 5
print(f"b = {b}")  # 3
print(f"a + b = {a + b}")  # 1 (mod 7)
print(f"a * b = {a * b}")  # 1 (mod 7)

# Create arrays of np_mint objects
arr1 = np.array([a, b])
print(f"Array 1: {arr1}")

# For arithmetic with regular numbers:
arr2 = np.array([1, 1])
# Need to convert regular numbers to np_mint objects with the same modulus
arr2_mint = np.array([np_mint(x, 7) for x in arr2])

# Now add arrays
result = arr1 + arr2_mint
print(f"Result: {result}")

# Or use list comprehension for operations
result = np.array([x + 1 for x in arr1])
print(f"Array + 1: {result}")
