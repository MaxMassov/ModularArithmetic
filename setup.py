from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
import numpy as np

# Define the Cython extension for np_mint
extensions = [
    Extension(
        "ModularArithmetic.np_mint",
        sources=["np_mint/np_mint.pyx"],
        extra_compile_args=["/std:c++17"],  # Enable C++17
        include_dirs=[np.get_include()],    # Include NumPy headers
        language="c++"
    ),
]

# Common setup configuration
setup(
    name="ModularArithmetic",
    version="0.1",
    packages=find_packages(),  # Include all packages
    ext_modules=cythonize(extensions),  # Build Cython extensions
    include_dirs=[np.get_include()],  # Include NumPy headers for compilation
    install_requires=[],  # Common dependencies (if any)
    extras_require={
        "pure": [],  # Optional: Dependencies for pure Python group (if any)
        "numpy": ["numpy"],  # Optional: Dependencies for NumPy group
        "all": ["numpy"],  # Optional: Install both groups
    },
    python_requires=">=3.7",  # Specify Python version compatibility
    package_data={
        # Include pure Python files only if "pure" or "all" is selected
        "ModularArithmetic.mint": ["*.py"],
        # Include NumPy-related files only if "numpy" or "all" is selected
        "ModularArithmetic.np_mint": [
            "*.pyx",  # Include all .pyx files
            "*.pxd",  # Include all .pxd files
            "*.cpp",  # Include all .cpp files
            "*.h",    # Include all .h files
            "*.pyd",  # Include compiled .pyd files (if needed)
        ],
    },
    exclude_package_data={
        # Exclude NumPy-related files if "pure" is selected
        "ModularArithmetic": ["np_mint/*"],
    },
)
