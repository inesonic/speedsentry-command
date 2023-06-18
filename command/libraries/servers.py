#!/usr/bin/python3
#-*-python-*-##################################################################
# Copyright 2021 - 2023 Inesonic, LLC
# 
# This file is licensed under two licenses.
#
# Inesonic Commercial License, Version 1:
#   All rights reserved.  Inesonic, LLC retains all rights to this software,
#   including the right to relicense the software in source or binary formats
#   under different terms.  Unauthorized use under the terms of this license is
#   strictly prohibited.
#
# GNU Public License, Version 3:
#   This program is free software: you can redistribute it and/or modify it
#   under the terms of the GNU General Public License as published by the Free
#   Software Foundation, either version 3 of the License, or (at your option)
#   any later version.
#   
#   This program is distributed in the hope that it will be useful, but WITHOUT
#   ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#   FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#   more details.
#   
#   You should have received a copy of the GNU General Public License along
#   with this program.  If not, see <https://www.gnu.org/licenses/>.
###############################################################################

"""
Class providing a API you can use to manager Server information.

"""

###############################################################################
# Import:
#

import sys
import os
import json
import base64
import time
import datetime

import libraries.enumeration as enumeration
import libraries.rest_api_common_v1 as rest_api_common_v1
import libraries.outbound_rest_api_v1 as outbound_rest_api_v1

###############################################################################
# Globals:
#

STATUS = enumeration.Enum("ALL_UNKNOWN ACTIVE INACTIVE DEFUNCT")
"""
Enumeration of server status values.

"""

###############################################################################
# Class Server:
#

class Server(object):
    """
    Class that encapsulates information about a single server.

    """

    def __init__(
        self,
        server_id,
        region_id,
        identifier,
        status,
        monitors_per_second,
        cpu_loading,
        memory_loading
        ):
        """
        Method that initializes the Server instance.

        :param server_id:
            The server's internal ID.

        :param region_id:
            The region where the server resides.

        :param identifier:
            The server's identifier string.  This string must be either the
            machines publically visible hostname or the machines publically
            visible IP address.

        :param status:
            The current server status.

        :param monitors_per_second:
            The service rate this server must sustain.

        :param cpu_loading:
            The last reported server CPU loading.

        :param memory_loading:
            The last reported memory utilization.

        :type server_id:           int
        :type region_id:           int
        :type identifier:          str
        :type status:              STATUS enumerated value.
        :type monitors_per_second: float
        :type cpu_loading:         float
        :type memory_loading:      float

        """

        super().__init__()

        self.__server_id = int(server_id)
        self.__region_id = int(region_id)
        self.__identifier = str(identifier)
        self.__status = status
        self.__monitors_per_second = float(monitors_per_second)
        self.__cpu_loading = float(cpu_loading)
        self.__memory_loading = float(memory_loading)


    @property
    def server_id(self):
        """
        Read-only property that holds the server ID.

        :type: int

        """

        return self.__server_id


    @property
    def region_id(self):
        """
        Read-write property that holds the region ID where this server resides.

        :type: int

        """

        return self.__region_id


    @region_id.setter
    def region_id(self, value):
        self.__region_id = int(value)


    @property
    def identifier(self):
        """
        Read-write property that holds the server's identifier string.

        :type: str

        """

        return self.__identifier


    @identifier.setter
    def identifier(self, value):
        self.__identifier = str(value)


    @property
    def status(self):
        """
        Read-write property that holds the server's current status.

        :type: STATUS enumerated value.

        """

        return self.__status


    @status.setter
    def status(self, value):
        self.__status = value


    @property
    def monitors_per_second(self):
        """
        Read-only property that holds the last reported monitor service rate.

        :type: int

        """

        return self.__monitors_per_second


    @property
    def cpu_loading(self):
        """
        Read-only property that holds the last reported CPU loading.

        :type: int

        """

        return self.__cpu_loading


    @property
    def memory_loading(self):
        """
        Read-only property that holds the last reported memory loading.

        :type: int

        """

        return self.__memory_loading

