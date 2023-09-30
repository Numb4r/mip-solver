[![GitHub license](https://img.shields.io/github/license/andremaravilha/mip-solver-prediction)](https://github.com/andremaravilha/mip-solver-prediction/blob/main/LICENSE) 
![GitHub last commit](https://img.shields.io/github/last-commit/andremaravilha/mip-solver-prediction) 
![Lines of code](https://img.shields.io/tokei/lines/github/andremaravilha/mip-solver-prediction) 

# Prediction of computational runtime for solving MIP problems

> André L. Maravilha<sup>1, 2</sup>  
> <sup>1</sup> *Dept. of Informatics, Management and Design - Centro Fed. de Edu. Tecnológica de Minas Gerais ([url](https://www.cefetmg.br/))*  
> <sup>2</sup> *Operations Research and Complex Systems Lab. - Universidade Federal de Minas Gerais ([url](https://orcslab.github.io/))*


## 1. Proposed strategy

Repository with source-code and computational experiments for predicting computational runtime for solving MIP problems.


## 2. How to build the project

#### 2.1. Important comments before building the project

To compile this project, you need CMake (version 3.13 or later), Gurobi (version 9.1), IBM CPLEX (version 20.10), 
FICO Xpress (version 8.11), and a compatible compiler installed on your computer. The code has not been tested on versions 
earlier than the ones specified.

#### 2.2. Building the project

Inside the root directory of the project, run the following commands:
```
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release -DGUROBI_DIR=<path to Gurobi> -DCPLEX_DIR=<path to CPLEX> -DXPRESS_DIR=<path to FICO Xpress> ..
make
```
for example:
```
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release -DGUROBI_DIR=/opt/gurobi911/linux64 -DCPLEX_DIR=/opt/ibm/ilog -DXPRESS_DIR=/opt/xpressmp ..
make
```




