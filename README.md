# lco_observing_tools

![Versions](https://img.shields.io/badge/python->3.7-blue)

## focus_curve

This tool analyses recent GFA images and produces a focus plot with the M2 piston position and the average FWHM from all the cameras for each position.

To use it, first take a focus sweep sequence (ideally using the STUI script) that covers a range of M2 piston values. Then call `focus_curve` as

    focus_curve MJD START END

where `MJD` is the MJD of the data, `START` is the sequence number of the first gimg exposure to use, and `END` is the last one. Alternatively it's possible to use the last N images taken with

    focus_curve --last N

The plot will pop up as a Matplotlib figure.
