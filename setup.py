from setuptools import setup
from os.path import abspath, dirname, join

this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='indiek-gui',
    python_requires='>=3.8',
    version='0.0.2',
    url='https://pypi.org/project/indiek-gui/',
    description='Tkinter GUI for IndieK',
    long_description=long_description,
    author='Adrian Ernesto Radillo',
    author_email='adrian.radillo@gmail.com',
    license='GNU Affero General Public License v3.0',
    packages=['indiek.gui'],
    install_requires=['indiek-core == 0.1.2'],
    extras_require={
        'dev': [
            'pytest',
            'pytest-pep8',
            'pytest-cov'
        ]
    },
    project_urls={
        'GitHub': 'https://github.com/indiek/indiek-gui',
        'Documentation': 'https://indiekgui.readthedocs.io/en/latest/'
    },
)