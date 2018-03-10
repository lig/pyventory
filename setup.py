import sys

from setuptools import setup, find_packages


setup(
    name='Pyventory',
    use_scm_version=True,
    description='Ansible Inventory implementation that uses Python syntax',
    url='https://github.com/lig/pyventory',
    author='Serge Matveenko',
    author_email='s@matveenko.ru',
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Systems Administration',
    ],
    keywords='devops ansible inventory terraform vars',
    packages=find_packages(),
    setup_requires=['setuptools_scm', 'pytest-runner'],
    install_requires=['attrs', 'ordered-set'],
    extras_require={
        'test': ['pytest', 'tox'],
    },
)
