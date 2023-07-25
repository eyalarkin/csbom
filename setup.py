from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()
setup(
    name = 'csbom',
    version = '0.0.1',
    author = 'Eyal Arkin',
    author_email = 'eyal@scribesecurity.com',
    license = 'Apache License, Version 2.0',
    description = 'cli tool for analyzing sbom files',
   #  url = '<github url where the tool code will remain>',
    py_modules = ['csbom', 'app'],
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    entry_points = '''
        [console_scripts]
        csbom=csbom:cli
    '''
)
