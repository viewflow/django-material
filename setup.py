from setuptools import setup

import material

try:
    long_description = open('README.rst').read()
except IOError:
    long_description = ''

setup(
    name='django-material',
    version=material.__version__,
    description='Material Design for Django applications',
    license='BSD',
    author='Mikhail Podgurskiy',
    author_email='kmmbvnr@gmail.com',
    url='http://github.com/viewflow/django-material',
    keywords=["django", "forms", "admin", "crud"],
    packages=[
        'material',
        'material.renderers',
        'material.templatetags'
    ],
    include_package_data=True,
    zip_safe=False,
    platforms=['any'],
    install_requires=[
        'django>=2.0a1',
    ],
    classifiers=[
        'Framework :: Django',
        "Framework :: Django :: 2.0",
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
        'Topic :: Software Development :: User Interfaces',
    ],
)
