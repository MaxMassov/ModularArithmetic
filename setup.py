from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

extensions = [
    Extension(
        "np_mint",
        ["np_mint.pyx"],
        extra_compile_args=["/std:c++17"],  # Enable C++17
        include_dirs=[np.get_include()],
        language="c++"
    )
]

setup(
    name="np_mint",
    ext_modules=cythonize(extensions),
)