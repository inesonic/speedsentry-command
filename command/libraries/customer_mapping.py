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
Class providing a API you can use to manager customer/server mapping
information

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
# Class Mapping:
#

class Mapping(set):
    """
    Class that encapsulates information about a customer/server mapping.

    """

    def __init__(
        self,
        primary_server_id = 0,
        servers = set()
        ):
        """
        Method that initializes the Mapping instance.

        :param primary_server_id:
            The server ID of the primary server.  This is the server that is
            providing the full suite of customer servers.

        :param servers:
            A set of servers that are servicing this customer.

        :type primary_server_id: int
        :type servers:           set

        """

        set.__init__(self, servers)
        self.__primary_server_id = primary_server_id


    @property
    def primary_server_id(self):
        """
        Read-only property that holds the ID of the primary server.

        :type: int

        """

        return self.__primary_server_id

###############################################################################
# Class CustomerMapping:
#

class CustomerMapping(object):
    """
    Class that can be used to manage customer/server mapping data.

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


    def get(self, customer_id):
        """
        Method you can use to obtain mapping information for a single customer.

        :param customer_id:
            The customer ID of the desired customer.

        :return:
            Returns a Mapping instance holding the mapping information.  The
            value None is returned on error.

        :type customer_id: int
        :rtype:            Mapping or None

        """

        response = self.__rest_api.post_message(
            slug = "mapping/get",
            secret = self.__secret,
            message = { 'customer_id' : customer_id }
        )

        if response is not None and 'status' in response:
            status = response['status']
            if status == 'OK' and 'mapping' in response:
                mapping = response['mapping']
                if 'primary_server' in mapping and 'servers' in mapping:
                    try:
                        primary_server = int(mapping['primary_server'])
                    except:
                        primary_server = None

                    if primary_server is not None:
                        try:
                            servers = { int(s) for s in mapping['servers'] }
                        except:
                            servers = None

                    if servers is not None:
                        result = Mapping(primary_server, servers)
                    else:
                        result = None
                else:
                    result = None
            else:
                result = None
        else:
            result = None

        return result


    def update(self, customer_id, primary_server_id, servers):
        """
        Method you can use to update customer mapping data.

        :param customer_id:
            The customer ID of the customer to be updated.

        :param primary_server_id:
            The primary server used serving this customer.

        :param servers:
            A list or set of servers providing customer service.

        :return:
            Returns True on success, returns False on error.

        :type customer_id:       int
        :type primary_server_id: int
        :type servers:           list or set
        :rtype:                  bool

        """

        server_list = [ primary_server_id ]
        for server_id in servers:
            if server_id != primary_server_id:
                server_list.append(server_id)

        message = {
            'customer_id' : customer_id,
            'mapping' : server_list
        }

        response = self.__rest_api.post_message(
            slug = "mapping/update",
            secret = self.__secret,
            message = message
        )

        return (
                response is not None
            and 'status' in response
            and response['status'] == 'OK'
        )


    def activate(self, customer_id):
        """
        Method you can use to activate a single customer.

        :param customer_id:
            The customer ID of the desired customer.

        :return:
            Returns True on success.  Returns False on error.

        :type customer_id: int
        :rtype:            bool

        """

        response = self.__rest_api.post_message(
            slug = "mapping/customer/activate",
            secret = self.__secret,
            message = { 'customer_id' : customer_id }
        )

        return (
                response is not None
            and 'status' in response
            and response['status'] == 'OK'
        )


    def deactivate(self, customer_id):
        """
        Method you can use to deactivate a single customer.

        :param customer_id:
            The customer ID of the desired customer.

        :return:
            Returns True on success.  Returns False on error.

        :type customer_id: int
        :rtype:            bool

        """

        response = self.__rest_api.post_message(
            slug = "mapping/customer/deactivate",
            secret = self.__secret,
            message = { 'customer_id' : customer_id }
        )

        return (
                response is not None
            and 'status' in response
            and response['status'] == 'OK'
        )


    def list(self, server_id = None):
        """
        Method you can use to obtain a list of customer/server mappings.

        :param server_id:
            If not None, then the returned mappings will only be those that
            reference this server.

        :return:
            Returns a dictionary of mappings by customer ID. The value None is
            returned on error.

        :type server_id: int or None
        :rtype:          dict or None

        """

        if server_id is not None:
            message = { 'server_id' : server_id }
        else:
            message = {}

        response = self.__rest_api.post_message(
            slug = "mapping/list",
            secret = self.__secret,
            message = message
        )

        if response is not None and 'status' in response:
            status = response['status']
            if status == 'OK' and 'mappings' in response:
                result = dict();
                for customer_id, data in response['mappings'].items():
                    primary_server_id = data['primary_server']
                    servers = set(data['servers'])

                    result[int(customer_id)] = Mapping(
                        primary_server_id,
                        servers
                    )
            else:
                result = None
        else:
            result = None

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
