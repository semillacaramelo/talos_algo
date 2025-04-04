from setuptools import setup, find_packages

setup(
    name="talos_algo",
    version="0.1.0",
    description="Trading algorithm package",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
)