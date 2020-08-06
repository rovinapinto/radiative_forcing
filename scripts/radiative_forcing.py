#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 14:01:41 2020

@author: rovina
"""
import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt 
import pandas as pd
import glob
import cartopy.crs as ccrs

# read netcdf files into the defined variables
class AerosolData:  # !!! usually classes in CamelCase so that one easily sees it is a class. Function is usually lower_case_with_underscores
    #TOA data for NorESM

    aer_rsdt = "/home/rovina/KlimaData/aero/CMIP6/RFMIP/piClim-spAer-aer/rsdt/rsdt_Amon_NorESM2-LM_piClim-spAer-aer_r1i1p1f1_gn_000101-003012.nc"
    aer_rsut = aer_rsdt.replace('rsdt','rsut')
    aer_rlut = aer_rsdt.replace('rsdt','rlut')
    
    def __init__(self):
        
        # data from rsut
        self.time = np.nan  # (time)
        self.latitude = np.nan  # (lat)
        self.longitude = np.nan  # (lon)
        self.rsut = np.nan  # (time, lat , lon)
        
        # !!! this overwrite the above defined variables. They should be named differently
        # data from rlut
        self.time = np.nan  # (time)
        self.latitude = np.nan  # (lat)
        self.longitude = np.nan  # (lon)
        self.rlut = np.nan  # (time, lat , lon)
        
        # data from rsdt
        self.time = np.nan  # (time)
        self.latitude = np.nan  # (lat)
        self.longitude = np.nan  # (lon)
        self.rsdt = np.nan  # (time, lat , lon)
        
    def read(self):
        
        rsdt_file = aer_rsdt
        rsut_file = aer_rsut
        rlut_file = aer_rlut
        
        with Dataset(rsut_file) as nc:
            
            self.time = nc.variables['time'][:] 
            self.latitude = nc.variables['lat'][:]
            self.longitude = nc.variables['lon'][:]
            self.rsut = nc.variables['rsut'][:]

        # here it is then enough to read just the rlut, rsdt
        # but to check the variables are in fact the same

        with Dataset(rlut_file) as nc:

        	# !!! check if lat lon time is the same
            assert nc.variables['time'][:] == self.time  # !!! try if this works - maybe it can not compare floats. Then maybe just compare the shapes
            assert nc.variables['lat'][:] == self.latitude 
            assert nc.variables['lon'][:] == self.longitude

            #self.time = nc.variables['time'][:] 
            #self.latitude = nc.variables['lat'][:]
            #self.longitude = nc.variables['lon'][:]
            self.rlut = nc.variables['rlut'][:]
            
        with Dataset(rsdt_file) as nc:
            
            #self.time = nc.variables['time'][:] 
            #self.latitude = nc.variables['lat'][:]
            #self.longitude = nc.variables['lon'][:]
            self.rsdt = nc.variables['rsdt'][:]
            
class control_Data:
    #TOA data for NorESM

    aer_rsdt = "/home/rovina/KlimaData/aero/CMIP6/RFMIP/piClim-spAer-aer/rsdt/rsdt_Amon_NorESM2-LM_piClim-spAer-aer_r1i1p1f1_gn_000101-003012.nc"
    
    control_rsdt = aer_rsdt.replace('piClim-spAer-aer','piClim-control')
    control_rsut = control_rsdt.replace('rsdt','rsut')
    control_rlut = control_rsdt.replace('rsdt','rlut')
    
    def __init__(self):
        
        # data from rsut
        self.time = np.nan  # (time)
        self.latitude = np.nan  # (lat)
        self.longitude = np.nan  # (lon)
        self.rsut = np.nan  # (time, lat , lon)
        
        # data from rlut
        self.time = np.nan  # (time)
        self.latitude = np.nan  # (lat)
        self.longitude = np.nan  # (lon)
        self.rlut = np.nan  # (time, lat , lon)
        
        # data from rsdt
        self.time = np.nan  # (time)
        self.latitude = np.nan  # (lat)
        self.longitude = np.nan  # (lon)
        self.rsdt = np.nan  # (time, lat , lon)
        
    def read(self):
        
        rsdt_file = control_rsdt
        rsut_file = control_rsut
        rlut_file = control_rlut
        
        with Dataset(rsut_file) as nc:
            
            self.time = nc.variables['time'][:] 
            self.latitude = nc.variables['lat'][:]
            self.longitude = nc.variables['lon'][:]
            self.rsut = nc.variables['rsut'][:]
                            
        with Dataset(rlut_file) as nc:
            
            self.time = nc.variables['time'][:] 
            self.latitude = nc.variables['lat'][:]
            self.longitude = nc.variables['lon'][:]
            self.rlut = nc.variables['rlut'][:]
            
        with Dataset(rsdt_file) as nc:
            
            self.time = nc.variables['time'][:] 
            self.latitude = nc.variables['lat'][:]
            self.longitude = nc.variables['lon'][:]
            self.rsdt = nc.variables['rsdt'][:]
