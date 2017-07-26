from os.path import isdir
from numpy.distutils.core import setup
from distutils.sysconfig import get_python_lib
import os
import glob

numpy_inc = os.path.join(get_python_lib(plat_specific=1), 'numpy/core/include')

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


def configuration():
    from numpy.distutils.misc_util import Configuration
    config = Configuration(package_name='spinsfast', top_path='spinsfast', package_path='python')
    config.add_extension('spinsfast_module',
                         sources = ['python/spinsfast_module.c'] + glob.glob('code/*.c'),
                         # include_dirs = [numpy_inc,'include'],
                         include_dirs=IncDirs,
                         # libraries=['spinsfast','fftw3'],
                         libraries=['fftw3'],
                         # library_dirs = ["lib"],
                         library_dirs=LibDirs,
                         extra_compile_args=['-std=c99','-fPIC','-O3'],
                         # depends=['lib/libspinsfast.a'],
    )
    return config

setup(version = '104', **configuration().todict())
