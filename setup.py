from setuptools import setup, find_packages

setup(
    name="inexML",
    version="0.1.0",
    author="Your Name",
    description="Interpolation and extrapolation ML for atomic and molecular data",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    python_requires=">=3.6",
)

