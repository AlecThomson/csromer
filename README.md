# CS-ROMER
*Compressed Sensing ROtation MEasure Reconstruction*

This code will run in a Python >= 3.9.7 environment with all the packages installed (see `requirements.txt` file).
The paper of this software is under submission but if you use it you can cite it as:

```
@misc{https://doi.org/10.48550/arxiv.2205.01413,
  doi = {10.48550/ARXIV.2205.01413},
  
  url = {https://arxiv.org/abs/2205.01413},
  
  author = {Cárcamo, Miguel and Scaife, Anna M. M. and Alexander, Emma L. and Leahy, J. Patrick},
  
  keywords = {Instrumentation and Methods for Astrophysics (astro-ph.IM), Astrophysics of Galaxies (astro-ph.GA), FOS: Physical sciences, FOS: Physical sciences},
  
  title = {CS-ROMER: A novel compressed sensing framework for Faraday depth reconstruction},
  
  publisher = {arXiv},
  
  year = {2022},
  
  copyright = {arXiv.org perpetual, non-exclusive license}
}
```
## Installation
The software can be installed as a python package locally or using Pypi
### Locally
`pip install -e .`
### From Pypi
`pip install csromer`
## Simulate Faraday sources directly in frequency space
CS-ROMER is able to simulate Faraday depth spectra directly in wavelength-squared space. The classes `FaradayThinSource` and `FaradayThickSource` inherit directly from `Dataset`, and therefore you can directly use them as an input to your reconstruction.
### Thin sources
```python
import numpy
from csromer.simulation import FaradayThinSource
# Let's create an evenly spaced frequency vector from 1.008 to 2.031 GHz (JVLA setup) 
nu = np.linspace(start=1.008e9, stop=2.031e9, num=1000)
# Let's say that the peak polarized intensity will be 0.0035 mJy/beam with a spectral index = 1.0
peak_thinsource = 0.0035
# The Faraday source will be positioned at phi_0 = -200 rad/m^2
thinsource = FaradayThinSource(nu=nu, s_nu=peak_thinsource, phi_gal=-200, spectral_idx=1.0)
```
### Thick sources
```python
import numpy
from csromer.simulation import FaradayThickSource
# Let's create an evenly spaced frequency vector from 1.008 to 2.031 GHz (JVLA setup) 
nu = np.linspace(start=1.008e9, stop=2.031e9, num=1000)
# Let's say that the peak polarized intensity will be 0.0035 mJy/beam with a spectral index = 1.0
peak_thicksource = 0.0035
# The Faraday source will be positioned at phi_0 = 200 rad/m^2 and with have a width of 140 rad/m^2
thicksource = FaradayThickSource(nu=nu, s_nu=peak_thicksource, phi_fg=140, phi_center=200, spectral_idx=1.0)
```

### Simulate
Once you have set your source parameters, you can call the `simulate()` function as
```python
thinsource.simulate()
thicksource.simulate()
```
This call will simulate the linealy polarized emission and it will assign the data to the `data` attribute.

### Mixed sources
A thin+thick or mixed source is simply a superposition/sum of a thin source and thick source. Therefore we have overriden the `+` operator in order to sum these two objects.
```python
mixedsource = thinsource + thicksource
```
The result will be a `FaradaySource` object.

### Remove frequency channels randomly as you were doing RFI flagging
The framework also allows you to randomly remove data with the function `remove_channels` to simulate RFI flagging
```python
# Let's say that we want to randomly remove 20% of the data
mixedsource.remove_channels(0.2)
```
### Adding noise to your simulations
If we want to add random Gaussian noise to our simulation we can simply call the function `apply_noise`
```python
# Let's add Gaussian random noise with mean 0 and standard deviation equal 
# to 20% the peak of the signal.
sigma = 0.2*mixedsource.s_nu
mixedsource.apply_noise(sigma)
```



## Reconstruct 1D Faraday sources

### Reconstruct a simulation

### Reconstruct real data

## Reconstruct a cube

## Contact
Please if you have any problem, issue or you catch a bug using this software please use the [issues tab](https://github.com/miguelcarcamov/csromer/issues) if you have a common question or you look for any help please use the [discussions tab](https://github.com/miguelcarcamov/csromer/discussions).