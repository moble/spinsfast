import os
import glob
import time
from os.path import isdir, join, dirname, realpath
from setuptools import setup, Extension
from distutils.sysconfig import get_python_lib


# NOTE: Don't change the following line; it is modified automatically in the
# github actions build step, based on the version given in pyproject.toml
version = "104.2022.4"

try:
    import numpy
    numpy_inc = numpy.get_include()
except:
    numpy_inc = os.path.join(get_python_lib(plat_specific=1), 'numpy', 'core', 'include')

## The following block is added for nicer behavior with `module`s on clusters
from os import environ
IncDirs = [numpy_inc, "include",]
LibDirs = ["lib",]
## See if GSL_HOME is set; if so, use it
if "GSL_HOME" in environ :
    IncDirs += [os.path.join(environ["GSL_HOME"], 'include')]
    LibDirs += [os.path.join(environ["GSL_HOME"], 'lib')]
## See if FFTW3_HOME is set; if so, use it
if "FFTW3_HOME" in environ :
    IncDirs += [
        os.path.join(environ["FFTW3_HOME"], 'include'),
        os.path.join(environ["FFTW3_HOME"], 'Library', 'include'),
        environ["FFTW3_HOME"]+'/include',  # stupid Windows
        environ["FFTW3_HOME"]+'/Library/include',  # stupid Windows
    ]
    LibDirs += [
        environ["FFTW3_HOME"],
        os.path.join(environ["FFTW3_HOME"], 'lib'),
        os.path.join(environ["FFTW3_HOME"], 'Library', 'lib'),
        os.path.join(environ["FFTW3_HOME"], 'Library', 'bin'),
        environ["FFTW3_HOME"]+'/Library/lib',  # stupid Windows
        environ["FFTW3_HOME"]+'/Library/bin',  # stupid Windows
    ]
    # fftw_rpath = '-Wl,-rpath,{FFTW3_HOME}/lib'.format(FFTW3_HOME=environ["FFTW3_HOME"])
# If /opt/local directories exist, use them
if isdir('/opt/local/include'):
    IncDirs += ['/opt/local/include']
if isdir('/opt/local/lib'):
    LibDirs += ['/opt/local/lib']


from sys import platform
on_windows = ('win' in platform.lower() and not 'darwin' in platform.lower())
if on_windows:
    extra_compile_args = ['-std=c99', '-O3', '-DNPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION']
    # # Use the below for MSVC; assuming mingw/gcc by default.  However, also note that FFTW's
    # # complex type appears to break MSVC, and I don't know how to solve it.
    # extra_compile_args = ['/O2', '/DNPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION']  # No c99 equivalent for MSVC
else:
    extra_compile_args = ['-std=c99', '-O3', '-fPIC', '-DNPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION']


long_description = """\
This module is a lightly modified version of the code originally written by Huffenberger and
Wandelt.  It enables the user to transform between modes of a spin-weighted spherical-harmonic
decomposition and values of that function on a spherical gride.
"""

setup(name = 'spinsfast',
      version = version,
      packages = ['spinsfast'],
      package_dir = {'spinsfast': 'python'},
      url = 'https://github.com/moble/spinsfast',
      maintainer = 'Mike Boyle',
      maintainer_email = 'mob22@cornell.edu',
      description='Fast and exact spin-s spherical-harmonic transforms',
      long_description=long_description,
      ext_modules = [Extension(
          name = 'spinsfast.cextension',
          sources = [os.path.join('python', 'cextension.c')] + glob.glob(os.path.join('code', '*.c')),
          include_dirs=IncDirs,
          libraries=['fftw3'],
          library_dirs=LibDirs,
          extra_compile_args=extra_compile_args,
          #extra_link_args=[fftw_rpath],
      )],
)
