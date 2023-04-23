# Demos for PSyKI

This repository is meant to present demos for [PSyKI](https://github.com/psykei/psyki-python), a python package for symbolic knowledge injection (SKI).
In our intentions, a user should be able to get started with PSyKI by cloning this repository and running the notebooks in the `notebooks` directory.

There exists a doker image for the demos!
```
docker pull pikalab/demo-psyki-python:latest
```
For M1 users
```
docker pull pikalab/demo-psyki-python:latest-apple-m1
```

To execute the container run
```
docker run -it --rm -p 8888:8888 pikalab/demo-psyki-python
```

## Before starting
All notebooks are self-contained and should be runnable in a fresh environment.
Make sure to have satisfied the requirements (see `requirements.txt`):

(for developers)
- build 0.10.0
- setuptools 67.6.0
- treon 0.1.4

(for users and developers)
- jupyter 1.0.0
- tensorflow 2.7.0
- psyki 0.3.10
- pandas 1.5.3
- scikit-learn 1.2.2

## Demos
- [KBANN](https://www.sciencedirect.com/science/article/pii/0004370294901058), the algorithm is presented in the context of a biological task consisting in classifying DNA sequences.
It makes use of propositional logic rules, see `knowledge\splice-junction.pl`.
The demo is available at `notebooks\kbann.ipynb`;
- [KINS](https://ceur-ws.org/Vol-3204/paper_25.pdf), a dataset concerning the yearly income of people living in the U.S. is used to present the algorithm.
KBANN accepts rules in stratified (a.k.a. no recursion) Datalog or subsets  of s. Datalog (e.g., propositional logic), see see `knowledge\census-income.pl`.
The demo is available at `notebooks\kins.ipynb`.
