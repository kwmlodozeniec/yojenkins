#!/usr/bin/env python3

import json
import logging
import os
import sys
from pathlib import Path

import click
from yo_jenkins.cli import cli_utility as cu
from yo_jenkins.cli.cli_utility import (CONFIG_DIR_NAME, HISTORY_FILE_NAME, log_to_history)
from yo_jenkins.Tools import Package
from yo_jenkins.Utility.utility import (browser_open, html_clean, load_contents_from_local_file)

# Getting the logger reference
logger = logging.getLogger()

BUG_REPORT_URL = "https://github.com/ismet55555/yo-jenkins/issues/new?assignees=&labels=&template=bug_report.md&title="
FEATURE_REQUEST_URL = "https://github.com/ismet55555/yo-jenkins/issues/new?assignees=&labels=&template=feature_request.md&title="


@log_to_history
def upgrade(user: bool, proxy: str) -> None:
    """TODO Docstring

    Details: TODO

    Args:
        TODO

    Returns:
        TODO
    """
    if not Package.install(user=user, proxy=proxy):
        click.echo(click.style('failed to upgrade', fg='bright_red', bold=True))
        sys.exit(1)
    click.echo(click.style('successfully upgraded', fg='bright_green', bold=True))


@log_to_history
def remove() -> None:
    """TODO Docstring

    Details: TODO

    Args:
        TODO

    Returns:
        TODO
    """
    if click.confirm('Are you sure you want to remove yo-jenkins?'):
        Package.uninstall()


@log_to_history
def bug_report() -> None:
    """TODO Docstring

    Details: TODO

    Args:
        TODO

    Returns:
        TODO
    """
    logger.debug(f'Opening bug report webpage in web browser: "{BUG_REPORT_URL}" ...')
    success = browser_open(url=BUG_REPORT_URL)
    if success:
        logger.debug('Successfully opened in web browser')
    else:
        logger.debug('Failed to open in web browser')
    return success


@log_to_history
def feature_request() -> None:
    """TODO Docstring

    Details: TODO

    Args:
        TODO

    Returns:
        TODO
    """
    logger.debug(f'Opening feature request webpage in web browser: "{FEATURE_REQUEST_URL}" ...')
    success = browser_open(url=FEATURE_REQUEST_URL)
    if success:
        logger.debug('Successfully opened in web browser')
    else:
        logger.debug('Failed to open in web browser')
    return success


def history(profile: str, clear: bool) -> None:
    """Displaying the command history and clearing the history file if requested.

    # TODO: Ability to clear only for a specific profile.

    Args:
        profile (str): The name of the profile to to filter history with
        clear (bool):  Clearing the history file

    Returns:
        None
    """
    # Load contents form history file
    history_file_path = os.path.join(os.path.join(Path.home(), CONFIG_DIR_NAME), HISTORY_FILE_NAME)
    contents = load_contents_from_local_file('json', history_file_path)
    if not contents:
        click.echo(click.style('No history found', fg='bright_red', bold=True))
        sys.exit(1)

    # Clearing the history file if requested
    if clear:
        logger.debug(f'Removing history file: {history_file_path} ...')
        try:
            os.remove(history_file_path)
        except OSError:
            logger.debug('Failed to clear history file')
            click.echo(click.style('failed', fg='bright_red', bold=True))
        else:
            logger.debug('Successfully cleared history file')
            click.echo(click.style('successfully cleared', fg='bright_green', bold=True))
            sys.exit(0)

    # Displaying the command history
    logger.debug(f'Displaying command history for profile "{profile}" ...')

    def output_history_to_console(command_list: list, profile_name: str) -> None:
        """Helper function to format and output to console"""
        for command_info in command_list:
            profile_str = f'{click.style("[" + profile_name + "]", fg="yellow", bold=True)}'
            datetime_str = f'{click.style("[" + command_info["datetime"] + "]", fg="green", bold=False)}'
            tool_version = f'{click.style("[" + "v" + command_info["tool_version"] + "]", fg="green", bold=False)}'

            command_info = f'{profile_str} {datetime_str} {tool_version} - {command_info["tool_path"]} {command_info["arguments"]}'
            click.echo(command_info)

    if profile:
        if profile in contents:
            output_history_to_console(contents[profile], profile)
        else:
            click.echo(click.style('No history found for profile: ' + profile, fg='bright_red', bold=True))
    else:
        for profile_name in contents:
            output_history_to_console(contents[profile_name], profile_name)


@log_to_history
def rest_request(profile: str, request_text: str, request_type: str, raw: bool, clean_html: bool) -> None:
    """Send a generic REST request to Jenkins Server using the loaded credentials

    Args:
        profile (str): The name of the credentials profile
        request_text (str): The text of the request to send
        request_type (str): The type of request to send
        raw (bool): Whether to return the raw response or formatted JSON
        clean_html (bool): Whether to clean the HTML tags from the response 

    Returns:
        None
    """
    jy_obj = cu.config_yo_jenkins(profile)
    request_text = request_text.strip('/')
    content, header, success = jy_obj.REST.request(
        target=request_text,
        request_type=request_type,
        json_content=(not raw),
    )

    if not success:
        click.echo(click.style('Failed to make request', fg='bright_red', bold=True))
        sys.exit(1)

    if request_type == 'HEAD':
        print(header)
        sys.exit(0)

    if content:
        if clean_html:
            try:
                print(html_clean(content))
            except Exception:
                print(content)
        else:
            try:
                print(json.dumps(content, indent=4))
            except Exception:
                print(content)
    else:
        click.echo(
            click.style('Content returned, however possible HTML content. Try --raw.', fg='bright_red', bold=True))


@log_to_history
def run_script(profile: str, script_text: str, script_filepath: str, output_filepath: str) -> None:
    """TODO

    Details: TODO: 

    Args:
        TODO 

    Returns:
        None
    """
    jy_obj = cu.config_yo_jenkins(profile)

    # Prepare the commands/script
    if script_text:
        script_text = script_text.strip().replace('  ', ' ')
        script = script_text
    elif script_filepath:
        logger.debug(f'Loading specified script form file: {script_filepath} ...')
        try:
            with open(os.path.join(script_filepath), 'r') as open_file:
                script = open_file.read()
            script_size = os.path.getsize(script_filepath)
            logger.debug(f'Successfully loaded script file ({script_size} Bytes)')
        except FileNotFoundError as error:
            click.echo(
                click.style(f'Failed to find specified script file ({script_filepath})', fg='bright_red', bold=True))
            sys.exit(1)

    # Send the request to the server
    content, _, success = jy_obj.REST.request(target='scriptText',
                                              request_type='post',
                                              data={'script': script},
                                              json_content=False)

    if not success:
        click.echo(click.style('Failed to make script run request', fg='bright_red', bold=True))
        sys.exit(1)

    # Save script result to file
    if output_filepath:
        logger.debug(f'Saving script result into file: {output_filepath} ...')
        try:
            with open(output_filepath, 'w+') as file:
                file.write(content)
            logger.debug('Successfully wrote script result to file')
        except Exception as error:
            logger.debug(f'Failed to write script result to file. Exception: {error}')
            return "", False

    click.echo(content)
