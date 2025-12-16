def choose_sample_every_n(fps: float) -> int:
    if fps >= 90:
        return 4
    if fps >= 50:
        return 2
    return 1
