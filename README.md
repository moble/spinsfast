# spinsfast
Fast and exact spin-s spherical-harmonic transforms

This code is a lightly modified version of the code hosted
[here](http://astrophysics.physics.fsu.edu/~huffenbe/research/spinsfast/index.html)
by Huffenberger, based on work by
[Huffenberger and Wandelt](http://stacks.iop.org/0067-0049/189/255).  My
modifications are basically to make it easier to install as a python module.  I
based my work on their "Revision 104, 13 Apr 2012", which is current as of this
writing.  Whenever I notice updates on their end, I will update this code, so
feel free to open an [issue](https://github.com/moble/spinsfast/issues) to
notify me.





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
