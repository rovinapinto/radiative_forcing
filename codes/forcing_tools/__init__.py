# -*- coding: utf-8 -*-
# 
#  This file is part of sz_tools.
# 
#  sz_tools is free software; you can redistribute it and/or modify
#  it under the terms of the MIT License.
# 
#  sz_tools is distributed in the hope that it will be useful,but 
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See 
#  the provided copy of the MIT License for more details.

"""forcing_tools is a python implementation of computing and visualising radiaitve frocing at the TOA for CMIP6 data, particularly RFMIP project. 
"""

__version__ = "1.0"

__bibtex__ = """
"""

from .forcing import (compute_forcings_allsky, compute_forcings_clearsky, compute_cloudy_sky)
from .stats import (global_mean, time_series, t_test, t_test_nd)
from .plot import (plot_data, plot_annual_data)
