from setuptools import setup, find_packages
from aaprom import __version__
setup(
    name="allianceauth-prometheus-exporter",
    version=__version__,
    author="AaronKable",
    author_email="aaronkable@gamil.com",
    description="Export Alliance Auth metrics to Prometheus.",
    license="Apache",
    keywords="allianceauth monitoring prometheus",
    packages=find_packages(),
    install_requires=[
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: Django",
        "Topic :: System :: Monitoring",
        "License :: OSI Approved :: Apache Software License",
    ],
)
