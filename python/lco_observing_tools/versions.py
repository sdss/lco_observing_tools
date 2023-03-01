#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-03-01
# @Filename: versions.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import asyncio
import subprocess

from clu.legacy.tron import TronConnection
from yaml import warnings


# These actors have an actor version command that replies normally,
# so we can just iterate over them.
ACTORS = [
    "apogeefpi",
    "lcolamps",
    "hartmann",
    "apogeeql",
    "alerts",
    "yao",
    "jaeger",
    "cherno",
    "fliswarm",
    "hal",
]


# "apogeecal",
# "apogee",
# "lcotcc",


async def get_actor_versions():
    """Retrieves actor versions by connecting to the hub."""

    client = TronConnection("LCO.versions", "sdss5-hub.lco.cl")
    await client.start(get_keys=False)

    for actor in ACTORS:
        cmd = await client.send_command(actor, "version")

        if cmd.status.did_fail:
            warnings.warn(f"Failed retrieving version for {actor}.", UserWarning)
            continue

        for reply in cmd.replies:
            if reply.message_code == ">" or reply.message == {}:
                continue
            for key, value in reply.message.items():
                name = f"{actor}.{key}"
                name = name.ljust(32)
                print(f"{name} \t {value[0]}")

    cmd_tcc = await client.send_command("lcotcc", "show version")
    tcc_version_reply = cmd_tcc.replies.get("Version")
    if tcc_version_reply:
        print(f"{'lcotcc.version':<32} \t {tcc_version_reply[0]}")

    print(f"{'apogee.version':<32} \t not available")
    print(f"{'apogeecal.version':<32} \t not available")


def get_sos_version():
    """Prints out SoS version."""

    cmd = subprocess.run(
        "source /home/sdss5/config/services/util/sources.sh && "
        "module load idlspec2d && "
        "echo $(idlspec2d_version)+$IDLSPEC2D_VER",
        stdout=subprocess.PIPE,
        shell=True,
    )
    version = cmd.stdout.decode()

    print(f"{'SoS.version':<32} \t {version}")


def get_versions():
    """Retrieves and prints versions of software/actors running at LCO."""

    asyncio.run(get_actor_versions())
    get_sos_version()
