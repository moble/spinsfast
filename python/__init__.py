"""Fast and exact spin-s spherical-harmonic transforms

This module contains functions for manipulating spin-weighted spherical harmonics, which are
essentially generalizations of the usual spherical harmonics, but with certain vectorial or
tensorial qualities.  For a full discussion of spin-weighted spherical functions see this paper:
<https://arxiv.org/abs/1604.08140>.

This code is a lightly modified version of the code created by Huffenberger, based on work by
Huffenberger and Wandelt <http://iopscience.iop.org/article/10.1088/0067-0049/189/2/255/meta>.

For examples, see here: <https://github.com/moble/spinsfast/blob/master/example/spinsfast.ipynb>.

"""

from __future__ import absolute_import

from ._version import __version__

# import all the non-underscored functions (underscored functions get ignored)
from .cextension import *

# explicitly import functions with underscores (which will be wrapped)
from .cextension import _salm2map, _map2salm


def salm2map(alm, s, lmax, Ntheta, Nphi):
    """Convert mode weights of spin-weighted function to values on a grid

    Parameters
    ----------
    alm : array_like
        Input array representing mode weights of the spin-weighted function.
    s : int
        Spin weight of the function.
    lmax : int
        The largest `ell` value present in the input array.
    Ntheta : int
        Number of points in the output grid along the polar angle.
    Nphi : int
        Number of points in the output grid along the azimuthal angle.


    Returns
    -------
    map : 2-d array of complex
        Values of the spin-weighted function on grid points of the sphere.


    See also
    --------
    spinsfast.map2salm : Roughly the inverse of this function.


    Notes
    -----

    The input `alm` data should be given in increasing order of `ell` value, always starting with
    (ell, m) = (0, 0) even if `s` is nonzero, proceeding to (1, -1), (1, 0), (1, 1), etc.
    Explicitly, the ordering should match this:

        [[ell,m] for ell in range(lmax+1) for m in range(-ell, ell+1)]

    The input is converted to a contiguous complex numpy array if necessary.

    The output data are presented on this grid of spherical coordinates:

        np.array([[[theta, phi]
                   for phi in np.linspace(0.0, 2*np.pi, num=2*lmax+1, endpoint=False)]
                  for theta in np.linspace(0.0, np.pi, num=2*lmax+1, endpoint=True)])

    Note that `map2salm` and `salm2map` are not true inverses of each other for several reasons.
    First, modes with `ell < |s|` should always be zero; they are simply assumed to be zero on input
    to `salm2map`.  It is also possible to define a `map` function that violates this assumption --
    for example, having a nonzero average value over the sphere, if the function has nonzero spin
    `s`, this is impossible.  Also, it is possible to define a map of a function with so much
    angular dependence that it cannot be captured with the given `lmax` value.  For example, a
    discontinuous function will never be perfectly resolved.


    Example
    -------
    >>> s = -2
    >>> lmax = 8
    >>> Ntheta = Nphi = 2*lmax + 1
    >>> modes = np.zeros(spinsfast.N_lm(lmax), dtype=np.complex128)
    >>> modes[spinsfast.lm_ind(2, 2, 8)] = 1.0
    >>> values = spinsfast.salm2map(modes, s, lmax, Ntheta, Nphi)

    """
    if Ntheta < 2 or Nphi < 1:
        raise ValueError("Input values of Ntheta={0} and Nphi={1} ".format(Ntheta, Nphi)
                         + "are not allowed; they must be greater than 1 and 0, respectively.")
    if lmax < 1:
        raise ValueError("Input value of lmax={0} ".format(lmax)
                         + "is not allowed; it must be greater than 0 and should be greater "
                         + "than |s|={0}.".format(abs(s)))
    import numpy as np
    alm = np.ascontiguousarray(alm, dtype=np.complex128)
    if alm.size < N_lm(lmax):
        raise ValueError("The input `alm` size of {0} is too small for the stated `lmax` of {1}.  ".format(alm.size, lmax)
                         + "Perhaps you forgot to include the (zero) modes with ell<|s|.")
    return _salm2map(alm, s, lmax, Ntheta, Nphi)
    

def map2salm(f, s, lmax):
    """Convert values of spin-weighted function on a grid to mode weights

    Parameters
    ----------
    f : array_like
        Values of the spin-weighted function on grid points of the sphere.
    s : int
        Spin weight of the function.
    lmax : int
        The largest `ell` value present in the input array.


    Returns
    -------
    salm : 2-d array of complex
        Mode weights of the spin-weighted function.


    See also
    --------
    spinsfast.map2salm : Roughly the inverse of this function.


    Notes
    -----

    The input data represent the values on this grid of spherical coordinates:

        np.array([[[theta, phi]
                   for phi in np.linspace(0.0, 2*np.pi, num=2*lmax+1, endpoint=False)]
                  for theta in np.linspace(0.0, np.pi, num=2*lmax+1, endpoint=True)])

    The input is converted to a contiguous complex numpy array if necessary.

    The output `salm` data are given in increasing order of `ell` value, always starting with
    (ell, m) = (0, 0) even if `s` is nonzero, proceeding to (1, -1), (1, 0), (1, 1), etc.
    Explicitly, the ordering matches this:

        [[ell,m] for ell in range(lmax+1) for m in range(-ell, ell+1)]

    Note that `map2salm` and `salm2map` are not true inverses of each other for several reasons.
    First, modes with `ell < |s|` should always be zero; they are simply assumed to be zero on input
    to `salm2map`.  It is also possible to define a `map` function that violates this assumption --
    for example, having a nonzero average value over the sphere, if the function has nonzero spin
    `s`, this is impossible.  Also, it is possible to define a map of a function with so much
    angular dependence that it cannot be captured with the given `lmax` value.  For example, a
    discontinuous function will never be perfectly resolved.


    Example
    -------
    >>> s = -2
    >>> lmax = 8
    >>> theta_phi = np.array([[[theta, phi]
                               for phi in np.linspace(0.0, 2*np.pi, num=2*lmax+1, endpoint=False)]
                              for theta in np.linspace(0.0, np.pi, num=2*lmax+1, endpoint=True)])
    >>> f = np.array([[np.sqrt(3/(8*np.pi)) * np.sin(tp[0]) for tp in _] for _ in theta_phi])
    >>> salm = spinsfast.map2salm(f, s, lmax)

    """
    import numpy as np
    f = np.ascontiguousarray(f, dtype=np.complex128)
    return _map2salm(f, s, lmax)
