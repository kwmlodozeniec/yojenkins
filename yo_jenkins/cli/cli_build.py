#!/usr/bin/env python3

import logging
import sys

import click
from yo_jenkins.cli.cli_utility import log_to_history
from yo_jenkins.YoJenkins.Status import Status

from yo_jenkins.cli import cli_utility as cu

# Getting the logger reference
logger = logging.getLogger()


@log_to_history
def info(opt_pretty: bool, opt_yaml: bool, opt_xml: bool, opt_toml: bool, profile: str, job: str, build_number: int,
         build_url: str, latest: bool) -> None:
    """TODO Docstring

    Args:
        TODO

    Returns:
        TODO
    """
    if job and not build_number and not latest:
        click.echo(
            click.style('INPUT ERROR: For job, either specify --number or --latest. See --help',
                        fg='bright_red',
                        bold=True))
        sys.exit(1)

    jy_obj = cu.config_yo_jenkins(profile)

    # Verify URLs
    if build_url:
        if not cu.is_full_url(build_url):
            click.echo(click.style('build url not formatted correctly', fg='bright_red', bold=True))
            sys.exit(1)
        valid_url_format = True
    else:
        valid_url_format = cu.is_full_url(job)

    # Request the data
    if valid_url_format:
        data = jy_obj.Build.info(build_url=build_url, job_url=job, build_number=build_number, latest=latest)
    else:
        data = jy_obj.Build.info(build_url=build_url, job_name=job, build_number=build_number, latest=latest)

    if not data:
        click.echo(click.style('no build information', fg='bright_red', bold=True))
        sys.exit(1)
    cu.standard_out(data, opt_pretty, opt_yaml, opt_xml, opt_toml)


@log_to_history
def status(profile: str, job: str, build_number: int, build_url: str, latest: bool) -> None:
    """TODO Docstring

    Args:
        TODO

    Returns:
        TODO
    """
    if job and not build_number and not latest:
        click.echo(
            click.style('INPUT ERROR: For job, either specify --number or --latest. See --help',
                        fg='bright_red',
                        bold=True))
        sys.exit(1)

    jy_obj = cu.config_yo_jenkins(profile)

    # Verify URLs
    if build_url:
        if not cu.is_full_url(build_url):
            click.echo(click.style('build url not formatted correctly', fg='bright_red', bold=True))
            sys.exit(1)
        valid_url_format = True
    else:
        valid_url_format = cu.is_full_url(job)

    # Request the data
    if valid_url_format:
        data = jy_obj.Build.status_text(build_url=build_url, job_url=job, build_number=build_number, latest=latest)
    else:
        data = jy_obj.Build.status_text(build_url=build_url, job_name=job, build_number=build_number, latest=latest)

    if not data:
        click.echo(click.style('No status found', fg='bright_red', bold=True))
        sys.exit(1)

    # Color for output
    if data.upper() in Status.unknown.value:
        output_fg = 'black'
    elif data.upper() in Status.queued.value:
        output_fg = 'yellow'
    elif data.upper() in Status.running.value:
        output_fg = 'blue'
    elif data.upper() in Status.success.value:
        output_fg = 'bright_green'
    elif data.upper() in Status.failure.value:
        output_fg = 'bright_red'
    else:
        output_fg = ''
    click.echo(click.style(f'{data}', fg=output_fg, bold=True))


@log_to_history
def abort(profile: str, job: str, build_number: int, build_url: str, latest: bool) -> None:
    """TODO Docstring

    Args:
        TODO

    Returns:
        TODO
    """
    if job and not build_number and not latest:
        click.echo(
            click.style('INPUT ERROR: For job, either specify --number or --latest. See --help',
                        fg='bright_red',
                        bold=True))
        sys.exit(1)

    jy_obj = cu.config_yo_jenkins(profile)

    # Verify URLs
    if build_url:
        if not cu.is_full_url(build_url):
            click.echo(click.style('build url not formatted correctly', fg='bright_red', bold=True))
            sys.exit(1)
        valid_url_format = True
    else:
        valid_url_format = cu.is_full_url(job)

    # Request the data
    if valid_url_format:
        data = jy_obj.Build.abort(build_url=build_url, job_url=job, build_number=build_number, latest=latest)
    else:
        data = jy_obj.Build.abort(build_url=build_url, job_name=job, build_number=build_number, latest=latest)

    if not data:
        click.echo(click.style('failed', fg='bright_red', bold=True))
        sys.exit(1)

    click.echo(click.style('success', fg='bright_green', bold=True))


@log_to_history
def delete(profile: str, job: str, build_number: int, build_url: str, latest: bool) -> None:
    """TODO Docstring

    Args:
        TODO

    Returns:
        TODO
    """
    if job and not build_number and not latest:
        click.echo(
            click.style('INPUT ERROR: For job, either specify --number or --latest. See --help',
                        fg='bright_red',
                        bold=True))
        sys.exit(1)

    jy_obj = cu.config_yo_jenkins(profile)

    # Verify URLs
    if build_url:
        if not cu.is_full_url(build_url):
            click.echo(click.style('build url not formatted correctly', fg='bright_red', bold=True))
            sys.exit(1)
        valid_url_format = True
    else:
        valid_url_format = cu.is_full_url(job)

    # Request the data
    if valid_url_format:
        data = jy_obj.Build.delete(build_url=build_url, job_url=job, build_number=build_number, latest=latest)
    else:
        data = jy_obj.Build.delete(build_url=build_url, job_name=job, build_number=build_number, latest=latest)

    if not data:
        click.echo(click.style('failed', fg='bright_red', bold=True))
        sys.exit(1)

    click.echo(click.style('{data}', fg='bright_green', bold=True))


