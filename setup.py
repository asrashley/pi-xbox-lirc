from setuptools import setup, find_packages
setup(
    name="xboxlirc",
    version="0.2",
    packages = find_packages('src'),  # include all packages under src
    package_dir = {'':'src'},   # tell distutils packages are under src
    install_requires = ['evdev>=0.4'],
    zip_safe=False,
)
