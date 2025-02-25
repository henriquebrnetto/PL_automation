from setuptools import setup, find_packages

setup(
    name='praire_data',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'numpy',
        'pandas',
        'matplotlib'
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='A module for handling PrairieLearn course data',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/praire_data',  # Update with your repository URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Update with your license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)