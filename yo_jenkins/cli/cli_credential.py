#!/usr/bin/env python3

import logging
import sys

import click
from yo_jenkins.cli import cli_utility as cu
from yo_jenkins.cli.cli_utility import log_to_history

# Getting the logger reference
logger = logging.getLogger()


@log_to_history
def list(opt_pretty: bool, opt_yaml: bool, opt_xml: bool, opt_toml: bool, opt_list: bool, profile: str, folder: str,
         domain: str, keys: str) -> None:
    """TODO Docstring

    Details: TODO

    Args:
        TODO

    Returns:
        TODO
    """
    jy_obj = cu.config_yo_jenkins(profile)
    data, data_list = jy_obj.Credential.list(folder=folder, domain=domain, keys=keys)

    if not data:
        click.echo(click.style('failed', fg='bright_red', bold=True))
        sys.exit(1)
    data = data_list if opt_list else data
    cu.standard_out(data, opt_pretty, opt_yaml, opt_xml, opt_toml)


@log_to_history
def info(opt_pretty: bool, opt_yaml: bool, opt_xml: bool, opt_toml: bool, profile: str, credential: str, folder: str,
         domain: str) -> None:
    """TODO Docstring

    Details: TODO

    Args:
        TODO

    Returns:
        TODO
    """
    jy_obj = cu.config_yo_jenkins(profile)
    data = jy_obj.Credential.info(credential=credential, folder=folder, domain=domain)
    if not data:
        click.echo(click.style('no credential information', fg='bright_red', bold=True))
        sys.exit(1)
    cu.standard_out(data, opt_pretty, opt_yaml, opt_xml, opt_toml)
