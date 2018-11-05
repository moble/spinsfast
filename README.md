<a href="https://zenodo.org/badge/latestdoi/30340582"><img align="right" src="https://zenodo.org/badge/30340582.svg" alt="DOI"></a>

# spinsfast
Fast and exact spin-s spherical-harmonic transforms

This code is a lightly modified version of the code hosted
[here](http://astrophysics.physics.fsu.edu/~huffenbe/research/spinsfast/index.html)
by Huffenberger, based on work by
[Huffenberger and Wandelt](http://stacks.iop.org/0067-0049/189/255).

My modifications mostly deal with the user interface:

  * add `multi_map2salm` and `multi_salm2map` for running many similar transformations efficiently;
  * create python wrappers for the `map2salm` and `salm2map` functions to deal with any (reasonable)
    type or shape of input data, including multi-dimensional;
  * add python 3.x compatibility to `python/spinsfast_module.c`;
  * fix segfaults due to use of `free` instead of `fftw_free` when `fftw_malloc` was used;
  * make it easier to install as a python module by trying to detect paths to
    FFTW;
  * fix numerous massive memory leaks in python extension module;
  * include an ipython/jupyter notebook in the `example` directory;
  * add integration with [pip](https://pypi.python.org/pypi/pip)
    and [pypi](https://pypi.python.org/pypi/spinsfast), for easy installation
    ([see below](#installation));
  * add integration with [conda](https://conda.io/docs/)
    and [anaconda.org](https://anaconda.org/moble/spinsfast), for easiest installation
    ([see below](#installation)).

# License

The original work is licensed under GPL, so that's what I have to license this
under as well.  (I usually go for the more liberal MIT license, but GPL is
fine.)  See the `LICENSE` file in this directory for more details.

I based my work on Huffenberger and Wandelt's "Revision 104, 13 Apr 2012",
which is current as of this writing (August 2015).  Whenever I notice updates
on their end, I will gladly update this code, so feel free to open an
[issue](https://github.com/moble/spinsfast/issues) to notify me.  To see more
specifically what I've added, look through the
[commits](https://github.com/moble/spinsfast/commits/master); my contributions
are just everything since the initial commit.


# Example Usage

A convenient ipython/jupyter notebook is found in the `example` directory, and
can also be
[viewed directly online](http://nbviewer.ipython.org/github/moble/spinsfast/blob/master/example/spinsfast.ipynb).
It shows some example python code that can be used to run this module, and
explains some of the conventions established by the `spinsfast` authors.

In the interests of a very short, explicit example, here is one using random `(ell,m)` modes:

```python
from numpy.random import normal, seed
import spinsfast

# Some boilerplate for setting things up:
s = 1  # spin weight of the field
lmax = 8  # maximum ell value used
Ntheta = 2*lmax+1  # Minimum value for accuracy
Nphi = 2*lmax+1  # Minimum value for accuracy
Nlm = spinsfast.N_lm(lmax);  # Total number of complex components of the mode decomposition

# `alm` will hold the mode components as discussed in `example/spinsfast.ipynb`
# Here we just fill it with some random numbers to test it
seed(3124432)  # Seed the random-number generator, for reproducibility
alm = normal(size=(Nlm,)) + 1j*normal(size=(Nlm,))

# This is the key line, where spinsfast converts from (ell,m) modes to values in physical space
f =  spinsfast.salm2map(alm,s,lmax,Ntheta,Nphi)

# We can also convert in the opposite direction like this:
alm2 = spinsfast.map2salm(f,s,lmax)
```


# Installation

## Anaconda

Though manual installation is possible, the best way by far to satisfy these
dependencies is to use the [`anaconda`](http://continuum.io/downloads)
distribution.  This distribution can co-exist with your system python with no
trouble -- you simply add the path to anaconda before your system executables.
It installs into your home directory, so it doesn't require root access.  It
can be uninstalled easily, since it exists entirely inside its own directory.
And updates are trivial.

Once `anaconda` is installed, this package may be installed with the command

```bash
conda install --channel conda-forge spinsfast
```

Note this may also install `numpy` and `fftw` automatically.


## Pip

While generally less robust, this package is also available via `pip`:

```bash
pip install spinsfast
```

Unfortunately, maintaining binary distributions on pip is too time-consuming, so `pip` will try to
compile the source code for you, in which case you will need to have FFTW and a compiler installed.
Unfortunately, `pip` has no good way of handling these dependencies.  See below for environment
variables you may need to set to get compilation working properly.


## Manual installation

Manual installation of this package is slightly more delicate.  The
[FFTW package](http://www.fftw.org/) must be installed first.  This is usually
very simple.  But the resulting header and library must be found by the
compilation step for this package.  You can first simply try to run

```bash
python setup.py install
```

from the top directory of the `spinsfast` code.

If this doesn't work, you can read the error message, but the most likely
problem is that the compiler cannot find the `fftw` header, or the linker
cannot find the `fftw` library.  To solve these problems, you will need to run
something more like this:

```bash
export LIBRARY_PATH=/path/to/fftw/lib
export C_INCLUDE_PATH=/path/to/fftw/include
python setup.py install
```

Alternatively, you could try to alter `setup.py` to point to the right
paths.


# Original installation instructions

Though these are not necessary for installing the python module, the following
are the instructions in the original source code for building the C code.

Get the latest version at:

    http://www.physics.miami.edu/~huffenbe/research/spinsfast/

## Compilation instructions

  1. Edit the file (or make a new file) called build/config.mk so that the proper locations for header and library files are included.

  2. Set the environment variable "build" so that it points to that file. I.e., in bash, say

        export build=build/config.mk 

  3. Build the library and example codes with 

        make

## (Optional) Checking the compilation

Run the example code following the instructions at 

    http://www.physics.miami.edu/~huffenbe/research/spinsfast/
