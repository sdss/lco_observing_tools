# lco_observing_tools

![Versions](https://img.shields.io/badge/python->3.7-blue)

## focus_curve

This tool analyses recent GFA images and produces a focus plot with the M2 piston position and the average FWHM from all the cameras for each position.

To use it, first take a focus sweep sequence (ideally using the STUI script) that covers a range of M2 piston values. Then call `focus_curve` as

    focus_curve MJD START END

where `MJD` is the MJD of the data, `START` is the sequence number of the first gimg exposure to use, and `END` is the last one. Alternatively it's possible to use the last N images taken with

    focus_curve --last N

The plot will pop up as a Matplotlib figure.


## cherno_dither

Produces a series of printouts with the `cherno` offset commands for a RA/Dec dither sequence. To get a sequence of 9 dithers with a maximum radius of 1 arcsec.

    $ cherno_dither 1 -n 9
    cherno offset 0.0 0.0 0.0
    cherno offset -0.84 -0.12 0.0
    cherno offset -0.19 -0.92 0.0
    cherno offset 0.05 0.62 0.0
    cherno offset -0.07 -0.15 0.0
    cherno offset -0.47 -0.72 0.0
    cherno offset 0.66 0.7 0.0
    cherno offset -0.07 0.85 0.0
    cherno offset 0.82 -0.05 0.0
    cherno offset 0.72 0.19 0.0

Note that the first offset is always the default one. To use a different default offset

    $ cherno_dither 0.75 -n 3 --default -3.5 1 420
    cherno offset -3.5 1.0 420.0
    cherno offset -3.23 1.08 420.0
    cherno offset -3.9 0.42 420.0
    cherno offset -3.43 0.4 420.0
