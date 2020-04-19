from setuptools import setup, find_packages

setup(
    install_requires=['pywin32'],
    name='NotesComPy',
    version=0.1,
    packages=find_packages(),
    url='https://github.com/dmtrbrlkv/NotesComPy',
    author='Dmitry Burlakov',
    author_email='dmtrbrlkv@gmail.com',
    description='Python classes for manipulating Notes/Domino objects via COM, advanced functionality and data export',
)
