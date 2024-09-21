"""
This script combines the world bank measures of national GDP with the % of gdp related to petrol. 
Then I adjust for nature's contribution. 
This script produces a panel of country-year values for GEP by petrolium as an ecosystem service. 
"""

# Dependencies
import os
import pandas as pd

def clean_wb_data(df, col_name):
    # Rename variables: 
    old_names = ['Country Name', 'Country Code']
    new_names = ['country', 'country_code']

    # Rename the columns
    rename_dict = dict(zip(old_names, new_names))
    df.rename(columns=rename_dict, inplace=True)

    # Drop non-country attributes
    countries_to_drop = ['Africa Eastern and Southern', 'Africa Western and Central', 'Arab World',
                        'Caribbean small states', 'East Asia & Pacific (excluding high income)',
                        'Early-demographic dividend', 'East Asia & Pacific', 'Europe & Central Asia (excluding high income)',
                        'Europe & Central Asia', 'European Union', 'Fragile and conflict affected situations',
                        'Heavily indebted poor countries (HIPC)', 'IBRD only', 'IDA & IBRD total', 'IDA total',
                        'IDA blend', 'IDA only', 'Not classified', 'Latin America & Caribbean (excluding high income)',
                        'Latin America & Caribbean', 'Least developed countries: UN classification', 'Low income',
                        'Lower middle income', 'Low & middle income', 'Late-demographic dividend', 'Middle income', 
                        'Middle East & North Africa (excluding high income)', 'North America', 'OECD members', 
                        'Other small states', 'Pre-demographic dividend', 'Pacific island small states',
                        'Pacific island small states', 'Sub-Saharan Africa (excluding high income)', 'Sub-Saharan Africa', 'Small states',
                        'East Asia & Pacific (IDA & IBRD countries)', 'Europe & Central Asia (IDA & IBRD countries)', 
                        'Latin America & the Caribbean (IDA & IBRD countries)', 'Middle East & North Africa (IDA & IBRD countries)', 
                        'South Asia (IDA & IBRD)', 'Sub-Saharan Africa (IDA & IBRD countries)', 'Upper middle income', 'World',]
    df = df[~df['country'].isin(countries_to_drop)]

    # Reshape to long format (year - country)
    df = pd.melt(df, 
                id_vars = ['country', 'country_code'], 
                value_vars = [str(year) for year in range(1970, 2022)],  # Years 1970 to 2021
                var_name = "year", 
                value_name = col_name)
    
    # Assert as dataframe
    df = pd.DataFrame(df)
    # Return Dataframe
    return(df)

# Import: World Bank Oil Rents: https://data.worldbank.org/indicator/NY.GDP.PETR.RT.ZS
df_oil_rents = pd.read_excel("../data/world_bank/national_petrol_edited.xls")
# Import: World Bank GDP: https://data.worldbank.org/indicator/NY.GDP.MKTP.CD
df_gdp = pd.read_excel("../data/world_bank/national_gdp_edited.xls")

# Clean oil rents data 
df_oil_rents = clean_wb_data(df_oil_rents, "oil")
# Clean GDP data
df_gdp = clean_wb_data(df_gdp, "gdp")

# Merge GDP with oil rents data
df_gep = pd.merge(left = df_oil_rents,
            right = df_gdp,
            how = 'inner')

# Assign nature's contribution value through resource rent adjustment
resource_rent = 0.3

# Estimate GEP value for oil 
df_gep["gep"] = df_gep["oil"] * df_gep["gdp"] * resource_rent

# Save a csv file of country, year petrolium values
df_gep = df_gep.sort_values(by = ['country', 'year'], ascending = [True, True])
df_gep.to_csv("../data/gep-datasets/gep-petrolium.csv", index=False)