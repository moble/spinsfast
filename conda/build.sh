# This script should be general enough to be used directly (from the top-level
# directory), but is primarily intended for use by conda-build.

# Conda used to set the `INCLUDE_PATH` variable, but that has changed
# <https://github.com/conda/conda-build/issues/509>, so the following line no
# longer works:
#
#   export C_INCLUDE_PATH=$INCLUDE_PATH
#
# However, according to @groutr on github, we simply need to use
# `$PREFIX/include` in its place.  To keep this script working for at least
# some other purposes, we'll just test for the presence of `$PREFIX`, and
# otherwise fall back to the original version:

if [ -z ${PREFIX+x} ]; then
    export C_INCLUDE_PATH=$INCLUDE_PATH
else
    export C_INCLUDE_PATH=$PREFIX/include
fi

python setup.py install
