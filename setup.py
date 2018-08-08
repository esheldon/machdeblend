import os
from distutils.core import setup
from glob import glob

scripts=glob('bin/*')
scripts = [s for s in scripts if '~' not in s]

setup(
    name="machdeblend", 
    version="0.1.0",
    description="Code for working on deblending with machine learning",
    license = "GPL",
    author="Erin Scott Sheldon, Chi-ting Chiang",
    author_email="erin.sheldon@gmail.com",
    scripts=scripts,
    packages=['machdeblend'],
)
