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
    TOA data for MPI-ESM1.2 with three realizations
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
        
    def read(self, path='/home/rpinto/KlimaData/CMIP6/RFMIP/', read_metadata=True):
        """
        Read data
        Needs 3 files corresponding to control sim and 3 files for sim incl anthropogenic aerosols
        """
        
        # incl anthropogenic aerosols
        file_rsdt_aer1 = path+"piClim-spAer-aer/rsdt/rsdt_Amon_MPI-ESM1-2-LR_piClim-spAer-aer_r1i1p1f1_gn_184901-187912.nc"
        file_rsut_aer1 = path+"piClim-spAer-aer/rsut/rsut_Amon_MPI-ESM1-2-LR_piClim-spAer-aer_r1i1p1f1_gn_184901-187912.nc"
        file_rlut_aer1 = path+"piClim-spAer-aer/rlut/rlut_Amon_MPI-ESM1-2-LR_piClim-spAer-aer_r1i1p1f1_gn_184901-187912.nc"

        # control- without anthro aerosols
        file_rsdt_c1 = path+"piClim-control/rsdt/rsdt_Amon_MPI-ESM1-2-LR_piClim-control_r1i1p1f1_gn_184901-187912.nc"
        file_rsut_c1 = path+"piClim-control/rsut/rsut_Amon_MPI-ESM1-2-LR_piClim-control_r1i1p1f1_gn_184901-187912.nc"
        file_rlut_c1 = path+"piClim-control/rlut/rlut_Amon_MPI-ESM1-2-LR_piClim-control_r1i1p1f1_gn_184901-187912.nc"
        
        file_rsdt_aer2 = path+"piClim-spAer-aer/rsdt/rsdt_Amon_MPI-ESM1-2-LR_piClim-spAer-aer_r2i1p1f1_gn_184901-187912.nc"
        file_rsut_aer2 = path+"piClim-spAer-aer/rsut/rsut_Amon_MPI-ESM1-2-LR_piClim-spAer-aer_r2i1p1f1_gn_184901-187912.nc"
        file_rlut_aer2 = path+"piClim-spAer-aer/rlut/rlut_Amon_MPI-ESM1-2-LR_piClim-spAer-aer_r2i1p1f1_gn_184901-187912.nc"

        # control- without anthro aerosols
        file_rsdt_c2 = path+"piClim-control/rsdt/rsdt_Amon_MPI-ESM1-2-LR_piClim-control_r2i1p1f1_gn_184901-187912.nc"
        file_rsut_c2 = path+"piClim-control/rsut/rsut_Amon_MPI-ESM1-2-LR_piClim-control_r2i1p1f1_gn_184901-187912.nc"
        file_rlut_c2 = path+"piClim-control/rlut/rlut_Amon_MPI-ESM1-2-LR_piClim-control_r2i1p1f1_gn_184901-187912.nc"
        
        file_rsdt_aer3 = path+"piClim-spAer-aer/rsdt/rsdt_Amon_MPI-ESM1-2-LR_piClim-spAer-aer_r3i1p1f1_gn_184901-187912.nc"
        file_rsut_aer3 = path+"piClim-spAer-aer/rsut/rsut_Amon_MPI-ESM1-2-LR_piClim-spAer-aer_r3i1p1f1_gn_184901-187912.nc"
        file_rlut_aer3 = path+"piClim-spAer-aer/rlut/rlut_Amon_MPI-ESM1-2-LR_piClim-spAer-aer_r3i1p1f1_gn_184901-187912.nc"

        # control- without anthro aerosols
        file_rsdt_c3 = path+"piClim-control/rsdt/rsdt_Amon_MPI-ESM1-2-LR_piClim-control_r3i1p1f1_gn_184901-187912.nc"
        file_rsut_c3 = path+"piClim-control/rsut/rsut_Amon_MPI-ESM1-2-LR_piClim-control_r3i1p1f1_gn_184901-187912.nc"
        file_rlut_c3 = path+"piClim-control/rlut/rlut_Amon_MPI-ESM1-2-LR_piClim-control_r3i1p1f1_gn_184901-187912.nc"
        
        
        # read experiment
        with Dataset(file_rsdt_aer1) as nc:
            
            self.rsdt_aer1 = nc.variables['rsdt'][:]

            # read only for first variable and assume the others are the same. To compare, see above the assert. But not sure if that would work
            self.time = nc.variables['time'][:] 
            self.lat = nc.variables['lat'][:]
            self.lon = nc.variables['lon'][:]

        with Dataset(file_rsut_aer1) as nc:
            
            self.rsut_aer1 = nc.variables['rsut'][:]

        with Dataset(file_rlut_aer1) as nc:
            
            self.rlut_aer1 = nc.variables['rlut'][:]

        # read control
        with Dataset(file_rsdt_c1) as nc:
            
            self.rsdt_c1 = nc.variables['rsdt'][:]

        with Dataset(file_rsut_c1) as nc:
            
            self.rsut_c1 = nc.variables['rsut'][:]

        with Dataset(file_rlut_c1) as nc:
            
            self.rlut_c1 = nc.variables['rlut'][:]
            
        # realization 2    
            
        with Dataset(file_rsdt_aer2) as nc:
            
            self.rsdt_aer2 = nc.variables['rsdt'][:]

        with Dataset(file_rsut_aer2) as nc:
            
            self.rsut_aer2 = nc.variables['rsut'][:]

        with Dataset(file_rlut_aer2) as nc:
            
            self.rlut_aer2 = nc.variables['rlut'][:]

        # read control
        with Dataset(file_rsdt_c2) as nc:
            
            self.rsdt_c2 = nc.variables['rsdt'][:]

        with Dataset(file_rsut_c2) as nc:
            
            self.rsut_c2 = nc.variables['rsut'][:]

        with Dataset(file_rlut_c2) as nc:
            
            self.rlut_c2 = nc.variables['rlut'][:]
            
            # realization 3  
            
        with Dataset(file_rsdt_aer3) as nc:
            
            self.rsdt_aer3 = nc.variables['rsdt'][:]

        with Dataset(file_rsut_aer3) as nc:
            
            self.rsut_aer3 = nc.variables['rsut'][:]

        with Dataset(file_rlut_aer3) as nc:
            
            self.rlut_aer3 = nc.variables['rlut'][:]

        # read control
        with Dataset(file_rsdt_c3) as nc:
            
            self.rsdt_c3 = nc.variables['rsdt'][:]

        with Dataset(file_rsut_c3) as nc:
            
            self.rsut_c3 = nc.variables['rsut'][:]

        with Dataset(file_rlut_c3) as nc:
            
            self.rlut_c3 = nc.variables['rlut'][:]
            
            self.rsdt_aer = (self.rsdt_aer1 + self.rsdt_aer2 + self.rsdt_aer3)/3
            self.rsut_aer = (self.rsut_aer1 + self.rsut_aer2 + self.rsut_aer3)/3
            self.rlut_aer = (self.rlut_aer1 + self.rlut_aer2 + self.rlut_aer3)/3
            
            self.rsdt_c = (self.rsdt_c1 + self.rsdt_c2 + self.rsdt_c3)/3
            self.rsut_c = (self.rsut_c1 + self.rsut_c2 + self.rsut_c3)/3
            self.rlut_c = (self.rlut_c1 + self.rlut_c2 + self.rlut_c3)/3
