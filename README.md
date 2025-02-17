# ModularArithmetic

A high-performance implementation of modular arithmetic rules for Python and NumPy, featuring both pure Python and optimized Cython-based NumPy operations.

## Features

- Pure Python modular arithmetic operations
- NumPy-accelerated operations using Cython
- Support for basic arithmetic operations (addition, subtraction, multiplication, division)
- Efficient handling of large numbers and arrays
- Compatible with both Python and NumPy workflows

## Installation

### Prerequisites

Before installing, ensure you have the following:
- Python 3.7 or higher
- pip
- setuptools
- Cython (for NumPy integration)
- NumPy (for array operations)

### Install Options

Choose the installation option that best suits your needs:

#### Complete Installation (Recommended)
```bash
pip install ModularArithmetic
# or
pip install ModularArithmetic[all]
```

#### Pure Python Only
```bash
pip install ModularArithmetic[pure]
```

#### NumPy Integration Only
```bash
pip install ModularArithmetic[numpy]
```

### Manual Build

If you need to build from source:

1. Clone the repository:
   ```bash
   git clone https://github.com/MaxMassov/ModularArithmetic/
   cd ModularArithmetic
   ```

2. Install development dependencies:
   ```bash
   pip install setuptools cython numpy
   ```

3. Build the Cython extension:
   ```bash
   python setup.py build_ext --inplace
   ```

   **VS Code Users:** You can also build using the included task:
   - Press `Ctrl+Shift+B`
   - Select "Build Cython Extension"

## Quick Start

```python
# Pure Python usage
from ModularArithmetic.mint import mint
x = mint(5, mod=7)  # Creates 5 mod 7
y = mint(3, mod=7)  # Creates 3 mod 7
result = x + y      # Addition in modulo 7
```
```python
# NumPy integration
from ModularArithmetic.np_mint import np_mint
import numpy as np

# Create modular arrays
arr = np.array([1, 2, 3, 4, 5])
mod_arr = np_mint(arr, mod=7)  # Convert to modular array
```

## Documentation

The following examples and explanation are shown for both classes mint and np_mint (the numpy version of mint) because of their simirality. The main goal of all opeartions is to follow the rules of modular arithmetic.

### Initialization

```python
from ModularArithmetic.mint import mint

a = mint(5, mod=3) # creates a mint instance that represents 5 in the equivalence class modulo 3
b = mint(13, 15) # creates a mint instance that represents 13 in the equivalence class modulo 15
c = mint(-3, 4)
d = mint(15.5, 10) # 15 in the equivalence class modulo 10
e = mint(False, 2.6) # 0 in the equivalence class modulo 2

f = mint(4, mod=1) # raises ValueError, because modulo must be at least 2
```
```python
from ModularArithmetic.np_mint import np_mint

g = np_mint(5, mod=3)
h = np_mint(13, 15)
```

There are also subclasses for the equivalence class of 2, 3, 5 and 7.

```python
from ModularArithmetic.mint import mint, mint2, mint3, mint5, mint7

x = mint5(2) # creates a mint instance that represents 2 in the equivalence class modulo 5
y = mint3(16) # creates a mint instance that represents 16 in the equivalence class modulo 3
```
```python
from ModularArithmetic.np_mint import np_mint, np_mint2, np_mint3, np_mint5, np_mint7

a = np_mint2(5)
b = np_mint7(13)
```

### Attributes

All instance's attributes are const and cannot be changed.

```python
from ModularArithmetic.mint import mint

x = mint(4, 6)
print(f"gcd({x.value}, {x.mod}) = {x.vm_gcd}") # gcd(4, 6) = 2
```
```python
from ModularArithmetic.np_mint import np_mint 

y = np_mint(5, 3)
print(f"gcd({y.value}, {y.mod}) = {y.vm_gcd}") # gcd(2, 3) = 1 
```

### Representation

There are 3 options how to represent of mint and np_mint instances.

```python
from ModularArithmetic.mint import mint

a = mint(3, mod=5)
print(a) # 3
print(a.__repr__()) # mint(3, mod=5)
print(a.parametric()) # 3 + 5 * k
```
```python
from ModularArithmetic.np_mint import np_mint

b = np_mint(4, 7)
print(b) # 4
print(b.__repr__()) # mint(4, mod=7)
print(b.parametric(param_name="n")) # 4 + 7 * n
```

### Type conversion

The instance of mint or np_mint can be converted to int of float:

```python
from ModularArithmetic.mint import mint

a = mint(13, mod=15)
print(int(a)) # 13
# mint.to_int treats value as an integer in a given base 
print(a.to_int(base=3)) # 7 
print(float(a)) # 13.0
```
```python
from ModularArithmetic.np_mint import np_mint 

b = np_mint(4, 7)
print(int(b)) # 4
print(b.to_int(5)) # 4
print(float(b)) # 4.0
```

As it was shown above int, float and bool values can be used in initialization of modular integer instances. However, these conversion could be prohibited by setting static class variable _DISABLE_INT2MINT_CONVERSION to True. There is an example, how it works:
```python
from ModularArithmetic.mint import mint

a = mint(3, mod=5)
# Default `_DISABLE_INT2MINT_CONVERSION` value
print(a.int2mint) # False
# method with no int to mint conversion
print(2 * a) # 1
# int converts to mint during the execution
print(a + 1) # 4
mint.set_int2mint(1)
print(mint.int2mint) # True
# Now int cannot be converted to mint
print(2 * a) # the same result
print(a + 1) # raises TypeError
```
```python
from ModularArithmetic.np_mint import np_mint 

b = np_mint(3, mod=5)
print(b.int2mint) # False
print(2 * b) # 1
print(b + 1) # 4
mint.set_int2mint(True)
print(np_mint.int2mint) # True
print(2 * b) # 1
print(b + 1) # raises TypeError
```

There are also other options to change the _DISABLE_INT2MINT_CONVERSION variable state:
   * mint.change_int2mint() -- toggles its state to the opposite value
   * mint.activate_int2mint() -- set its value to False
   * mint.disable_int2mint() -- set its value to True

The value of a variable affects the operation of only the following methods:
   * multiplication (`__mul__`, `__rmul__`),
   * powering (`__pow__`),
   * division (`__floordiv__`, `__truediv__`, `__rfloordiv__`, `__rtruediv__`),
   * bit shifting (`__lshift__`)

## Contributing

We welcome contributions! Please see our [contributing guidelines]() for details on how to get involved.

## License

This project is licensed under [insert license] - see the [LICENSE]() file for details.

## Citation

If you use this package in your research, please cite:

```bibtex
@software{ModularArithmetic,
  title = {ModularArithmetic: Python/NumPy Modular Arithmetic Implementation},
  author = {[Maksim Massov]},
  year = {[2025]},
  url = {[https://github.com/MaxMassov/ModularArithmetic/]}
}
```
