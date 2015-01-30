# $Id: Makefile 209 2007-08-19 16:41:44Z mccosar $

TARGET = pcsets_tutorial

.PHONY: default all pdf ps dvi clean

default: all

all: pdf ps

pdf: ${TARGET}.tex
	pdflatex $<
	bibtex ${TARGET}
	makeindex ${TARGET}.idx
	pdflatex $<
	pdflatex $<
	pdflatex $<

ps: ${TARGET}.dvi
	dvips $< -t letter -o ${TARGET}.ps

dvi: ${TARGET}.dvi

${TARGET}.dvi: ${TARGET}.tex
	latex $<
	bibtex ${TARGET}
	makeindex ${TARGET}.idx
	latex $<
	latex $<
	latex $< # Yep, required.

clean:
	rm -f ${TARGET}.log
	rm -f ${TARGET}.aux
	rm -f ${TARGET}.idx
	rm -f ${TARGET}.ilg
	rm -f ${TARGET}.ind
	rm -f ${TARGET}.toc
	rm -f ${TARGET}.bbl
	rm -f ${TARGET}.blg
