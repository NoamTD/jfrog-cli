from setuptools import setup, find_packages

with open("README.md") as fp:
    long_description = fp.read()

requirements = [
    "Click",
    "tabulate",
    "requests"
]


setup(
    name="jfrog",
    version="4.0.0",
    author="Noam Dolovich",
    packages=find_packages(),
    author_email="noam.tzvi.dolovich@gmail.com",
    description="Jfrog cli home assignment",
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=requirements,
    extras_require={"dev": ["wheel", "pytest", "flake8", "autopep8", "black"]},
    entry_points={"console_scripts": ["jfrog-saas = jfrog.cli:cli"]},
    python_requires=">=3.7",
)
