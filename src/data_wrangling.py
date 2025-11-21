from pathlib import Path
import pandas as pd
import geopandas as gpd

from .config import RAW_EEP_PATH, PROCESSED_EEP_PATH

def load_raw_eep(path: Path = RAW_EEP_PATH) -> pd.DataFrame:
    """Load raw EEP grid data."""
    return pd.read_csv(path)

def to_geodataframe(df: pd.DataFrame) -> gpd.GeoDataFrame:
    data = df.copy()
    data["geometry"] = gpd.GeoSeries.from_wkt(data["geometry"])
    return gpd.GeoDataFrame(data, geometry="geometry", crs="EPSG:4326")

def clean_eep(df: pd.DataFrame) -> gpd.GeoDataFrame:
    """Clean and augment raw EEP data with treatment flags."""
    gdf = to_geodataframe(df)
    gdf["industrial_park_name"] = gdf["industrial_park_name"].replace({"None": pd.NA})
    gdf["year_oper"] = pd.to_numeric(gdf["year_oper"], errors="coerce")
    gdf["SEZ"] = gdf["SEZ"].fillna(0).astype(int)

    earliest_oper = gdf.loc[gdf["year_oper"].notna(), "year_oper"].min()
    gdf["earliest_oper_year"] = earliest_oper
    gdf["treat"] = gdf["SEZ"] == 1
    gdf["adjacent"] = gdf["SEZ"] == 2
    gdf["post_baseline"] = gdf["year"] >= earliest_oper
    gdf["post_by_grid"] = (gdf["year"] >= gdf["year_oper"]).fillna(False)
    gdf["sez_category"] = gdf["SEZ"].map({0: "non_sez", 1: "sez", 2: "adjacent"}).astype("category")

    return gdf

def save_processed(gdf: gpd.GeoDataFrame, path: Path = PROCESSED_EEP_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    out_df = gdf.copy()
    out_df["geometry"] = out_df.geometry.to_wkt()
    out_df.to_csv(path, index=False)

def build_processed_dataset(raw_path: Path = RAW_EEP_PATH, out_path: Path = PROCESSED_EEP_PATH) -> gpd.GeoDataFrame:
    """Build processed dataset and persist to CSV."""
    raw = load_raw_eep(raw_path)
    gdf = clean_eep(raw)
    save_processed(gdf, out_path)
    return gdf
