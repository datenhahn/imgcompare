from os import path

from setuptools import setup, find_packages

dir_path = path.dirname(path.realpath(__file__))

version = {}
with open(path.join(dir_path, "imgcompare/version.py")) as fp:
    exec(fp.read(), version)

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name='imgcompare',
    packages=find_packages(include=['imgcompare']),
    version=version['__version__'],
    description='compares two images for equality or a difference percentage',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Jonas Hahn',
    author_email='jonas.hahn@datenhahn.de',
    url='https://github.com/datenhahn/imgcompare',
    download_url='https://github.com/datenhahn/imgcompare/tarball/' + version['__version__'],
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
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    license='MIT',
    python_requires='>=3.5',
    install_requires=['pillow>=7.0.0']
)
