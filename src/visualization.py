from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

from .config import FIGURES_DIR

sns.set(style="whitegrid")

def plot_time_trends(gdf, outcome, out_dir=FIGURES_DIR):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.lineplot(data=gdf, x="year", y=outcome, hue="sez_category", estimator="mean", errorbar="se", ax=ax)
    ax.set_title(f"{outcome} trends by SEZ category")
    fig.tight_layout()
    path = out_dir / f"{outcome.lower()}_trend.png"
    fig.savefig(path, dpi=300)
    plt.close(fig)
    return path

def plot_distribution(gdf, outcome, out_dir=FIGURES_DIR):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=gdf, x="sez_category", y=outcome, ax=ax)
    ax.set_title(f"{outcome} by SEZ category")
    fig.tight_layout()
    path = out_dir / f"{outcome.lower()}_distribution.png"
    fig.savefig(path, dpi=300)
    plt.close(fig)
    return path

def plot_centroid_map(gdf, out_dir=FIGURES_DIR):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 8))
    gdf = gdf.copy()
    centroids = gdf.centroid
    sns.scatterplot(
        x=centroids.x,
        y=centroids.y,
        hue=gdf["sez_category"],
        alpha=0.4,
        ax=ax,
        s=10,
    )
    ax.set_title("SEZ grid centroids")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    path = out_dir / "sez_centroids.png"
    fig.savefig(path, dpi=300)
    plt.close(fig)
    return path
