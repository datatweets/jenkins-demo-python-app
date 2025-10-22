from setuptools import setup, find_packages

setup(
    name='jenkins-demo-python-app',
    version='1.0.0',
    description='Demo Python application for Jenkins CI/CD',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'pytest>=7.4.3',
        'pytest-cov>=4.1.0',
        'pylint>=3.0.3',
        'black>=23.12.1',
    ],
)
