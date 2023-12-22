#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-03-01
# @Filename: versions.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import asyncio
import re
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
                name = f"{actor}.{key}" if key != "version" else actor
                print(f"{name:<33} \t {value[0]}")

    cmd_tcc = await client.send_command("lcotcc", "show version")
    tcc_version_reply = cmd_tcc.replies.get("Version")
    if tcc_version_reply:
        print(f"{'lcotcc.version':<33} \t {tcc_version_reply[0]}")

    print(f"{'apogee.version':<33} \t not available")
    print(f"{'apogeecal.version':<33} \t not available")


def get_sos_version():
    """Prints out SoS version."""

    cmd = subprocess.run(
        "source /home/sdss5/config/services/util/sources.sh && "
        "module -q load idlspec2d && "
        "echo $(idlspec2d_version)+$IDLSPEC2D_VER",
        stdout=subprocess.PIPE,
        shell=True,
    )
    version = cmd.stdout.decode().strip()

    print(f"{'SoS':<33} \t {version}")


def get_module_versions(modules: list[str]):
    """Prints out module versions."""

    for module in modules:
        cmd = subprocess.run(
            "source /home/sdss5/config/services/util/sources.sh && "
            f"module -q load {module} && "
            f"module show {module}",
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            shell=True,
        )
        info = cmd.stderr.decode()

        match = re.search(rf"{module}/(.+?)\.lua", info, re.MULTILINE)
        if match:
            version = match.group(1)
            print(f"{module:<33} \t {version}")


def get_kronos_versions():
    """Retrieves kronos and autoscheduler versions."""

    cmd = subprocess.run(
        "source /home/sdss5/config/services/util/sources.sh && "
        "module -q load kronos && "
        "kronosversion.py && roboschedulerversion.py",
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        shell=True,
    )

    info = cmd.stdout.decode().strip().split()

    print(f"{'kronos':<33} \t {info[0].strip()}")
    print(f"{'roboscheduler':<33} \t {info[1].strip()}")


def get_versions():
    """Retrieves and prints versions of software/actors running at LCO."""

    asyncio.run(get_actor_versions())
    get_sos_version()
    get_module_versions(["tron"])
    get_kronos_versions()
