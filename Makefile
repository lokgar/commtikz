# Makefile for commtikz LaTeX/TikZ Library

LATEX    ?= pdflatex
LATEXFLAGS ?= -interaction=nonstopmode -halt-on-error
DOC      := commtikz-doc

.PHONY: all doc check clean distclean

all: doc

doc: $(DOC).pdf

check:
	LATEX="$(LATEX)" LATEXFLAGS="$(LATEXFLAGS)" python3 tests/check.py

$(DOC).pdf: $(DOC).tex commtikz.sty tikzlibrarycommtikz.code.tex \
            tikzlibrarycommtikz.base.code.tex \
            tikzlibrarycommtikz.optical.code.tex \
            tikzlibrarycommtikz.instruments.code.tex \
            tikzlibrarycommtikz.rf.code.tex \
            tikzlibrarycommtikz.paths.code.tex \
            tikzlibrarycommtikz.electrical.code.tex
	$(LATEX) $(LATEXFLAGS) $(DOC).tex
	$(LATEX) $(LATEXFLAGS) $(DOC).tex

clean:
	rm -f $(DOC).aux $(DOC).log $(DOC).out $(DOC).toc

distclean: clean
	rm -f $(DOC).pdf
