from setuptools import find_packages, setup

EXCLUDE_FROM_PACKAGES = [
    'tests'
]

version = "0.1.0"

setup(
    name='All Voice',
    version=version,
    url='',
    author='Lampshady',
    author_email='lampshady24@gmail.com',
    description=('A Python library for handling requests from Alexa'
                 'and API AI (Google Home)'),
    license='MIT',
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    scripts=['django/bin/django-admin.py'],
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)

