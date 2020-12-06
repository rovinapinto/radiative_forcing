import numpy as np
from netCDF4 import Dataset
import xarray as xr
import dask as ds

def compute_forcings_allsky(data_aerosols, data_control):
    ''' Calculate the effective radiative forcing at TOA due shortwave and longwave radiation flux
       Parameters:
       -----------
       data_aerosols: xarray.Dataset
                 aerosol data; should include 'rsdt', 'rsut' and 'rlut' fluxes; usually: dim=(time, lat, lon) 
       data_control: xarray.Dataset
                     control data; should include 'rsdt', 'rsut' and 'rlut' fluxes and has to be of the 
                     same dimension as data_aer

       Returns:
       --------
       sw_forcing_toa: xarray.DataArray
                       shortwave forcing at toa; same dimension as input data (usually (time, lat, lon))
       lw_forcing_toa: xarray.DataArray
                       longwave forcing at toa; same dimension as input data (usually (time, lat, lon))
    '''

    sw_balance_aer = data_aerosols["rsdt"] - data_aerosols["rsut"]
    sw_balance_control = data_control["rsdt"] - data_control["rsut"]
    sw_forcing_toa = -sw_balance_control + sw_balance_aer
    lw_balance_aer = data_aerosols["rsdt"] - data_aerosols["rsut"] - data_aerosols["rlut"]
    lw_balance_control = data_control["rsdt"] - data_control["rsut"] - data_control["rlut"]
    lw_forcing_toa = -lw_balance_control + lw_balance_aer

    return sw_forcing_toa, lw_forcing_toa
    
def compute_forcings_clearsky(data_aerosols, data_control):
    ''' Calculate the effective radiative forcing at TOA due shortwave and longwave radiation flux
       Parameters:
       -----------
       data_aerosols: xarray.Dataset
                 aerosol data; should include 'rsdt', 'rsut' and 'rlut' fluxes; usually: dim=(time, lat, lon) 
       data_control: xarray.Dataset
                     control data; should include 'rsdt', 'rsut' and 'rlut' fluxes and has to be of the 
                     same dimension as data_aer

       Returns:
       --------
       sw_forcing_toa: xarray.DataArray
                       shortwave forcing at toa; same dimension as input data (usually (time, lat, lon))
       lw_forcing_toa: xarray.DataArray
                       longwave forcing at toa; same dimension as input data (usually (time, lat, lon))
    '''

    sw_balance_aer = data_aerosols["rsdt"] - data_aerosols["rsutcs"]
    sw_balance_control = data_control["rsdt"] - data_control["rsutcs"]
    sw_forcing_toa = -sw_balance_control + sw_balance_aer
    lw_balance_aer = data_aerosols["rsdt"] - data_aerosols["rsutcs"] - data_aerosols["rlutcs"]
    lw_balance_control = data_control["rsdt"] - data_control["rsutcs"] - data_control["rlutcs"]
    lw_forcing_toa = -lw_balance_control + lw_balance_aer

    return sw_forcing_toa, lw_forcing_toa
    
def compute_cloudy_sky(data_aerosols, data_control):
    ''' Calculate the effective radiative forcing at TOA due shortwave and longwave radiation flux
       Parameters:
       -----------
       data_aerosols: xarray.Dataset
                 aerosol data; should include 'rsdt', 'rsut' and 'rlut' fluxes; usually: dim=(time, lat, lon) 
       data_control: xarray.Dataset
                     control data; should include 'rsdt', 'rsut' and 'rlut' fluxes and has to be of the 
                     same dimension as data_aer

       Returns:
       --------
       sw_forcing_toa: xarray.DataArray
                       shortwave forcing at toa; same dimension as input data (usually (time, lat, lon))
       lw_forcing_toa: xarray.DataArray
                       longwave forcing at toa; same dimension as input data (usually (time, lat, lon))
    '''

    forcing_allsky = compute_forcings_allsky(data_aerosols, data_control)
    forcing_clearsky = compute_forcings_clearsky(data_aerosols, data_control)

    a = forcing_allsky[0] - (1 - data_aerosols["clt"]
                             * 0.01) * forcing_clearsky[0]
    a1 = forcing_allsky[0] - (1 - data_control["clt"]
                              * 0.01) * forcing_clearsky[0]
    a2 = forcing_allsky[1] - (1 - data_aerosols["clt"]
                              * 0.01) * forcing_clearsky[1]
    a3 = forcing_allsky[1] - (1 - data_control["clt"]
                              * 0.01) * forcing_clearsky[1]

    deno1 = data_aerosols["clt"].values * 0.01
    deno2 = data_control["clt"].values * 0.01

    deno1[deno1 < 0.01] = 0  # xarray equivalent: deno1.where(deno1 < 0.01, 0)
    deno2[deno2 < 0.01] = 0  # xarray equivalent: deno2.where(deno2 < 0.01, 0)

    # haven't found an xarray equivalent of np.divide
    sw_cloudy_aer = np.divide(
        a.values, deno1, out=np.zeros_like(a.values), where=(deno1 != 0))
    sw_cloudy_control = np.divide(
        a1.values, deno2, out=np.zeros_like(a1.values), where=(deno2 != 0))
    lw_cloudy_aer = np.divide(
        a2.values, deno1, out=np.zeros_like(a2.values), where=(deno1 != 0))
    lw_cloudy_control = np.divide(
        a3.values, deno2, out=np.zeros_like(a3.values), where=(deno2 != 0))

    return sw_cloudy_control, sw_cloudy_aer, lw_cloudy_control, lw_cloudy_aer