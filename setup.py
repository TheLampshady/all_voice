from setuptools import find_packages, setup

version = "0.1.1"

setup(
    name='all_voice',
    version=version,
    url='https://github.com/TheLampshady/all_voice',
    author='Lampshady',
    author_email='lampshady24@gmail.com',
    description=('A Python library for handling requests from Alexa'
                 'and API AI (Google Home)'),
    license='MIT',
    packages=find_packages(exclude=['tests']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        "Topic :: Home Automation",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='alexa',
)
