"""Auth Menu CLI Entrypoints"""

import logging
import sys

import click

from yojenkins.cli import cli_utility as cu
from yojenkins.cli.cli_utility import log_to_history
from yojenkins.yo_jenkins import Auth, Rest

# Getting the logger reference
logger = logging.getLogger()


@log_to_history
def configure(api_token: str) -> None:
    """Configure authentication

    Args:
        api_token: API token to use for profile setup

    Returns:
        None
    """
    Auth().configure(api_token=api_token)
    click.secho('Successfully configured credentials file', fg='bright_green', bold=True)


@log_to_history
def token(profile: str) -> None:
    """Generate authentication API token

    Args:
        profile: The profile/account to use

    Returns:
        None
    """
    auth = Auth()

    if profile:
        # Add/Refresh the newly generated API token for an existing profile
        data = auth.profile_add_new_token(profile_name=profile)
    else:
        # Simply display the new API Token
        data = auth.generate_token()
    if profile:
        click.secho('success', fg='bright_green', bold=True)
    else:
        click.secho(data, fg='bright_green', bold=True)


@log_to_history
def show(opt_pretty: bool, opt_yaml: bool, opt_xml: bool, opt_toml: bool) -> None:
    """Show the local credentials profiles

    Args:
        opt_pretty: Option to pretty print the output
        opt_yaml: Option to output in YAML format
        opt_xml: Option to output in XML format
        opt_toml: Option to output in TOML format

    Returns:
        None
    """
    data = Auth().show_local_credentials()
    cu.standard_out(data, opt_pretty, opt_yaml, opt_xml, opt_toml)


@log_to_history
def verify(profile: str) -> None:
    """Check if credentials can authenticate

    Args:
        profile: The profile/account to use

    Returns:
        None
    """
    auth = Auth(Rest())
    auth.get_credentials(profile)
    auth.create_auth()
    click.secho('success', fg='bright_green', bold=True)


@log_to_history
def user(opt_pretty: bool, opt_yaml: bool, opt_xml: bool, opt_toml: bool, profile: str) -> None:
    """Show current user information

    Args:
        opt_pretty: Option to pretty print the output
        opt_yaml: Option to output in YAML format
        opt_xml: Option to output in XML format
        opt_toml: Option to output in TOML format
        profile: The profile/account to use

    Returns:
        None
    """
    data = cu.config_yo_jenkins(profile).auth.user()
    cu.standard_out(data, opt_pretty, opt_yaml, opt_xml, opt_toml)