from setuptools import setup, find_packages
import os

# Read version from _version.py
def get_version():
    version_file = os.path.join(os.path.dirname(__file__), 'darktrace', '_version.py')
    with open(version_file) as f:
        exec(f.read())
    return locals()['__version__']

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='darktrace-sdk',
    version=get_version(),
    description='A modern, modular, and complete Python SDK for the Darktrace API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='LegendEvent',
    author_email='ridge.thrill7680@eagereverest.com',
    url='https://github.com/LegendEvent/darktrace-sdk',
    packages=['darktrace'],
    package_data={
        'darktrace': ['py.typed'],
    },
    install_requires=[
        'requests>=2.25.1',
    ],
    python_requires='>=3.7',
    include_package_data=True,
    license='MIT',
    keywords='darktrace sdk api security threat-visualizer',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
) 