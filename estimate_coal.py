"""
This script takes the CWON estimates for natural capital rents as national GEP values for coal. 
"""

# Dependencies
import os
import pandas as pd
import geopandas as gpd
import numpy as np  

# Import CWON Estimates 
df_gep = pd.read_excel("../data/cwon-resource-rents/cwon-rents-coal.xlsx")
# Keep only 2019 
col_keep = ['countrycode', 'countryname', 'YR2019']
df_gep = df_gep[col_keep]
# Rename 2019 to gep_coal 
df_gep.rename(columns= {'YR2019': 'gep_coal', 'countrycode': 'country_code', 'countryname': 'country'}, inplace=True)

# Correctiong for ee_r250 country mapping
file_path = "../data/ee_r250_correspondence.gpkg"
gdf = gpd.read_file(file_path)
# Merge on country code from df_gep and adm0_a3 from geopackage
df_merged = pd.merge(gdf, df_gep,  how='left', left_on='adm0_a3', right_on='country_code')
# Keep a subset of variables 
df_merged = df_merged[['ee_r264_id', 'iso3_r250_id', 'iso3_r250_label', 'ee_r264_description', 'gep_coal']]

# Save a csv file of country, year coal values
df_gep = df_merged.sort_values(by = ['ee_r264_id'], ascending = [True])
df_gep.to_csv("../data/gep-datasets/gep-coal.csv", index=False)