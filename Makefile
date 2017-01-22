# Makefile for AniCal
# 
# Author        : Yongwen Zhuang(zYeoman)
# Created       : 2017-01-20
# Last Modified : 2017-01-20

PYLINT = pylint
PYLINTFLAGS = -rn

PYTHONFILES := $(wildcard *.py ./Parser/*.py)

init:
	pip install -r requirements.txt

test:
	cd tests && python test.py

install:
	python setup.py install

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

%.pylint:
	-$(PYLINT) $(PYLINTFLAGS) $*.py

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf thu_utils.egg-info/
	find . \( -name \*.pyc -o -name \*.pyo -o -name __pycache__ \) -delete
