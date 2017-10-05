from os.path import isdir
from setuptools import setup, Extension
from distutils.sysconfig import get_python_lib
import os
import glob
import time

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
    IncDirs += [environ["GSL_HOME"]+'/include']
    LibDirs += [environ["GSL_HOME"]+'/lib']
## See if FFTW3_HOME is set; if so, use it
if "FFTW3_HOME" in environ :
    IncDirs += [environ["FFTW3_HOME"]+'/include']
    LibDirs += [environ["FFTW3_HOME"]+'/lib']
# If /opt/local directories exist, use them
if isdir('/opt/local/include'):
    IncDirs += ['/opt/local/include']
if isdir('/opt/local/lib'):
    LibDirs += ['/opt/local/lib']

# Construct the version number, starting with spinsfast's own version (104) and appending the date
# and time this python version was created.
version = '104.'
if "datetime" in environ:
    version += environ["datetime"]
else:
    version += time.strftime("%Y.%m.%d.%H.%M.%S", time.gmtime())
with open('python/_version.py', 'w') as f:
    f.write('__version__ = "{0}"'.format(version))

extension = Extension(
    name = 'spinsfast.cextension',
    sources = ['python/cextension.c'] + glob.glob('code/*.c'),
    include_dirs=IncDirs,
    libraries=['fftw3'],
    library_dirs=LibDirs,
    extra_compile_args=['-std=c99','-fPIC','-O3'],
)

setup(name = 'spinsfast',
      version = version,
      packages = ['spinsfast'],
      package_dir = {'spinsfast': 'python'},
      url = 'https://github.com/moble/spinsfast',
      maintainer = 'Mike Boyle',
      maintainer_email = 'mob22@cornell.edu',
      ext_modules = [Extension(
          name = 'spinsfast.cextension',
          sources = ['python/cextension.c'] + glob.glob('code/*.c'),
          include_dirs=IncDirs,
          libraries=['fftw3'],
          library_dirs=LibDirs,
          extra_compile_args=['-std=c99','-fPIC','-O3']),
      ],
)
