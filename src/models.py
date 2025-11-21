import statsmodels.api as sm

ADJUSTMENT_COVARS = ["Elevation_m", "Rainfall_mm", "Temperature_C", "NighttimeLight_nW"]

def _fit_ols(formula, data, weights=None):
    if weights is not None:
        model = sm.WLS.from_formula(formula=formula, data=data, weights=weights).fit(cov_type="HC3")
    else:
        model = sm.OLS.from_formula(formula=formula, data=data).fit(cov_type="HC3")
    return model

def run_did(gdf, outcome, weight_col=None, use_baseline=True):
    """DiD: SEZ (1) vs non-SEZ (0) using earliest operational year as baseline."""
    data = gdf[gdf["SEZ"].isin([0, 1])].dropna(subset=[outcome]).copy()
    earliest_oper = data.loc[data["SEZ"] == 1, "year_oper"].min()
    data["post"] = data["year"] >= earliest_oper if use_baseline else data["post_by_grid"]
    data["treated"] = data["SEZ"] == 1
    weights = data[weight_col] if weight_col and weight_col in data else None

    formula = f"{outcome} ~ treated + post + treated:post + " + " + ".join(ADJUSTMENT_COVARS)
    return _fit_ols(formula, data, weights)

def run_spillover(gdf, outcome):
    """Spillover DiD: adjacent (2) vs non-SEZ (0) using SEZ earliest operational year."""
    data = gdf[gdf["SEZ"].isin([0, 2])].dropna(subset=[outcome]).copy()
    baseline = gdf.loc[gdf["SEZ"] == 1, "year_oper"].min()
    data["post"] = data["year"] >= baseline
    data["adjacent_group"] = data["SEZ"] == 2
    formula = f"{outcome} ~ adjacent_group + post + adjacent_group:post + " + " + ".join(ADJUSTMENT_COVARS)
    return _fit_ols(formula, data)
