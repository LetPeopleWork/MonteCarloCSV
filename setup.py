from setuptools import setup, find_packages

setup(
    name='montecarlocsv',
    version='1.0.3',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'MonteCarloCSV': ['logo.png'],
    },
    install_requires=[
        "argparse", "pandas", "numpy", "matplotlib"
    ],
    entry_points={
        'console_scripts': [
            'montecarlocsv=MonteCarloCSV.main:main',
        ],
    },
    author='Benjamin Huser-Berta',
    author_email='benj.huser@gmail.com',
    description='A package to generate Monte Carlo Simulations from CSV files.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://letpeople.work',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
