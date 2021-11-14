from setuptools import find_packages, setup

setup(
    name="Klimawatch",
    description="Ein Open Data-Plattform zur Darstellung von kommunalen CO2-Emissionen und Schutzkonzepten",
    version="0.1.0",
    author="Code for Germany",
    author_email="muenster@codefor.de",
    url="https://klimawatch.de/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: POSIX",
    ],
    packages=find_packages(),
    scripts=[],
    python_requires="~=3.7",
    install_requires=["pandas>=1.2.4", "plotly>=5.0.0", "numpy", "scipy"],
    extras_require={
        "dev": [
            "black",
            "docformatter",
            "jupyter",
            "pre-commit",
            "pylama",
            "pytest",
            "rope",
        ],
    },
)
