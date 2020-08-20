from os.path import isdir, join, dirname, realpath
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


# Construct the version number, starting with spinsfast's own version (104) and appending the date
# and time this python version was created.
from os import environ
from sys import platform
on_windows = ('win' in platform.lower() and not 'darwin' in platform.lower())
if "package_version" in environ:
    version = environ["package_version"]
    print("Setup.py using environment version='{0}'".format(version))
else:
    print("The variable 'package_version' was not present in the environment")
    try:
        # For cases where this is being installed from git.  This gives the true version number.
        from subprocess import check_output
        if on_windows:
            version = check_output("""git log -1 --format=%cd --date=format:'%Y.%m.%d.%H.%M.%S'""", shell=False)
            version = version.decode('ascii').strip().replace('.0', '.').replace("'", "")
        else:
            try:
                from subprocess import DEVNULL as devnull
                version = check_output("""git log -1 --format=%cd --date=format:'%Y.%-m.%-d.%-H.%-M.%-S'""", shell=True, stderr=devnull)
            except AttributeError:
                from os import devnull
                version = check_output("""git log -1 --format=%cd --date=format:'%Y.%-m.%-d.%-H.%-M.%-S'""", shell=True, stderr=devnull)
            version = version.decode('ascii').rstrip()
        print("Setup.py using git log version='{0}'".format(version))
    except Exception:
        # For cases where this isn't being installed from git.  This gives the wrong version number,
        # but at least it provides some information.
        # import traceback
        # print(traceback.format_exc())
        try:
            from time import strftime, gmtime
            try:
                version = strftime("%Y.%-m.%-d.%-H.%-M.%-S", gmtime())
            except ValueError:  # because Windows
                version = strftime("%Y.%m.%d.%H.%M.%S", gmtime()).replace('.0', '.')
            print("Setup.py using strftime version='{0}'".format(version))
        except:
            version = '0.0.0'
            print("Setup.py failed to determine the version; using '{0}'".format(version))
    version = '104.' + version
with open(os.path.join('python', '_version.py'), 'w') as f:
    f.write('__version__ = "{0}"'.format(version))


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
