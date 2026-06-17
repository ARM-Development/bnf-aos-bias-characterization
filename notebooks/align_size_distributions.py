import numpy as np


def _to_numpy(a):
    """Strip xarray/pandas wrappers down to a plain numpy array."""
    return np.asarray(getattr(a, "values", a), dtype=float)


def align_size_distributions(dp1, dndlogdp1, dp2, dndlogdp2, common_bins=None):
    """Rebin two size distributions onto a shared diameter grid.

    Parameters
    ----------
    dp1, dp2 : array-like
        Bin-center diameters (same units, e.g. nm). Either 1D (n_bins,)
        or 2D (n_time, n_bins) if the instrument reports time-varying
        bin centers (common for mobility scans).
    dndlogdp1, dndlogdp2 : array-like
        Number concentrations as dN/dlogDp. Either 1D (n_bins,) or
        2D (n_time, n_bins). Time axis must match the time axis of
        the corresponding dp array when dp is 2D.
    common_bins : 1D array, optional
        Bin centers to align onto. Defaults to a log-spaced grid
        spanning the overlap of the two instruments' diameter ranges.

    Returns
    -------
    common_bins : 1D array
    aligned1, aligned2 : arrays
        Interpolated onto `common_bins`. Values outside each
        instrument's native range are NaN.
    """
    dp1 = _to_numpy(dp1)
    dp2 = _to_numpy(dp2)
    y1 = _to_numpy(dndlogdp1)
    y2 = _to_numpy(dndlogdp2)

    if common_bins is None:
        lo = max(np.nanmin(dp1), np.nanmin(dp2))
        hi = min(np.nanmax(dp1), np.nanmax(dp2))
        if not (hi > lo):
            raise ValueError("dp1 and dp2 have no overlapping diameter range")
        n_points = min(dp1.shape[-1], dp2.shape[-1])
        common_bins = np.geomspace(lo, hi, n_points)
    else:
        common_bins = _to_numpy(common_bins)

    log_tgt = np.log10(common_bins)

    def _interp(dp_src, y_src):
        # Case 1: 1D bin centers shared across all times.
        if dp_src.ndim == 1:
            log_src = np.log10(dp_src)
            out_of_range = (common_bins < dp_src.min()) | (common_bins > dp_src.max())
            order = np.argsort(log_src)
            log_src_s = log_src[order]

            if y_src.ndim == 1:
                out = np.interp(log_tgt, log_src_s, y_src[order])
                out[out_of_range] = np.nan
                return out

            out = np.empty((y_src.shape[0], common_bins.size), dtype=float)
            for i in range(y_src.shape[0]):
                out[i] = np.interp(log_tgt, log_src_s, y_src[i, order])
            out[:, out_of_range] = np.nan
            return out

        # Case 2: 2D bin centers (time, n_bins) — interpolate per row.
        if dp_src.ndim != 2 or y_src.ndim != 2 or dp_src.shape != y_src.shape:
            raise ValueError(
                f"dp and dndlogdp shapes incompatible: {dp_src.shape} vs {y_src.shape}"
            )
        out = np.empty((dp_src.shape[0], common_bins.size), dtype=float)
        for i in range(dp_src.shape[0]):
            dp_row = dp_src[i]
            y_row = y_src[i]
            mask = np.isfinite(dp_row) & np.isfinite(y_row) & (dp_row > 0)
            if mask.sum() < 2:
                out[i] = np.nan
                continue
            log_src = np.log10(dp_row[mask])
            order = np.argsort(log_src)
            row = np.interp(log_tgt, log_src[order], y_row[mask][order])
            row[(common_bins < dp_row[mask].min()) | (common_bins > dp_row[mask].max())] = np.nan
            out[i] = row
        return out

    return common_bins, _interp(dp1, y1), _interp(dp2, y2)


if __name__ == "__main__":
    dp_smps = np.geomspace(10, 500, 50)
    dp_aps = np.geomspace(500, 10000, 40)
    n_smps = np.exp(-((np.log(dp_smps) - np.log(100)) ** 2) / 0.5)
    n_aps = np.exp(-((np.log(dp_aps) - np.log(2000)) ** 2) / 0.5)

    bins, a1, a2 = align_size_distributions(
        dp_smps, n_smps, dp_aps, n_aps,
        common_bins=np.geomspace(10, 10000, 80),
    )
    print(f"common bins: {bins.shape}, smps: {a1.shape}, aps: {a2.shape}")
