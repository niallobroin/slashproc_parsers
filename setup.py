"""
slashproc_parsers
-----------------

Usual python setup.py install

Package features
````````````````

* Scraping the /proc directory and returning a python dictionary
* Version 0.1
* There will be no dependencies for this package

Links
`````
* `documentation <https://bitbucket.org/niallobyrnes/slashproc_parsers/wiki>`_
* `development <https://bitbucket.org/niallobyrnes/slashproc_parsers/src>`_`

"""

from distutils.core import setup


classifiers = [
    'Development Status :: 1 - Planning',
    'Programming Language :: Python',
    'Operating system :: POSIX :: Linux',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'Topic :: Utilities'
    ]

setup(name='slashproc_parsers',
      version='0.1',
      description='Scraping the /proc directory and returning a python dictionary',
      long_description=__doc__,
      author='Niall OByrnes',
      author_email='nobyrnes@icloud.com',
      url='https://bitbucket.org/niallobyrnes/slashproc_parsers',
      packages=['parsers', 'sp_parser'],
      scripts=['bin/delete_non_compliant_parsers.py'],
      classifiers=classifiers)