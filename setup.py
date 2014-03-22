from setuptools import setup, find_packages


setup(
    name='hello_mom',
    version='0.1',
    description='Generate simple static photo album',
    author='Dmi Baranov',
    author_email='dmi.baranov@gmail.com',
    packages=find_packages(),
    install_requires=['Pillow', 'pystache'],
)
