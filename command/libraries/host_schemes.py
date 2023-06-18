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
Class providing a API you can use to manage Host/Scheme information.

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
import urllib

import libraries.enumeration as enumeration
import libraries.rest_api_common_v1 as rest_api_common_v1
import libraries.outbound_rest_api_v1 as outbound_rest_api_v1

###############################################################################
# Globals:
#

SCHEME = enumeration.Enum("INVALID HTTP HTTPS FTP SFTP")
"""
The supported schemes used to access remote servers.

"""

###############################################################################
# Class HostScheme:
#

class HostScheme(object):
    """
    Class that tracks information related to a host and scheme.

    """

    def __init__(
        self,
        host_scheme_id = None,
        customer_id = None,
        host = None,
        scheme = SCHEME.INVALID,
        ssl_expiration_timestamp = None
        ):
        """
        Method that initializes the HostPort class.

        :param host_scheme_id:
            The host/scheme ID used to reference this entry.  This value will
            be unique.

        :param customer_id:
            The customer ID of the customer tied to this entry.

        :param host:
            The host FQDN.

        :param scheme:
            The scheme used to access this system.

        :param ssl_expiration_timestamp:
            The Unix timestamp indicating when the SSL certificate associated
            with this system is expected to expire.

        :type host_scheme_id:           int
        :type customer_id:              int
        :type host:                     str
        :type scheme:                   host_scheme.SCHEME enumerated value.
        :type ssl_expiration_timestamp: int

        """

        super().__init__()

        self.__host_scheme_id = host_scheme_id
        self.__customer_id = customer_id
        self.__host = host
        self.__scheme = scheme
        self.__ssl_expiration_timestamp = ssl_expiration_timestamp


    @property
    def host_scheme_id(self):
        """
        Read-only property that holds the host/scheme ID.

        :type: int

        """

        return self.__host_scheme_id


    @property
    def customer_id(self):
        """
        Property that holds the customer ID.

        :type: int

        """

        return self.__customer_id


    @customer_id.setter
    def customer_id(self, value):
        self.__customer_id = int(value)


    @property
    def host(self):
        """
        Property that holds the host FQDN.

        :type: str

        """

        return self.__host


    @host.setter
    def host(self, value):
        self.__host = str(value)


    @property
    def scheme(self):
        """
        Property that holds the scheme used to communicate with the host.

        :type: host_scheme.SCHEME enumerated value.

        """

        return self.__scheme


    @scheme.setter
    def scheme(self, value):
        self.__scheme = value


    @property
    def ssl_expiration_timestamp(self):
        """
        Property that holds the ssl_expiration_timestamp.

        :type: int

        """

        return self.__ssl_expiration_timestamp


    @ssl_expiration_timestamp.setter
    def ssl_expiration_timestamp(self, value):
        self.__ssl_expiration_timestamp = int(value)

###############################################################################
# Class HostSchemes:
#

