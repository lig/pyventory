import sys

from setuptools import setup, find_packages


install_requires = ['six', 'attrs']

if sys.version_info < (3, 4):
    install_requires.append('pathlib')

setup(
    name='Pyventory',
    use_scm_version=True,
    description='Ansible Inventory implementation that uses Python syntax',
    url='https://github.com/lig/pyventory',
    author='Serge Matveenko',
    author_email='s@matveenko.ru',
    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Systems Administration',
    ],
    keywords='devops ansible inventory',
    packages=find_packages(),
    setup_requires=['setuptools_scm', 'pytest-runner'],
    install_requires=install_requires,
    extras_require={
        'test': ['pytest', 'tox'],
    },
    entry_points={
        'console_scripts': [
            'pyventory=pyventory.cli:main',
        ],
    },
)
