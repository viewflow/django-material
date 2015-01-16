from setuptools import setup

try:
    long_description = open('README.rst').read()
except IOError:
    long_description = ''

setup(
    name='django-material',
    version='0.1.0',
    description='Template driven form rendering for django.',
    author='Mikhail Podgurskiy',
    author_email='kmmbvnr@gmail.com',
    url='http://github.com/viewflow/django-material',
    keywords="django",
    packages=['material',
              'material.admin'],
    include_package_data=True,
    zip_safe=False,
    platforms=['any'],
    classifiers=[
        'Framework :: Django',
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: Free for non-commercial use',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development',
        'Topic :: Software Development :: User Interfaces',
    ],
)