class HostSchemes(object):
    """
    Class that can be used to manage host/scheme data.

    """

    def __init__(self, rest_api, secret):
        """
        Method that initializes the HostSchemes class.

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


    def get(self, host_scheme_id):
        """
        Method you can use to obtain a specific host/scheme instance by
        host/scheme ID.

        :param host_scheme_id:
            The host/scheme ID to obtain.

        :return:
            Returns a HostScheme instance holding the requested host scheme.  A
            value of None is returned on error.

        :type host_scheme_id: int
        :rtype:               HostScheme or None

        """

        response = self.__rest_api.post_message(
            slug = "host_scheme/get",
            secret = self.__secret,
            message = { 'host_scheme_id' : host_scheme_id }
        )

        if response is not None and 'status' in response:
            status = response['status']
            if status == 'OK':
                try:
                    host_scheme_id = int(response['host_scheme_id'])
                    customer_id = int(response['customer_id'])
                    url = response['url']
                    ssl_expiration_timestamp = int(
                        response['ssl_expiration_timestamp']
                    )
                except:
                    host_scheme_id = None
                    customer_id = None
                    url = None
                    ssl_expiration_timestamp = None

                if host_scheme_id is not None:
                    (
                        scheme_string,
                        network_location,
                        path,
                        parameters,
                        query_fields,
                        fragment
                    ) = urllib.parse.urlparse(
                        url
                    )

                    try:
                        scheme = SCHEME.by_name(scheme_string.upper())
                    except:
                        scheme = None

                    if scheme is not None:
                        result = HostScheme(
                            host_scheme_id = host_scheme_id,
                            customer_id = customer_id,
                            host = network_location,
                            scheme = scheme,
                            ssl_expiration_timestamp = ssl_expiration_timestamp
                        )
                    else:
                        result = None
                else:
                    result = None
            else:
                result = None
        else:
            result = None

        return result


    def create(self, customer_id, url):
        """
        Method you can use to add a new host/scheme.

        :param customer_id:
            The customer ID to tie to the host/scheme.

        :param url:
            The URL to tie to the host/scheme.

        :return:
            Returns the newly created host/scheme instance.  None is returned
            on error.

        :type customer_id: int
        :type url:         str
        :rtype:            HostScheme

        """

        response = self.__rest_api.post_message(
            slug = "host_scheme/create",
            secret = self.__secret,
            message = {
                'customer_id' : customer_id,
                'url' : url
            }
        )

        if response is not None and 'status' in response:
            status = response['status']
            if status == 'OK':
                try:
                    host_scheme_id = int(response['host_scheme_id'])
                    customer_id = int(response['customer_id'])
                    url = response['url']
                    ssl_expiration_timestamp = int(
                        response['ssl_expiration_timestamp']
                    )
                except:
                    host_scheme_id = None
                    customer_id = None
                    url = None
                    ssl_expiration_timestamp = None

                if host_scheme_id is not None    and \
                   ssl_expiration_timestamp >= 0     :
                    (
                        scheme_string,
                        network_location,
                        path,
                        parameters,
                        query_fields,
                        fragment
                    ) = urllib.parse.urlparse(
                        url
                    )

                    try:
                        scheme = SCHEME.by_name(scheme_string.upper())
                    except:
                        scheme = None

                    if scheme is not None:
                        result = HostScheme(
                            host_scheme_id = host_scheme_id,
                            customer_id = customer_id,
                            host = network_location,
                            scheme = scheme,
                            ssl_expiration_timestamp = ssl_expiration_timestamp
                        )
                    else:
                        result = None
                else:
                    result = None
            else:
                result = None
        else:
            result = None

        return result


    def modify(
        self,
        host_scheme_id,
        customer_id = None,
        url = None
        ):
        """
        Method you can use to update information about a host/scheme.

        :param host_scheme_id:
            The host/scheme ID of the host/scheme to be modified.

        :param customer_id:
            The new customer ID for the host/scheme.  The customer ID is not
            checked.  A value of None will cause the customer ID to remain
            unchanged.

        :param url:
            A combined URL holding the new scheme and host.  A value of None
            will cause the scheme and host to remain unchanged.

        :return:
            Returns the updated HostScheme instance or None on error.

        :type host_scheme_id: int
        :type customer_id:    int or None
        :type url:            str or None
        :rtype:               HostScheme or None

        """

        message = { 'host_scheme_id' : host_scheme_id }

        if customer_id is not None:
            message['customer_id'] = customer_id

        if url is not None:
            message['url'] = url

        response = self.__rest_api.post_message(
            slug = "host_scheme/modify",
            secret = self.__secret,
            message = message
        )

        if response is not None and 'status' in response:
            status = response['status']
            if status == 'OK':
                try:
                    host_scheme_id = int(response['host_scheme_id'])
                    customer_id = int(response['customer_id'])
                    url = response['url']
                    ssl_expiration_timestamp = int(
                        response['ssl_expiration_timestamp']
                    )
                except:
                    host_scheme_id = None
                    customer_id = None
                    url = None
                    ssl_expiration_timestamp = None

                if host_scheme_id is not None    and \
                   ssl_expiration_timestamp >= 0     :
                    (
                        scheme_string,
                        network_location,
                        path,
                        parameters,
                        query_fields,
                        fragment
                    ) = urllib.parse.urlparse(
                        url
                    )

                    try:
                        scheme = SCHEME.by_name(scheme_string.upper())
                    except:
                        scheme = None

                    if scheme is not None:
                        result = HostScheme(
                            host_scheme_id = host_scheme_id,
                            customer_id = customer_id,
                            host = network_location,
                            scheme = scheme,
                            ssl_expiration_timestamp = ssl_expiration_timestamp
                        )
                    else:
                        result = None
                else:
                    result = None
            else:
                result = None
        else:
            result = False

        return result


    def delete(self, host_scheme):
        """
        Method you can use to delete a host/scheme.  Note that deleting a
        host/scheme will also cause any slugs associated with that host scheme
        to also be deleted.

        Use this method with care.

        :param host_scheme:
            The server to be deleted.

        :return:
            Returns true on success.  Returns false on error.

        :type server: Server
        :rtype:       bool

        """

        response = self.__rest_api.post_message(
            slug = "host_scheme/delete",
            secret = self.__secret,
            message = { 'host_scheme_id' : host_scheme.host_scheme_id }
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


    def purge(self, customer_id):
        """
        Method you can use to delete all host/schemes tied to a given customer.
        Note that deleting these host schemes will also delete all slugs tied
        to the host schemes.

        Use this method with care.

        :param customer_id:
            The server to be deleted.

        :return:
            Returns true on success.  Returns false on error.

        :type server: Server
        :rtype:       bool

        """

        response = self.__rest_api.post_message(
            slug = "host_scheme/delete",
            secret = self.__secret,
            message = { 'customer_id' : customer_id }
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


    def list(self, customer_id = None):
        """
        Method you can use to obtain a list of host schemes.

        :param customer_id:
            An optional customer ID used to constraint the list to only
            host/schemes tied to a single customer.  A value of None will cause
            host/schemes for all customers to be returned.

        :return:
            Returns a dictionary of host/scheme instances indexed by
            host/scheme ID.  None is returned on error.

        :type customer_id: int or None
        :rtype:            dict or None

        """

        if customer_id is not None:
            message = { 'customer_id' : customer_id }
        else:
            message = dict()

        response = self.__rest_api.post_message(
            slug = "host_scheme/list",
            secret = self.__secret,
            message = message
        )

        if response is not None and 'status' in response:
            status = response['status']
            if status == 'OK' and 'data' in response:
                host_schemes_data = response['data']
                result = dict()
                for host_scheme_data in host_schemes_data.values():
                    if result is not None:
                        try:
                            host_scheme_id = int(
                                host_scheme_data['host_scheme_id']
                            )
                            customer_id = int(
                                host_scheme_data['customer_id']
                            )
                            url = host_scheme_data['url']
                            ssl_expiration_timestamp = int(
                                host_scheme_data['ssl_expiration_timestamp']
                            )
                        except Exception as e:
                            host_scheme_id = None
                            customer_id = None
                            url = None
                            ssl_expiration_timestamp = None

                        if host_scheme_id is not None:
                            (
                                scheme_string,
                                network_location,
                                path,
                                parameters,
                                query_fields,
                                fragment
                            ) = urllib.parse.urlparse(
                                url
                            )

                            try:
                                scheme = SCHEME.by_name(scheme_string.upper())
                            except:
                                print("C")
                                scheme = None

                            if scheme is not None:
                                host_scheme = HostScheme(
                                    host_scheme_id = host_scheme_id,
                                    customer_id = customer_id,
                                    host = network_location,
                                    scheme = scheme,
                                    ssl_expiration_timestamp = \
                                                       ssl_expiration_timestamp
                                )

                                result[host_scheme_id] = host_scheme
                            else:
                                print("D")
                                result = None
                        else:
                            result = None
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
