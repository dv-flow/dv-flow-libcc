# Minimal Makefile for Sphinx documentation
# Adapted from sphinx-quickstart

DOC_DIR:=$(dir $(abspath $(lastword $(MAKEFILE_LIST))))
PROJ_DIR:=$(abspath $(DOC_DIR)/..)

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= $(PROJ_DIR)/packages/python/bin/sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

.PHONY: help Makefile

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
