# Distance to shore ¨

The distance to shore can be found by running the file distance_to_coast.py in a conda environment as described in the prerequisites. At this point, it is implemented by using the Basemap library only. For future developement it might be handy to use the seacharts library. Some testing is done and thus also put in this folder. 

## Prerequisites

### Using Anaconda

The simplest way to acquire the necessary dependencies is to install an edition of the [Anaconda](
https://www.anaconda.com/products/individual-d) package manager, and then
create a new _conda environment_ with **Python 3.9** using e.g. the graphical
user interface of [PyCharm Professional](
https://www.jetbrains.com/lp/pycharm-anaconda/) as detailed [here](
https://www.jetbrains.com/help/pycharm/conda-support-creating-conda-virtual-environment.html
).

The required data processing libraries for spatial calculations and
visualization may subsequently be installed simply by running the following
command in the terminal of your chosen environment:

```
conda install -c conda-forge fiona cartopy matplotlib
conda install basemap
```

## Contributors

- Seacharts package found at https://github.com/simbli/seacharts
- Guro Drange Veglo ([guroveglo@gmail.com](mailto:guroveglo@gmail.com))
