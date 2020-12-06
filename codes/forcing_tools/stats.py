import numpy as np
from netCDF4 import Dataset
import xarray as xr
import dask as ds
from scipy import stats

def global_mean(data, data_main=None):
    ''' Calculate the global mean value of given data with (lat,lon) coordinates
        Parameters:
        -----------

        data: 3D or 2D xarray.DataArray/ numpy.ndarray
              can be forcing, SST, temperature, preciptitation, etc. over a sphere. 
              For 2D ndarray, axis has to be changed to 0
        data_main:  3D or 2D xarray.DataArray
               required to convert latitudes

        Returns:
        --------
        area_mean: 1D xarray.DataArray/ numpy.ndarray
                   area mean. Use only 2 decimal points
        global_mean: float64
                     spatial and/or temporal mean.  Use only 2 decimal points
    '''
    if data_main is not None:
        weight = np.cos(np.deg2rad(data_main.lat))
        area_mean = np.average(data, axis=1, weights=weight)
        global_mean = area_mean.mean()
    else:
        weight = np.cos(np.deg2rad(data.lat))
        area_mean = data.weighted(weight).mean(dim=("lon", "lat"))
        global_mean = area_mean.mean().values

    return (area_mean, global_mean)

def time_series(data, variable, grid_dist=1.0, plot=True):
    ''' Compute the time-series for any given variable of interest with (lat,lon) coordinates
    https://github.com/pangeo-data/pangeo-tutorial/blob/agu2019/notebooks/xarray.ipynb#More-Complicated-Example:-Weighted-Mean
    Parameters:
    -----------
    data:      xarray.Dataset
               usually: dim=(time, lat, lon) and contains several variables of interest such as temperature etc.

    variable: 3D or 2D xarray.DataArray
               can be forcing, SST, temperature, preciptitation, etc. over a sphere

    grid_dist: float64
               distance between the grid points. Default = 1.0

    Returns:
    --------
    weighted_mean: 1D xarray.DataArray
                   returns the weighted time series data of the variable of interest 
                   by calculating the total spherical area and points on the map where the variable is not zero.
                   where ϕ is latitude, dϕ is the spacing of the points in latitude, 
                   dλ is the spacing of the points in longitude, and R is Earth's radius. 

    plot:      boolean
               plots time series data if True. Default = True
    '''

    R = 6.37e6
    dϕ = np.deg2rad(grid_dist)
    dλ = np.deg2rad(grid_dist)
    dA = R**2 * dϕ * dλ * np.cos(np.deg2rad(data.lat))

    pixel_area = dA.where(variable[0].notnull())
    total_area = pixel_area.sum(dim=('lon', 'lat'))
    weighted_mean = (
        variable * pixel_area).sum(dim=('lon', 'lat')) / total_area

    if plot is True:
        weighted_mean.plot()

    return weighted_mean

def t_test(data, n, pop_mean):
    '''Compute the one sample t-test an xarray DataArray
    Parameters:
    -----------
    data:       xarray.Dataset
                sample whose t-test is to be computed. Can be 2D or 3D. Alternate hypothesis, H1
    n:          integer
                sample size (example: if averaged yearly then climatalogy has 30 years)
    pop_mean:   integer or 1D array
                the null hypothesis H0
                
    Returns:
    --------
    t-statistics: numpy array ( 1D or 2D depending on input)
    p_value:      numpy array ( 1D or 2D depending on input)
                  value at each grid cell for a two tailed distribution
    '''
    
    sample_mean = data.mean(dim='time') #at each grid cell and not field
    sample_var = data.var(dim='time', ddof=1)
    t_statistics = (sample_mean - pop_mean) / (np.sqrt(sample_var/n))
    p_value = stats.t.sf(np.abs(t_statistics), n-1)*2  # two-sided pvalue = Prob(abs(t)>tt)
    return t_statistics, p_value

def t_test_nd(data, n, pop_mean):
    '''Compute the one sample t-test for an nd.array
    Parameters:
    -----------
    data:       numpy array
                sample whose t-test is to be computed. Can be 2D or 3D. Alternate hypothesis, H1
    n:          integer
                sample size (example: if averaged yearly then climatalogy has 30 years)
    pop_mean:   integer or 1D array
                the null hypothesis H0
                
    Returns:
    --------
    t-statistics: numpy array ( 1D or 2D depending on input)
    p_value:      numpy array ( 1D or 2D depending on input)
                  value at each grid cell for a two tailed distribution
    '''
    
    sample_mean = np.mean(data, axis=0)
    sample_var = np.var(data, axis=0, ddof=1)
    t_statistics = (sample_mean - pop_mean) / (np.sqrt(sample_var/n))
    p_value = stats.t.sf(np.abs(t_statistics), n-1) * 2 
    return t_statistics, p_value