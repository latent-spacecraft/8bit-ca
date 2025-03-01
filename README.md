# Conway's Game of Life in 8bits

This is a work in progress, the only script published right now runs a set of four cellular automata grids in parallel, as seen on [the website](https://latentspacecraft.com/code/deep-ca).

## Usage
Edit the setup parameters in this block:
```
# Setup parameters
width, height = 64, 64
noise_level = 0.000
max_values = [16, 32, 64, 128]
```

Width, height are the dimensions of the grid in cells. Square grids seem to work the best, but oblong/rectangular also work.
Noise level is noise injected at every step of the calculation, to make the grid more stochastic. You'll also be prompted to set this via the command line when running the script.
