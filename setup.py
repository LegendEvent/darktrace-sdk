from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='darktrace-sdk',
    version='1.0.0',
    description='A modern, modular, and complete Python SDK for the Darktrace API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='LegendEvent',
    author_email='ridge.thrill7680@eagereverest.com',
    url='https://github.com/LegendEvent/darktrace-sdk',
    packages=find_packages(),
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