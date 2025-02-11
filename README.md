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
   git clone <repository_url>
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

For detailed usage instructions and API documentation, visit our [documentation page](../../../c:/Users/Maksim/Downloads/link_to_docs).

## Contributing

We welcome contributions! Please see our [contributing guidelines](../../../c:/Users/Maksim/Downloads/link_to_contributing) for details on how to get involved.

## License

This project is licensed under [insert license] - see the [LICENSE](../../../c:/Users/Maksim/Downloads/link_to_license) file for details.

## Citation

If you use this package in your research, please cite:

```bibtex
@software{ModularArithmetic,
  title = {ModularArithmetic: Python/NumPy Modular Arithmetic Implementation},
  author = {[Author Names]},
  year = {[Year]},
  url = {[Repository URL]}
}
```
