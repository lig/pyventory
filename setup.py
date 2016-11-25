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
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: System :: Systems Administration',
    ],
    keywords='devops ansible inventory',
    packages=find_packages(),
    python_requires='>=3.3',
    setup_requires=['setuptools_scm', 'pytest-runner'],
    install_requires=['attrs'],
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'pyventory=pyventory.cli:main',
        ],
    },
)
