@ECHO OFF

REM Command file for Sphinx documentation

set SPHINXBUILD=sphinx-build
set SOURCEDIR=.
set BUILDDIR=_build

if "%SPHINXBUILD%" == "" (
    set SPHINXBUILD=sphinx-build
)
if "%SOURCEDIR%" == "" (
    set SOURCEDIR=.
)
if "%BUILDDIR%" == "" (
    set BUILDDIR=_build
)

%SPHINXBUILD% %SPHINXOPTS% -M %1 %SOURCEDIR% %BUILDDIR%
