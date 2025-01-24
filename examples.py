import numpy as np
from np_mint import np_mint

print(np_mint(1, 2).int2mint)
# Create modular integers
a = np_mint(5, 7)
b = np_mint(3, 7)

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
