import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

readme = (
        'Library for getting cli user responses in a sane way'
        'without need for extensive validation')

with open('README.rst') as readme_source:
    readme = readme_source.read()

details = {}
with open(os.path.join(here, 'enquiries', '__details__.py')) as detail_source:
    exec(detail_source.read(), details)

setup(
        name=details['__title__'],
        packages=find_packages(exclude=['docs', 'tests']),
        version=details['__version__'],
        description=details['__description__'],
        long_description=readme,
        author=details['__author__'],
        author_email=details['__author_email__'],
        install_requires=['curtsies'],
        url=details['__url__'],
        keywords=['cli', 'prompt', 'input'],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
            'Operating System :: POSIX',
            'Programming Language :: Python :: 3 :: Only',
            'Topic :: Utilities'
            ],
        license='MPLv2',
        python_requires='>=3',
        )
