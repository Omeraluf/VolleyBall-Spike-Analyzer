from pathlib import Path
import matplotlib.pyplot as plt

def save_series_plot(values: list[float], out_path: Path, title: str):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure()
    plt.plot(values)
    plt.title(title)
    plt.xlabel("frame index (sampled)")
    plt.ylabel("normalized Y (0=top, 1=bottom)")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