@log_to_history
def stages(opt_pretty: bool, opt_yaml: bool, opt_xml: bool, opt_toml: bool, profile: str, opt_list: bool, job: str,
           build_number: int, build_url: str, latest: bool) -> None:
    """TODO Docstring

    Args:
        TODO

    Returns:
        TODO
    """
    if job and not build_number and not latest:
        click.echo(
            click.style('INPUT ERROR: For job, either specify --number or --latest. See --help',
                        fg='bright_red',
                        bold=True))
        sys.exit(1)

    jy_obj = cu.config_yo_jenkins(profile)

    # Verify URLs
    if build_url:
        if not cu.is_full_url(build_url):
            click.echo(click.style('build url not formatted correctly', fg='bright_red', bold=True))
            sys.exit(1)
        valid_url_format = True
    else:
        valid_url_format = cu.is_full_url(job)

    # Request the data
    if valid_url_format:
        data, data_list = jy_obj.Build.stage_list(build_url=build_url,
                                                  job_url=job,
                                                  build_number=build_number,
                                                  latest=latest)
    else:
        data, data_list = jy_obj.Build.stage_list(build_url=build_url,
                                                  job_name=job,
                                                  build_number=build_number,
                                                  latest=latest)

    if not data:
        click.echo(click.style('failed', fg='bright_red', bold=True))
        sys.exit(1)

    data = data_list if opt_list else data
    cu.standard_out(data, opt_pretty, opt_yaml, opt_xml, opt_toml)


@log_to_history
def logs(profile: str, job: str, build_number: int, build_url: str, latest: bool, tail: float, download_dir: bool,
         follow: bool) -> None:
    """TODO Docstring

    Args:
        TODO

    Returns:
        TODO
    """
    if job and not build_number and not latest:
        click.echo(
            click.style('INPUT ERROR: For job, either specify --number or --latest. See --help',
                        fg='bright_red',
                        bold=True))
        sys.exit(1)

    jy_obj = cu.config_yo_jenkins(profile)

    # Verify URLs
    if build_url:
        if not cu.is_full_url(build_url):
            click.echo(click.style('build url not formatted correctly', fg='bright_red', bold=True))
            sys.exit(1)
        valid_url_format = True
    else:
        valid_url_format = cu.is_full_url(job)

    # Request the data
    if valid_url_format:
        data = jy_obj.Build.logs(build_url=build_url,
                                 job_url=job,
                                 build_number=build_number,
                                 latest=latest,
                                 tail=tail,
                                 download_dir=download_dir,
                                 follow=follow)
    else:
        data = jy_obj.Build.logs(build_url=build_url,
                                 job_name=job,
                                 build_number=build_number,
                                 latest=latest,
                                 tail=tail,
                                 download_dir=download_dir,
                                 follow=follow)

    if not data:
        click.echo(click.style('failed', fg='bright_red', bold=True))
        sys.exit(1)

    if download_dir:
        click.echo(click.style('success', fg='bright_green', bold=True))


@log_to_history
def browser(profile: str, job: str, build_number: int, build_url: str, latest: bool) -> None:
    """TODO Docstring

    Args:
        TODO

    Returns:
        TODO
    """
    if job and not build_number and not latest:
        click.echo(
            click.style('INPUT ERROR: For job, either specify --number or --latest. See --help',
                        fg='bright_red',
                        bold=True))
        sys.exit(1)

    jy_obj = cu.config_yo_jenkins(profile)

    # Verify URLs
    if build_url:
        if not cu.is_full_url(build_url):
            click.echo(click.style('build url not formatted correctly', fg='bright_red', bold=True))
            sys.exit(1)
        valid_url_format = True
    else:
        valid_url_format = cu.is_full_url(job)

    # Request the data
    if valid_url_format:
        data = jy_obj.Build.browser_open(build_url=build_url, job_url=job, build_number=build_number, latest=latest)
    else:
        data = jy_obj.Build.browser_open(build_url=build_url, job_name=job, build_number=build_number, latest=latest)

    if not data:
        click.echo(click.style('failed', fg='bright_red', bold=True))
        sys.exit(1)


@log_to_history
def monitor(profile: str, job: str, build_number: int, build_url: str, latest: bool, sound: bool) -> None:
    """TODO Docstring

    Args:
        TODO

    Returns:
        TODO
    """
    if job and not build_number and not latest:
        click.echo(
            click.style('INPUT ERROR: For job, either specify --number or --latest. See --help',
                        fg='bright_red',
                        bold=True))
        sys.exit(1)

    jy_obj = cu.config_yo_jenkins(profile)

    # Verify URLs
    if build_url:
        if not cu.is_full_url(build_url):
            click.echo(click.style('build url not formatted correctly', fg='bright_red', bold=True))
            sys.exit(1)
        valid_url_format = True
    else:
        valid_url_format = cu.is_full_url(job)

    # Request the data
    if valid_url_format:
        data = jy_obj.Build.monitor(build_url=build_url,
                                    job_url=job,
                                    build_number=build_number,
                                    latest=latest,
                                    sound=sound)
    else:
        data = jy_obj.Build.monitor(build_url=build_url,
                                    job_name=job,
                                    build_number=build_number,
                                    latest=latest,
                                    sound=sound)

    if not data:
        click.echo(click.style('failed', fg='bright_red', bold=True))
        sys.exit(1)
