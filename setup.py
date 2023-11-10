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
        "plotly" 
    ],
    author="Sebastien Caron",
    description="Projet dans le cadre de la maitrise",
    url="",  # Add your project's URL if available.
    classifiers=["Programming Language :: Python :: 3"],
)