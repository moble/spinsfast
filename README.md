# spinsfast
Fast and exact spin-s spherical-harmonic transforms

This code is a lightly modified version of the code hosted
[here](http://astrophysics.physics.fsu.edu/~huffenbe/research/spinsfast/index.html)
by Huffenberger, based on work by
[Huffenberger and Wandelt](http://stacks.iop.org/0067-0049/189/255).

My modifications

  * add python 3.x compatibility;
  * make it easier to install as a python module;
  * add integration with [conda](http://conda.pydata.org/docs/) and
    [binstar](https://binstar.org/), for easy installation
    ([see below](#installation)).


# License

The original work is licensed under GPL, so that's what I've had to license
this under as well.  (I usually go for the more liberal MIT license, but GPL is
cool too.)  See the LICENSE file in this directory for more details.

I based my work on Huffenberger and Wandelt's "Revision 104, 13 Apr 2012",
which is current as of this writing.  Whenever I notice updates on their end, I
will update this code, so feel free to open an
[issue](https://github.com/moble/spinsfast/issues) to notify me.  To see more
specifically what I've added, look through the
[commits](https://github.com/moble/spinsfast/commits/master); my contributions
are just everything since the initial commit.


# Example Usage

A convenient ipython notebook is found in the `example` directory, and can also
be [viewed directly online](http://nbviewer.ipython.org/github/moble/spinsfast/blob/master/example/spinsfast.ipynb).
It shows some example python code that can be used to run this module, and explains
some of the conventions established by the `spinsfast` authors.

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
conda install --channel moble spinsfast
```

(Note that the explanation for how to create and upload conda packages is
contained in the [README](https://github.com/moble/fftw/blob/master/README.md)
for my [FFTW installer](https://github.com/moble/fftw).)

## Manual installation

Manual installation of this package is slightly more delicate.  The
[FFTW package](http://www.fftw.org/) must be installed first.  This is usually
very simple.  But the resulting header and library must be found by the
compilation step for this package.  You can first simply try to run

```bash
python python/setup.py install
```

from the top directory of the `spinsfast` code.

If this doesn't work, you can read the error message, but the most likely
problem is that the compiler cannot find the `fftw` header, or the linker
cannot find the `fftw` library.  To solve these problems, you will need to run
something more like this:

```bash
export LIBRARY_PATH=/path/to/fftw/lib
export C_INCLUDE_PATH=/path/to/fftw/include
python python/setup.py install
```

Alternatively, you could try to alter `python/setup.py` to point to the right
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
