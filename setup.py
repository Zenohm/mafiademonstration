import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='mafiademonstration',
    version='0.4.5',
    author='Isaac Smith, Hei Jing Tsang',
    author_email='sentherus@gmail.com',
    description='A user friendly interface for playing a simplified game of Mafia.',
    long_description=read('README.rst'),
    license='MIT',
    keywords=(
        "Python, kivy, pytest, projects, project, "
        "documentation, setup.py, package "
    ),
    url='https://github.com/zenohm/mafiademonstration',
    install_requires=[
        'kivy>=1.9.1',
        'click',
    ],
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    tests_require=['unittest'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: X11 Applications',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Graphics :: Presentation',
        'Topic :: Software Development :: User Interfaces',
    ],
)
