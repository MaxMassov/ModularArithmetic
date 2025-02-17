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
from ModularArithmetic.np_mint import np_mint

x = mint(5, mod=3) # creates a mint instance that represents 5 in the equivalence class modulo 3
y = mint(13, 15) # creates a mint instance that represents 13 in the equivalence class modulo 15

z = mint(4, mod=1) # raises ValueError, because modulo must be at least 2

x = np_mint(5, mod=3)
y = np_mint(13, 15)
```

There are also subclasses for the equivalence class of 2, 3, 5 and 7.

```python
from ModularArithmetic.mint import mint, mint2, mint3, mint5, mint7
from ModularArithmetic.np_mint import np_mint, np_mint2, np_mint3, np_mint5, np_mint7

x = mint5(2) # creates a mint instance that represents 2 in the equivalence class modulo 5
y = mint3(16) # creates a mint instance that represents 16 in the equivalence class modulo 3

x = np_mint2(5)
y = np_mint7(13)
```


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
