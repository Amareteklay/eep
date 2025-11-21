import numpy as np
import statsmodels.api as sm

COVARIATES = ["Elevation_m", "Rainfall_mm", "Temperature_C", "NighttimeLight_nW"]

def fit_propensity_scores(gdf, covariates=COVARIATES):
    """Compute propensity scores using SEZ treated (1) vs control (0)."""
    data = gdf[gdf["SEZ"].isin([0, 1])].dropna(subset=covariates).copy()
    data["treated"] = data["SEZ"] == 1
    X = sm.add_constant(data[covariates])
    model = sm.Logit(data["treated"].astype(int), X).fit(disp=False)
    data["propensity_score"] = model.predict(X)
    data["iptw"] = np.where(
        data["treated"],
        1 / data["propensity_score"].clip(lower=1e-3),
        1 / (1 - data["propensity_score"]).clip(lower=1e-3),
    )
    scores = data[["Grid_ID", "year", "propensity_score", "iptw"]]
    return scores, model

def attach_propensity_scores(gdf, covariates=COVARIATES):
    scores, model = fit_propensity_scores(gdf, covariates)
    merged = gdf.merge(scores, on=["Grid_ID", "year"], how="left")
    return merged, model
