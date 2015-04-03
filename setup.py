from setuptools import setup

try:
    long_description = open('README.rst').read()
except IOError:
    long_description = ''

setup(
    name='django-material',
    version='0.2.0',
    description='Material design for django forms and admin',
    license='BSD',
    author='Mikhail Podgurskiy',
    author_email='kmmbvnr@gmail.com',
    url='http://github.com/viewflow/django-material',
    keywords="django",
    packages=['material',
              'material.templatetags',
              'material.admin',
              'material.admin.templatetags'],
    include_package_data=True,
    zip_safe=False,
    platforms=['any'],
    classifiers=[
        'Framework :: Django',
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
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
