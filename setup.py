from setuptools import setup, find_packages

setup(
    name="VariationQuadratique",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit",
        "pandas",
        "numpy",
        "plotly",
        "subprocess"  # Note: 'subprocess' is part of the standard library in Python 3, so it doesn't need to be installed separately.
    ],
    author="Sebastien Caron",
    description="Projet dans le cadre de la maitrise",
    url="",  # Add your project's URL if available.
    classifiers=["Programming Language :: Python :: 3"],
)