#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 21:18:22 2020

@author: rovina
"""

import numpy as np
from netCDF4 import Dataset

class RadiativeFluxData: 
    """
    TOA data for NorESM
    """

    def __init__(self):
        """
        Initialize variables
        rsut: TOA Outgoing Shortwave Radiation (Wm^-2)
        rsdt: TOA Incident Shortwave Radiation (Wm^-2)
        rlut: TOA Outgoing Longwave Radiation (Wm^-2)
        """
        
        self.time = np.nan  # (time)
        self.lat = np.nan  # (lat)
        self.lon = np.nan  # (lon)
        self.rsdt_aer = np.nan  # (time, lat , lon)
        self.rsut_aer = np.nan  # (time, lat , lon)
        self.rlut_aer = np.nan  # (time, lat , lon)
        self.rsdt_c = np.nan  # (time, lat , lon)
        self.rsut_c = np.nan  # (time, lat , lon)
        self.rlut_c = np.nan  # (time, lat , lon)
        
    def read(self, path='/home/rovina/KlimaData/aero/CMIP6/RFMIP/', read_metadata=True):
        """
        Read data
        Needs 3 files corresponding to control sim and 3 files for sim incl anthropogenic aerosols
        """

        # incl anthropogenic aerosols
        file_rsdt_aer = path+"piClim-spAer-aer/rsdt/rsdt_Amon_NorESM2-LM_piClim-spAer-aer_r1i1p1f1_gn_000101-003012.nc"
        file_rsut_aer = path+"piClim-spAer-aer/rsut/rsut_Amon_NorESM2-LM_piClim-spAer-aer_r1i1p1f1_gn_000101-003012.nc"
        file_rlut_aer = path+"piClim-spAer-aer/rlut/rlut_Amon_NorESM2-LM_piClim-spAer-aer_r1i1p1f1_gn_000101-003012.nc"

        # control- without anthro aerosols
        file_rsdt_c = path+"piClim-control/rsdt/rsdt_Amon_NorESM2-LM_piClim-control_r1i1p1f1_gn_000101-003012.nc"
        file_rsut_c = path+"piClim-control/rsut/rsut_Amon_NorESM2-LM_piClim-control_r1i1p1f1_gn_000101-003012.nc"
        file_rlut_c = path+"piClim-control/rlut/rlut_Amon_NorESM2-LM_piClim-control_r1i1p1f1_gn_000101-003012.nc"
        
        # read experiment
        with Dataset(file_rsdt_aer) as nc:
            
            self.rsdt_aer = nc.variables['rsdt'][:]

            # read only for first variable and assume the others are the same. To compare, see above the assert. But not sure if that would work
            self.time = nc.variables['time'][:] 
            self.lat = nc.variables['lat'][:]
            self.lon = nc.variables['lon'][:]

        with Dataset(file_rsut_aer) as nc:
            
            self.rsut_aer = nc.variables['rsut'][:]

        with Dataset(file_rlut_aer) as nc:
            
            self.rlut_aer = nc.variables['rlut'][:]

        # read control
        with Dataset(file_rsdt_c) as nc:
            
            self.rsdt_c = nc.variables['rsdt'][:]

        with Dataset(file_rsut_c) as nc:
            
            self.rsut_c = nc.variables['rsut'][:]

        with Dataset(file_rlut_c) as nc:
            
            self.rlut_c = nc.variables['rlut'][:]