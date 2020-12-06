import numpy as np
from netCDF4 import Dataset
import xarray as xr
import dask as ds
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import from_levels_and_colors
from pylab import *
import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point

def plot_data(dataset, data_var, dtype="ndarray", ticks=None, colors=None, levels=None, title=None, figname=None):
    '''Plot time averaged data on a Mollweide map using xarray DataArray or numpy array
    Parameters:
    ----------
    dataset:    xarray Dataset
                must contain dimensions of time, lat and lon
    data_var:   xarray DataArray or a numpy ndArray
                has to have three dimensions including time
    dtype:      string
                can be either an ndarray or an xarray. Default: ndarray
    ticks:      list
                integer or float list of ticks for colorbar. Default: None
    colors:     list
                list of colors as hexcodes in string. 
                Default is RdBu_r is colors if set to None
                Use default None to ascertain the levels and colors
    levels:     list
                list of levels for the map. Has to be same lenght as colors. For extend True, 
                change set_over and set_under colors to required colormap. 
    title:      string
                Default is None
    figname:    string
                use to save figure with transparent background and tight borders. Deafult is None.
    
    Returns:
    --------
    cs:         plots the map
    '''
                

    if dtype == "ndarray":
        vmax = np.max(np.mean(data_var, axis=0))
        vmin = np.min(np.mean(data_var, axis=0))
        var = data_var
    else:
        vmax = np.max(np.mean(data_var, axis=0))
        # (data_var.mean("year").values)
        vmin = np.min(np.mean(data_var, axis=0))
        var = data_var.values

    v_ext = np.max([np.abs(vmin), np.abs(vmax)])
    norm = mcolors.TwoSlopeNorm(vmin=-v_ext, vmax=v_ext, vcenter=0)
    cmap = cm.get_cmap('RdBu_r', 20)

    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Mollweide())
    ax.set_global()
    ax.coastlines()
    val, ll = add_cyclic_point(var, coord=dataset.lon.values)

    if colors is not None:
        cs = ax.contourf(ll, dataset.lat.values, np.mean(val, axis=0), norm=norm,
                         transform=ccrs.PlateCarree(), colors=colors, levels=levels, extend='both')
        plt.colorbar(cs, shrink=0.8, fraction=0.046, pad=0.04,
                     label=r"$\mathrm{Wm}^{-2}$", orientation='horizontal', ticks=ticks)
        cs.cmap.set_under("#053061")
        cs.cmap.set_over("#67001f")

    else:
        cs = ax.contourf(ll, dataset.lat.values, np.mean(
            val, axis=0), norm=norm, transform=ccrs.PlateCarree(), cmap='RdBu_r')
        plt.colorbar(cs, shrink=0.8, fraction=0.046, pad=0.04, extendrect=True,
                     label=r"$\mathrm{Wm}^{-2}$", orientation='horizontal')

    if title is not None:
        plt.title(title, loc='center', fontsize=12)

    if figname is not None:
        plt.savefig(figname + ".pdf", bbox_inches='tight', transparent=True)

    return cs

def plot_annual_data(dataset, data_var, dtype="ndarray", ax=None, ticks=None, colors=None, levels=None,title=None,figname=None):
    '''Plot data on a Mollweide map using xarray DataArray or numpy array
    Parameters:
    ----------
    dataset:    xarray Dataset
                must contain dimensions of lat and lon
    data_var:   xarray DataArray or a numpy ndArray
                has to have two dimensions
    dtype:      string
                can be either an ndarray or an xarray. Default: ndarray
    ticks:      list
                integer or float list of ticks for colorbar. Default: None
    colors:     list
                list of colors as hexcodes in string. 
                Default is RdBu_r is colors if set to None
                Use default None to ascertain the levels and colors
    levels:     list
                list of levels for the map. Has to be same lenght as colors. For extend True, 
                change set_over and set_under colors to required colormap. 
    title:      string
                Default is None
    figname:    string
                use to save figure with transparent background and tight borders. Deafult is None.
    
    Returns:
    --------
    cs:         plots the map
    '''
    
    if dtype == "ndarray":
        vmax = np.max(data_var)
        vmin = np.min(data_var)
        var = data_var
    else:
        vmax = np.max(data_var.values)
        vmin = np.min(data_var.values)
        var = data_var.values

    v_ext = np.max([np.abs(vmin), np.abs(vmax)])
    norm = mcolors.TwoSlopeNorm(vmin=-v_ext, vmax=v_ext, vcenter=0)
    cmap = cm.get_cmap('RdBu_r', 20)

    ax.set_global()
    ax.coastlines()
    val, ll = add_cyclic_point(var, coord=data_var.lon.values)

    if colors is not None:
        cs = ax.contourf(ll, data_var.lat.values, val, norm=norm, transform=ccrs.PlateCarree(
        ), colors=colors, levels=levels, extend='both')
        cs.cmap.set_under("#053061")
        cs.cmap.set_over("#67001f")
    else:
        cs = ax.contourf(ll, data_var.lat.values, val, norm=norm,
                         transform=ccrs.PlateCarree(), cmap='RdBu_r')

    if title is not None:
        plt.title(title, loc='center', fontsize=12)

    if figname is not None:
        plt.savefig(figname + ".pdf", bbox_inches='tight', transparent=True)

    return cs