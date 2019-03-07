#
# Filename: os_client_utils.py
# Author: Ade <aussieade@gmail.com>
#
"""openstack client utility functions"""

from __future__ import print_function

import os_client_config
from os_client_config.exceptions import OpenStackConfigException
from keystoneauth1.exceptions.auth_plugins import MissingRequiredOptions


def get_client(service, cloud=False):
    """get openstack service client connection

    :param service: service name (str)
    :param cloud: clouds.yaml cloud name (optional)
    :return: service client connection
    """
    if cloud:
        try:
            return os_client_config.make_client(service, cloud=cloud)
        except OpenStackConfigException:
            print('cloud config for %s not found' % cloud)
            return False
    else:
        try:
            return os_client_config.make_client(service)
        except (OpenStackConfigException, MissingRequiredOptions):
            print('%s client connection failed' % service)
            return False


def get_session(service, cloud=False):
    """get openstack service session

    :param service: service name (str)
    :param cloud: clouds.yaml cloud name (optional)
    :return: service session
    """
    if cloud:
        try:
            return os_client_config.session_client(service, cloud=cloud)
        except OpenStackConfigException:
            print('cloud config for %s not found' % cloud)
            return False
    else:
        try:
            return os_client_config.session_client(service)
        except (OpenStackConfigException, MissingRequiredOptions):
            print('%s create session failed' % service)
            return False
    
