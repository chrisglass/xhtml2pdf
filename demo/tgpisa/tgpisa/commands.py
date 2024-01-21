"""This module contains functions called from console script entry points."""

import os
import sys
from os.path import dirname, exists, join

import cherrypy
import pkg_resources
import turbogears

cherrypy.lowercase_api = True  # type: ignore[attr-defined]


class ConfigurationError(Exception):
    pass


def start() -> None:
    """Start the CherryPy application server."""
    setupdir = dirname(dirname(__file__))
    curdir = os.getcwd()

    # First look on the command line for a desired config file,
    # if it's not on the command line, then look for 'dev.cfg'
    # in the current directory. If there, load configuration
    # from a file called 'dev.cfg'. If it's not there, the project
    # is probably installed and we'll look first for a file called
    # 'prod.cfg' in the current directory and then for a default
    # config file called 'default.cfg' packaged in the egg.
    if len(sys.argv) > 1:
        configfile = sys.argv[1]
    elif exists(join(setupdir, "dev.cfg")):
        configfile = join(setupdir, "dev.cfg")
    elif exists(join(curdir, "prod.cfg")):
        configfile = join(curdir, "prod.cfg")
    else:
        try:
            configfile = pkg_resources.resource_filename(
                pkg_resources.Requirement.parse("tgpisa"), "config/default.cfg"
            )
        except pkg_resources.DistributionNotFound as e:
            msg = "Could not find default configuration."
            raise ConfigurationError(msg) from e

    turbogears.update_config(configfile=configfile, modulename="tgpisa.config")
    # ruff: noqa: PLC0415
    from tgpisa.controllers import Root

    turbogears.start_server(Root())
