
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='onaudience_api',
     version='0.1',
     scripts=['api_dmp.py'] ,
     author="Kacper Wozniak",
     author_email="kacper.wozniak@audiencenetwork.pl",
     description="Package to assign datapoints to users",
     packages=setuptools.find_packages())

