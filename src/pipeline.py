from pathlib import Path

from .config import FIGURES_DIR, PROCESSED_EEP_PATH
from .data_wrangling import build_processed_dataset
from .matching import attach_propensity_scores, COVARIATES
from .models import run_did, run_spillover
from .visualization import plot_time_trends, plot_distribution, plot_centroid_map

TARGETS = ["EVI", "NDVI"]

def run_pipeline():
    gdf = build_processed_dataset()
    gdf, ps_model = attach_propensity_scores(gdf, covariates=COVARIATES)

    figure_paths = []
    for target in TARGETS:
        figure_paths.append(plot_time_trends(gdf, target))
        figure_paths.append(plot_distribution(gdf, target))
    figure_paths.append(plot_centroid_map(gdf))

    model_results = {}
    for target in TARGETS:
        model_results[f"did_{target.lower()}"] = run_did(gdf, target, weight_col="iptw", use_baseline=True)
        model_results[f"spillover_{target.lower()}"] = run_spillover(gdf, target)

    summary = {
        "processed_data_path": PROCESSED_EEP_PATH,
        "figure_paths": figure_paths,
        "models": model_results,
        "propensity_model": ps_model,
    }
    return summary

def main():
    results = run_pipeline()
    print(f"Processed data saved to: {results['processed_data_path']}")
    for path in results["figure_paths"]:
        print(f"Figure created: {path}")
    for name, model in results["models"].items():
        effect = model.params.get("treated:post", model.params.get("adjacent_group:post", None))
        print(f"{name}: estimator term={effect:.4f}" if effect is not None else f"{name}: model fitted")

if __name__ == "__main__":
    main()
