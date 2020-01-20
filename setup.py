from os import path

from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name='imgcompare',
    packages=find_packages(include=['imgcompare']),
    version='1.0.0',
    description='compares two images for equality or a difference percentage',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Jonas Hahn',
    author_email='jonas.hahn@datenhahn.de',
    url='https://github.com/datenhahn/imgcompare',
    download_url='https://github.com/datenhahn/imgcompare/tarball/1.0.0',
    project_urls={
        'Documentation': 'https://github.com/datenhahn/imgcompare',
        'Source': 'https://github.com/datenhahn/imgcompare',
        'Tracker': 'https://github.com/datenhahn/imgcompare/issues',
    },
    keywords='image, compare',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ],
    license='MIT',
    python_requires='>=2.6, <3',
    install_requires=['pillow<7']
)