###############################################################################
# Class Servers:
#

class Servers(object):
    """
    Class that can be used to manage servers.

    """

    def __init__(self, rest_api, secret):
        """
        Method that initializes the Servers class.

        :param rest_api:
            The outbound REST API instance to be used.

        :param secret:
            The secret to be used.

        :type rest_api: outbound_rest_api_v1.Server
        :type secret:   bytes

        """

        super().__init__()

        self.__rest_api = rest_api
        self.__secret = secret


    def get(self, server_identifier):
        """
        Method you can use to obtain a server instance by server ID.

        :param server_identifier:
            The server ID or address of the desired server.

        :return:
            Returns a Server instance holding information about the server.

        :type region_id: int or str
        :rtype:          Server

        """

        try:
            server_id = int(server_identifier)
            message = { 'server_id' : server_id }
        except:
            message = { 'identifier' : server_identifier }

        response = self.__rest_api.post_message(
            slug = "server/get",
            secret = self.__secret,
            message = message
        )

        if response is not None and 'status' in response:
            status = response['status']
            if status == 'OK':
                try:
                    server_id = int(response['server_id'])
                    region_id = int(response['region_id'])
                    identifier = str(response['identifier'])
                    server_status = STATUS.by_name(
                        response['server_status'].upper()
                    )
                    monitors_per_second = float(
                        response['monitor_service_rate']
                    )
                    cpu_loading = float(response['cpu_loading'])
                    memory_loading = float(response['memory_loading'])
                except:
                    server_id = None
                    region_id = None
                    identifier = None
                    status = None
                    monitors_per_second = None
                    cpu_loading = None
                    memory_loading = None

                if server_id is not None:
                    result = Server(
                        server_id = server_id,
                        region_id = region_id,
                        identifier = identifier,
                        status = server_status,
                        monitors_per_second = monitors_per_second,
                        cpu_loading = cpu_loading,
                        memory_loading = memory_loading
                    )
                else:
                    result = None
            else:
                result = None
        else:
            result = None

        return result


    def create(self, region_id, identifier):
        """
        Method you can use to add a new server.

        :param region_id:
            The region ID where the server resides.

        :param identifier:
            The server's identifier string.  This must be either the server's
            publically visible hostname or the server's publically visible IP
            address.

        :return:
            Returns the newly created server instance.  None is returned on
            error.

        :type region_id:  int
        :type identifier: str
        :rtype:           Server

        """

        response = self.__rest_api.post_message(
            slug = "server/create",
            secret = self.__secret,
            message = {
                'region_id' : region_id,
                'identifier' : identifier
            }
        )

        if response is not None and 'status' in response:
            status = response['status']
            if status == 'OK':
                try:
                    server_id = int(response['server_id'])
                    region_id = int(response['region_id'])
                    identifier = str(response['identifier'])
                    server_status = STATUS.by_name(
                        response['server_status'].upper()
                    )
                    monitors_per_second = float(
                        response['monitor_service_rate']
                    )
                    cpu_loading = float(response['cpu_loading'])
                    memory_loading = float(response['memory_loading'])
                except:
                    server_id = None
                    region_id = None
                    identifier = None
                    status = None
                    monitors_per_second = None
                    cpu_loading = None
                    memory_loading = None

                if server_id is not None:
                    result = Server(
                        server_id = server_id,
                        region_id = region_id,
                        identifier = identifier,
                        status = server_status,
                        monitors_per_second = monitors_per_second,
                        cpu_loading = cpu_loading,
                        memory_loading = memory_loading
                    )
                else:
                    result = None
            else:
                result = None
        else:
            result = None

        return result


    def modify(
        self,
        server_id,
        region_id = None,
        identifier = None,
        status = None
        ):
        """
        Method you can use to update information about a server.

        :param server_id:
            The server ID of the server to be modified.

        :param region_id:
            The new region ID for the server.  The region ID must be valid.  A
            value of None will cause the region ID to remain unchanged.

        :param identifier:
            The new identifier for the server.  A value of None will cause the
            server identifier to remain unchanged.

        :param status:
            The new server status.  A value of None or STATUS.ALL_UNKNOWN will
            cause the server status to remain unchanged.

        :return:
            Returns the updated Server instance or None on error.

        :type server_id:  int
        :type region_id:  int or None
        :type identifier: str or None
        :type status:     STATUS enumerated value or None
        :rtype:           Server or None

        """

        message = { 'server_id' : server_id }

        if region_id is not None:
            message['region_id'] = region_id

        if identifier is not None:
            message['identifier'] = identifier

        if status is not None and status != STATUS.ALL_UNKNOWN:
            message['server_status'] = str(status).lower()

        response = self.__rest_api.post_message(
            slug = "server/modify",
            secret = self.__secret,
            message = message
        )

        if response is not None and 'status' in response:
            status = response['status']
            if status == 'OK':
                try:
                    server_id = int(response['server_id'])
                    region_id = int(response['region_id'])
                    identifier = str(response['identifier'])
                    server_status = STATUS.by_name(
                        response['server_status'].upper()
                    )
                    monitors_per_second = float(
                        response['monitor_service_rate']
                    )
                    cpu_loading = float(response['cpu_loading'])
                    memory_loading = float(response['memory_loading'])
                except:
                    server_id = None
                    region_id = None
                    identifier = None
                    status = None
                    monitors_per_second = None
                    cpu_loading = None
                    memory_loading = None

                if server_id is not None:
                    result = Server(
                        server_id = server_id,
                        region_id = region_id,
                        identifier = identifier,
                        status = server_status,
                        monitors_per_second = monitors_per_second,
                        cpu_loading = cpu_loading,
                        memory_loading = memory_loading
                    )
                else:
                    result = None
            else:
                result = None
        else:
            result = False

        return result


    def delete(self, server):
        """
        Method you can use to delete a server.  Note that deleting a server
        will also cause customer data collected by that server to be deleted.

        Use this method with care.

        :param server:
            The server to be deleted.

        :return:
            Returns True on success.  Returns False on error.

        :type server: Server
        :rtype:       bool

        """

        response = self.__rest_api.post_message(
            slug = "server/delete",
            secret = self.__secret,
            message = { 'server_id' : server.server_id }
        )

        if response is not None and 'status' in response:
            status = response['status']
            if status == 'OK':
                result = True
            else:
                result = False
        else:
            result = False

        return result


    def list(self, region_id = None, status = None):
        """
        Method you can use to obtain a list of servers.

        :param region_id:
            An optional region ID to use to constrain the returned list.  A
            value of None will return servers in all regions.

        :param status:
            An optional status value to use to constraint the returned list.  A
            value of None will return servers with any status.

        :return:
            Returns a list of servers.  None is returned on error.

        :type region_id: int or None
        :type status:    STATUS enumerated value or None
        :rtype:          list or None

        """

        message = dict()

        if region_id is not None:
            message['region_id'] = region_id

        if status is not None and status != STATUS.ALL_UNKNOWN:
            message['server_status'] = str(status).lower()

        response = self.__rest_api.post_message(
            slug = "server/list",
            secret = self.__secret,
            message = message
        )

        if response is not None and 'status' in response:
            status = response['status']
            if status == 'OK' and 'servers' in response:
                servers_data = response['servers']

                result = list()
                for server_data in servers_data:
                    try:
                        server_id = int(server_data['server_id'])
                        region_id = int(server_data['region_id'])
                        identifier = str(server_data['identifier'])
                        server_status = STATUS.by_name(
                            server_data['server_status'].upper()
                        )
                        monitors_per_second = float(
                            server_data['monitor_service_rate']
                        )
                        cpu_loading = float(server_data['cpu_loading'])
                        memory_loading = float(server_data['memory_loading'])
                    except:
                        server_id = None
                        region_id = None
                        identifier = None
                        status = None
                        monitors_per_second = None
                        cpu_loading = None
                        memory_loading = None

                    if server_id is not None:
                        server_instance = Server(
                            server_id = server_id,
                            region_id = region_id,
                            identifier = identifier,
                            status = server_status,
                            monitors_per_second = monitors_per_second,
                            cpu_loading = cpu_loading,
                            memory_loading = memory_loading
                        )
                        result.append(server_instance)
            else:
                result = None
        else:
            result = False

        return result


    def activate(self, server_id):
        """
        Method you can use to activate a server.

        :param server_id:
            The ID of the server to be activated.

        :return:
            Returns True on success.  Returns False on error.

        :type server_id: int
        :rtype:          bool

        """

        response = self.__rest_api.post_message(
            slug = "server/activate",
            secret = self.__secret,
            message = { 'server_id' : server_id }
        )

        if response is not None and 'status' in response:
            status = response['status']
            if status == 'OK':
                result = True
            else:
                result = False
        else:
            result = False

        return result


    def deactivate(self, server_id):
        """
        Method you can use to deactivate a server.

        :param server_id:
            The ID of the server to be deactivated.

        :return:
            Returns True on success.  Returns False on error.

        :type server_id: int
        :rtype:          bool

        """

        response = self.__rest_api.post_message(
            slug = "server/deactivate",
            secret = self.__secret,
            message = { 'server_id' : server_id }
        )

        if response is not None and 'status' in response:
            status = response['status']
            if status == 'OK':
                result = True
            else:
                result = False
        else:
            result = False

        return result


    def start(self, server_id):
        """
        Method you can use to start a server.

        :param server_id:
            The ID of the server to be started.

        :return:
            Returns True on success.  Returns False on error.

        :type server_id: int
        :rtype:          bool

        """

        response = self.__rest_api.post_message(
            slug = "server/start",
            secret = self.__secret,
            message = { 'server_id' : server_id }
        )

        if response is not None and 'status' in response:
            status = response['status']
            if status == 'OK':
                result = True
            else:
                result = False
        else:
            result = False

        return result


    def reassign(self, from_server_id, to_server_id = None):
        """
        Method you can use to reassign work between servers.

        :param from_server_id:
            The server ID of the server to take work away from.

        :param to_server_id:
            The server to reassign work to.  A value of None indicates that the
            work should be reassigned evenly across all other servers in the
            same region.

        :return:
            Returns True on success.  Returns False on error.

        :type from_server_id: int
        :type to_server_id:   int or None
        :rtype:               bool

        """

        message = { 'from_server_id' : from_server_id }

        if to_server_id is not None:
            message['to_server_id'] = to_server_id

        response = self.__rest_api.post_message(
            slug = "server/reassign",
            secret = self.__secret,
            message = message
        )

        result = (
                response is not None
            and 'status' in response
            and response['status'] == 'OK'
        )

        return result


    def redistribute(self, region_id):
        """
        Method you can use to redistribute work across servers in a single
        region.

        :param region_id:
            The region to redistribute work across.

        :return:
            Returns True on success.  Returns False on error.

        :type region_id: int
        :rtype:          bool

        """

        message = { 'region_id' : region_id }

        response = self.__rest_api.post_message(
            slug = "server/redistribute",
            secret = self.__secret,
            message = { 'region_id' : region_id }
        )

        result = (
                response is not None
            and 'status' in response
            and response['status'] == 'OK'
        )

        return result

###############################################################################
# Main:
#

if __name__ == "__main__":
    import sys
    sys.stderr.write(
        "*** This module is not intended to be run as a script..\n"
    )
    exit(1)
