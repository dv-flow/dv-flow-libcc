.. DV Flow LibCC documentation master file, created by
   sphinx-quickstart.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
###############
DV Flow LibCC
###############

LibCC is a DV-Flow library that provides tasks for building C/C++ shared libraries and executables.
The library defines a set of tasks for compiling C/C++ sources and object files into shared libraries or executables.

.. contents::
    :depth: 2

Task: SharedLib
===============
Builds a shared library from C/C++ sources and object files.

Consumes
--------
* cSource
* cppSource
* objFile

Parameters
----------
* **cc** - [Optional, default: gcc] C compiler to use
* **cxx** - [Optional, default: g++] C++ compiler to use
* **libname** - [Optional] Basename of the shared library

Task: Exe
=========
Builds an executable from C/C++ sources and object files.

Consumes
--------
* cSource
* cppSource
* objFile

Parameters
----------
* **cc** - [Optional, default: gcc] C compiler to use
* **cxx** - [Optional, default: g++] C++ compiler to use
* **libname** - [Optional] Basename of the executable

.. note::
    This package is intended for use with DV-Flow and provides reusable build tasks for C/C++ projects.
