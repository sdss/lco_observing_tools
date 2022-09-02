#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2022-09-02
# @Filename: dithers.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from typing import Any

import numpy
from astropy import units as uu
from astropy.coordinates import SkyCoord


__all__ = ["ra_dec_dither"]


def sample_disk(dither_radius: float):
    """Returns the PA and radius of a random offset.

    Parameters
    ----------
    dither_radius
        The dither radius, in degrees.

    """

    angle: Any = numpy.random.uniform() * 360  # degrees
    radius: Any = numpy.sqrt(numpy.random.uniform() * dither_radius**2)
    return angle * uu.deg, radius * uu.deg


def ra_dec_dither(
    dither_radius: float,
    default: tuple[float, float, float] | list[float] = (0.0, 0.0, 0.0),
):
    """Returns a random dither offset in RA/Dec.

    Parameters
    ----------
    field_ra
        The RA of the field centre.
    field_dec
        The Dec of the field centre.
    dither_radius
        The maximum radius of the dither offset, in arcsec.
    default
        A tuple with the default offset ``(ra, dec, pa)``, in arcsec.

    """

    field_centre = SkyCoord(10.0, 0.0, unit="deg", frame="icrs")

    # https://docs.astropy.org/en/stable/coordinates/matchsep.html
    position_angle, radius = sample_disk(dither_radius / 3600.0)
    offset_centre = field_centre.directional_offset_by(position_angle, radius)

    ra_off = (offset_centre.ra - field_centre.ra).arcsec  # type: ignore
    dec_off = (offset_centre.dec - field_centre.dec).arcsec  # type: ignore

    return (
        round(ra_off + default[0], 2),
        round(dec_off + default[1], 2),
        round(default[2], 0),
    )
