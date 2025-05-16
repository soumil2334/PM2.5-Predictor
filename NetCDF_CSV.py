import xarray as xr
import pandas as pd

# Ensure the 'netcdf4' library is installed: pip install netcdf4
ds = xr.open_dataset("PM2.5.nc", 
    engine="netcdf4"
)

# Convert to DataFrame
df = ds.to_dataframe().reset_index()

# Save as CSV
df.to_csv("PM2.5.csv", index=False)