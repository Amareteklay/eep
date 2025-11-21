# Assessing environmental impact of spacial economic zones in ethiopia

## Data
- Open data/raw/eep.csv
- create a pipeline for data cleaning and preprocessing

## Features
- geometry,
- EVI,
- Elevation_m,
- Grid_ID,
- Id,
- NDVI,
- Rainfall_mm,
- Shape_Area,
- Shape_Leng,
- Temperature_C,
- year,
- NighttimeLight_nW,
- centroid_lon,
- centroid_lat,
- index_right,
- industrial_park_name,
- year_oper,
- SEZ

## Target
- Use EVI and NDVI as target variables to assess environmental impact

## Analysis
- Show trends over time and based on SEZ categories
- Use the earliest year_oper data to make comparisons between SEZ grids and non-SEZ grids (SEZ=0)
- For matching, use covariates: Elevation_m, Rainfall_mm, Temperature_C, NighttimeLight_nW
- Create visualizations and save the figures in results/figures
- Save processed data in data/processed/eep_processed.csv
- Create DiD models to assess the impact of SEZs. 
- Do spatial spillover analysis to see if SEZs impact neighboring areas (SEZ=2, adjacent). 

## Deliverables
- Modular code inside the src folder
- Jupyter notebooks for exploratory data analysis and visualizations inside notebooks folder
- Final report in reports/final_report.md

## Tools
- Python
- Libraries: pandas, geopandas, matplotlib, seaborn, statsmodels
- Jupyter Notebooks
