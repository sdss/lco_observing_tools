#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2022-08-21
# @Filename: focus.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import multiprocessing
import pathlib
import re

import matplotlib.pyplot as plt
import numpy
import pandas
import seaborn
import sep
from astropy.io import fits


RESULTS = pathlib.Path(__file__).parent / "../results/lco"
PIXEL_SCALE = 0.146

seaborn.set_theme()


def get_seqno(path: pathlib.Path):
    """Returns the sequence number."""

    match = re.search(r"gimg-gfa[1-6]s-([0-9]+).fits", str(path))
    if match:
        return int(match.group(1))
    else:
        raise ValueError


def run_sep(path: pathlib.Path, threshold: float = 5, **sep_opts):
    """Substracts background and runs extraction."""

    seq_no = get_seqno(path)

    data = fits.getdata(str(path)).astype("f8")  # type: ignore
    header = fits.getheader(str(path), 1)

    back = sep.Background(data)
    rms = back.rms()

    stars = sep.extract(data - back, threshold, err=rms)

    df = pandas.DataFrame(stars)
    df["camera"] = int(header["CAMNAME"][3])
    df["seq_no"] = seq_no
    df["mjd"] = int(header["SJD"])
    df["m2piston"] = header["M2PISTON"]

    return df


def process_mjd(mjd: int, min_seqno: int | None = None, max_seqno: int | None = None):
    """Processes and MJD."""

    gcam = pathlib.Path(f"/data/gcam/{mjd}")
    files = gcam.glob("gimg-gfa[1-6]s-[0-9][0-9][0-9][0-9].fits")

    if min_seqno and max_seqno:
        valid_files = []
        for file in files:
            seq_no = get_seqno(file)
            if seq_no >= min_seqno and seq_no <= max_seqno:
                valid_files.append(file)

        files = valid_files

    with multiprocessing.Pool(4) as pool:
        data_list = pool.map(run_sep, files)

    data = pandas.concat(data_list)

    return data


def filter_data(data: pandas.DataFrame):
    """Excludes bad data."""

    ecc = numpy.sqrt(data.a**2 - data.b**2) / data.a

    # fmt: off
    filter = (
        (data.a * PIXEL_SCALE) < 5 &
        ((data.a * PIXEL_SCALE) > 0.4) &
        (data.cpeak < 60000) &
        (ecc < 0.7)
    )
    # fmt: on

    return data.loc[filter]


def get_fwhm(data: pandas.DataFrame, filter: bool = True):
    """Returns the FWHM in arcsec."""

    def _calc_fwhm(g):
        fwhm_pixel = numpy.mean(2 * numpy.sqrt(numpy.log(2) * (g.a**2 + g.b**2)))
        return float(PIXEL_SCALE * fwhm_pixel)

    data = data.copy()
    data = data.set_index(["seq_no", "camera"])

    if filter:
        data = filter_data(data)

    data["fwhm"] = data.groupby(["seq_no", "camera"]).apply(_calc_fwhm)

    return data


def plot_focus(
    data: pandas.DataFrame,
    interactive: bool = True,
    outpath: str | pathlib.Path | None = None,
):
    """Filters and plots focus data."""

    mjd = data.mjd.iloc[0]

    fwhm = get_fwhm(data.copy())
    fwhm_piston = fwhm.groupby("m2piston").apply(lambda g: g.fwhm.median())

    with plt.ioff():  # type: ignore
        fig, ax = plt.subplots()

        seaborn.scatterplot(x=fwhm_piston.index, y=fwhm_piston)
        ax.set_xlabel("M2 Piston [microns]")
        ax.set_ylabel("FWHM [arcsec]")

        ax.set_title(f"{mjd}")

    if interactive:
        plt.show()

    if outpath:
        fig.savefig(str(outpath))

    return fwhm_piston
