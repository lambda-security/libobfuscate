from setuptools import setup, find_packages

setup(
    name='libobfuscate',
    version='1.0.0',
    #author='',
    #url='https://github.com/user/libofuscate',
    description = 'A module to obfuscate placeholders in a string with variable-lenth random strings.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.6',
)
