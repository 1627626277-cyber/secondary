from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "manuscript_figures"
OUT.mkdir(parents=True, exist_ok=True)


def copy_stem(source_stem: Path, target_stem: Path) -> None:
    for ext in ["png", "pdf", "svg"]:
        source = source_stem.with_suffix(f".{ext}")
        if source.exists():
            shutil.copyfile(source, target_stem.with_suffix(f".{ext}"))


def main() -> None:
    spatial_path = ROOT / "analysis" / "spatial_autocorrelation_niche" / "spatial_autocorrelation_niche_summary.png"
    sensitivity_path = ROOT / "analysis" / "commppass_sensitivity_models" / "commppass_os_sensitivity_forestplot.png"
    if not spatial_path.exists():
        raise FileNotFoundError(spatial_path)
    if not sensitivity_path.exists():
        raise FileNotFoundError(sensitivity_path)

    copy_stem(
        ROOT / "analysis" / "spatial_autocorrelation_niche" / "spatial_autocorrelation_niche_summary",
        OUT / "fig3_spatial_organization",
    )
    copy_stem(
        ROOT / "analysis" / "commppass_sensitivity_models" / "commppass_os_sensitivity_forestplot",
        OUT / "fig8_commppass_sensitivity_models",
    )
    print(OUT / "fig3_spatial_organization.png")
    print(OUT / "fig8_commppass_sensitivity_models.png")


if __name__ == "__main__":
    main()
