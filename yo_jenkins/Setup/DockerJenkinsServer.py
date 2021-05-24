#!/usr/bin/env python3

import logging
from pprint import pprint
from typing import Dict, List, Tuple
import sys
import os
from time import time

import docker

# Getting the logger reference
logger = logging.getLogger()


class DockerJenkinsServer():
    """Class managing containerized Jenkins instance"""

    def __init__(self, protocol_schema:str='http', hostname:str='localhost', port:int=8080, docker_registry:str='registry.hub.docker.com/library/', image_rebuild:bool=False, volumes_renew:bool=False):
        """Object constructor method, called at object creation

        Args:
            None

        Returns:
            None
        """
        # Get the local docker client
        self.docker_client = docker.from_env()

        # Ping the docker client
        if not self.docker_client.ping():
            logger.debug('ERROR: Cannot reach local docker client')
            return
        logger.debug('Successfully connected to local docker client/engine')

        # Image Related
        self.image_dockerfile_dir = os.path.join(
            os.getcwd(),
            'yo_jenkins/server_docker_settings'
            )
        self.image_tag = 'jenkins:jcasc'
        self.image_build_args = {
            "PROTOCOL_SCHEMA": f"{protocol_schema}",
            "JENKINS_HOSTNAME": f"{hostname}",
            "JENKINS_PORT": f"{port}",
            "JENKINS_ADMIN_ID": "admin",
            "JENKINS_ADMIN_PASSWORD": "password"
        }
        self.image_rebuild = image_rebuild

        # Container Related
        self.container_name = 'jenkins'
        self.container_address = f"{protocol_schema}//{hostname}:{port}"
        self.container_ports = {
            '8080/tcp': port,
            '50000/tcp': 50000
        }
        self.container_env_vars = []
        self.container_restart_policy={}
        self.container_remove = False if self.container_restart_policy else True

        # Volume Related
        self.volumes_bind = {}
        self.volumes_named = {'jenkins': '/var/jenkins_home'}
        self.volumes_mounts = []
        self.volumes_renew = volumes_renew


    def setup(self) -> bool:
        """TODO Docstring

        Details: TODO

        Args:
            TODO

        Returns:
            TODO
        """
        self.__container_kill()

        if self.image_rebuild:
            self.__image_remove()
        self.__image_build()

        self.__volumes_create()

        self.__container_run()


    def all_clean(self) -> bool:
        """TODO Docstring

        Details: TODO

        Args:
            TODO

        Returns:
            TODO
        """
        # Remove existing container that matches name
        self.__container_kill()

        # Remove the existing volume that matches name
        self.__volumes_remove()

        # Remove existing images
        self.__image_remove()


    def __image_build(self) -> bool:
        """TODO Docstring

        Details: TODO

        Args:
            TODO

        Returns:
            TODO
        """
        start_time = time()
        logger.info(f'Building image: {self.image_tag} ...')
        logger.info(f'Dockerfile directory: {self.image_dockerfile_dir}')
        try:
            self.docker_client.images.build(
                path=self.image_dockerfile_dir,
                tag=self.image_tag,
                rm=True,
                buildargs=self.image_build_args,
                quiet=False
            )
        except Exception as e:
            logger.info(f'Failed to build image: {self.image_tag}. Exception: {e}')
            return False
        logger.info(f'Successfully build image: {self.image_tag} (Elapsed time: {time() - start_time}s)')
        return True
        # Get the image tag name (same as self.image_tag???)
        # self.image_tag_name = image[0].tags[0]

    def __image_remove(self) -> bool:
        """TODO Docstring

        Details: TODO

        Args:
            TODO

        Returns:
            TODO
        """
        logger.info(f'Removing image: {self.image_tag} ...')
        try:
            self.docker_client.images.remove(self.image_tag)
        except Exception as e:
            logger.info(f'Failed to remove image: {self.image_tag}. Exception: {e}')
            return False
        logger.info(f'Successfully removed image: {self.image_tag}')
        return True


    def __volumes_create(self) -> bool:
        """TODO Docstring

        Details: TODO

        Args:
            TODO

        Returns:
            TODO
        """
        self.volumes_mounts = []

        # Bind Volume Mounts
        for volume_source, volume_target in self.volumes_bind.items():
            logger.info(f'Adding new local bind volume to mount list: {volume_source} -> {volume_target} ...')
            mount = docker.types.Mount(
                source=volume_source,
                target=volume_target,
                type='bind',
                read_only=False
            )
            self.volumes_mounts.append(mount)

        # Named Volume Mounts
        for volume_name, volume_dir in self.volumes_named.items():
            try:
                volume_handle = self.docker_client.volumes.get(volume_name)
                if self.volumes_renew:
                    logger.info(f'Removing found matching/existing named volume: {volume_name} ...')
                    volume_handle.remove(force=True)
                else:
                    logger.warning(f'Using found matching/existing named volume: {volume_name}')
            except:
                logger.info(f'Creating new named volume: {volume_name}')
                self.docker_client.volumes.create(name=volume_name, driver='local')
                logger.info('Successfully created!')

            logger.info(f'Adding named volumes to mount list: {volume_name} ...')
            mount = docker.types.Mount(
                target=volume_dir,
                source=volume_name,
                type='volume',
                read_only=False
            )
            self.volumes_mounts.append(mount)

        logger.info(f'Number of volumes to be mounted to container: {len(self.volumes_mounts)}')


    def __volumes_remove(self) -> bool:
        """TODO Docstring

        Details: TODO

        Args:
            TODO

        Returns:
            TODO
        """
        logger.warning(f'Removing named volumes: {self.volumes_named.keys()}')
        for volume_name in self.volumes_named:
            try:
                volume_named = self.docker_client.volumes.get(volume_name)
                volume_named.remove(force=True)
                logger.warning(f'    - Volume: {volume_name} - REMOVED')
            except Exception as e:
                logger.warning(f'    - Volume: {volume_name} - FAILED - Exception: {e}')


    def __container_run(self) -> bool:
        """TODO Docstring

        Details: TODO

        Args:
            TODO

        Returns:
            TODO
        """
        logger.info(f'Creating and running container: {self.container_name} ...')
        try:
            self.docker_client.containers.run(
                name=self.container_name,
                image=self.image_tag,
                environment=self.container_env_vars,
                ports=self.container_ports,
                mounts=self.volumes_mounts,
                restart_policy=self.container_restart_policy,
                remove=self.container_remove,
                auto_remove=self.container_remove,
                detach=True
                )
        except Exception as e:
            logger.warning(f'Failed to run container: {self.container_name} Exception: {e}')
            return False
        logger.info(f'Successfully running container: {self.container_name}')
        logger.info(f'Container is running here: {self.container_address}')
        return True


    def __container_stop(self) -> bool:
        """TODO Docstring

        Details: TODO

        Args:
            TODO

        Returns:
            TODO
        """
        logger.warning(f'Stopping container with matching tag: {self.container_name} ...')
        try:
            container_handle = self.docker_client.containers.get(self.container_name)
            container_handle.stop()
            logger.warning('Container is stopped')
        except Exception as e:
            logger.warning(f'Failed to stop container matching tag: {self.container_name}. Exception: {e}')


    def __container_kill(self) -> bool:
        """TODO Docstring

        Details: TODO

        Args:
            TODO

        Returns:
            TODO
        """
        logger.warning(f'Killing container with matching tag: {self.container_name} ...')
        try:
            container_handle = self.docker_client.containers.get(self.container_name)
            container_handle.kill()
            logger.warning('Container is dead')
        except Exception as e:
            logger.warning(f'Failed to kill container matching tag: {self.container_name}. Exception: {e}')
