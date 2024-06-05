"""Jaclang setup file."""

from setuptools import find_packages, setup  # type: ignore


VERSION = "0.0.1"

setup(
    name="jac-streamlit",
    version=VERSION,
    packages=find_packages(include=["jac_streamlit", "streamlit.*"]),
    install_requires=["streamlit", "pydot", "streamlit-agraph"],
    package_data={
        "": ["*.ini"],
    },
    entry_points={
        "jac": ["dot_view = jac_streamlit.streamlit:JacCmd"],
    },
    url="https://github.com/Jaseci-Labs/jaclang",
)
