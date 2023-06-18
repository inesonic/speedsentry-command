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
Class providing a API you can use to manage monitors information.

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

METHOD = enumeration.Enum("HEAD GET POST PUT DELETE OPTIONS PATCH")
"""
The supported HTTP access methods.

"""

CONTENT_CHECK_MODE = enumeration.Enum("""
    NO_CHECK
    CONTENT_MATCH
    ANY_KEYWORDS
    ALL_KEYWORDS
    SMART_CONTENT_MATCH
""")
"""
Support content match states.

"""

CONTENT_TYPE = enumeration.Enum("JSON XML TEXT")
"""
The supported POST content type values.

"""

###############################################################################
# Class MonitorEntry:
#

class MonitorEntry(object):
    """
    Class that tracks information required to update a monitor.

    """

    def __init__(
        self,
        user_ordering = None,
        path = None,
        method = METHOD.GET,
        content_check_mode = CONTENT_CHECK_MODE.NO_CHECK,
        keywords = list(),
        content_type = CONTENT_TYPE.TEXT,
        user_agent = str(),
        post_content = str()
        ):
        """
        Method that initializes the MonitorEntry class.

        :param user_ordering:
            The user ordering in the user interface.

        :param path:
            The actual path string under the host and scheme.

        :param method:
            The method to be used to access this monitor.

        :param content_check_mode:
            The mode to be applied to check content.

        :param keywords:
            The list of keywords to be tied to this monitor.

        :param content_type:
            The content-type to report in the POST header.

        :param user_agent:
            The user agent to report in the POST header.

        :param post_content:
            The content to send with the POST request.

        :type user_ordering:      int
        :type path:               str
        :type method:             monitors.METHOD enumerated value.
        :type content_check_mode: monitors.CONTENT_CHECK_MODE enumerated value.
        :type keywords:           list of str
        :type content_type:       monitors.CONTENT_TYPE enumerated value.
        :type user_agent:         str
        :type post_content:       str

        """

        super().__init__()

        self.__user_ordering = user_ordering
        self.__path = path
        self.__method = method
        self.__content_check_mode = content_check_mode
        self.__keywords = keywords
        self.__content_type = content_type
        self.__user_agent = user_agent
        self.__post_content = post_content


    @property
    def user_ordering(self):
        """
        Property that holds the user_ordering.

        :type: int

        """

        return self.__user_ordering


    @user_ordering.setter
    def user_ordering(self, value):
        self.__user_ordering = int(value)


    @property
    def path(self):
        """
        Property that holds the path under the host and scheme.

        :type: int

        """

        return self.__path


    @path.setter
    def path(self, value):
        self.__path = str(value)


    @property
    def method(self):
        """
        Property that holds the URL access method.

        :type: int

        """

        return self.__method


    @method.setter
    def method(self, value):
        self.__method = value


    @property
    def content_check_mode(self):
        """
        Property that holds the monitor content check mode.

        :type: int

        """

        return self.__content_check_mode


    @content_check_mode.setter
    def content_check_mode(self, value):
        self.__content_check_mode = value


    @property
    def keywords(self):
        """
        Property that holds the keywords used for content checking.

        :type: int

        """

        return self.__keywords


    @keywords.setter
    def keywords(self, value):
        self.__keywords = value


    @property
    def content_type(self):
        """
        Property that holds the content type enumerated value.

        :type: monitors.CONTENT_TYPE enumerated value.

        """

        return self.__content_type


    @content_type.setter
    def content_type(self, value):
        self.__content_type = value


    @property
    def user_agent(self):
        """
        Property that holds the user agent string.

        :type: str

        """

        return self.__user_agent


    @user_agent.setter
    def user_agent(self, value):
        self.__user_agent = str(value)


    @property
    def post_content(self):
        """
        Property that holds the actual post content to be sent.

        :type: str

        """

        return self.__post_content


    @post_content.setter
    def post_content(self, value):
        self.__post_content = value


    def as_dictionary(self):
        return {
            'user_ordering' : self.__user_ordering,
            'path' : self.__path,
            'method' : str(self.__method),
            'content_check_mode' : str(self.__content_check_mode),
            'keywords' : [
                k.decode('utf-8', errors = 'backslashreplace')
                for k in self.__keywords
            ],
            'content_type' : str(self.__content_type),
            'user_agent' : self.__user_agent,
            'post_content' : self.__post_content.decode(
                'utf-8',
                errors = 'backslashreplace'
            )
        }

###############################################################################
# Class Monitor:
#

class Monitor(MonitorEntry):
    """
    Class that tracks information related to a monitor.

    """

    def __init__(
        self,
        monitor_id = None,
        customer_id = None,
        host_scheme_id = None,
        user_ordering = None,
        path = None,
        method = METHOD.GET,
        content_check_mode = CONTENT_CHECK_MODE.NO_CHECK,
        keywords = list(),
        content_type = CONTENT_TYPE.TEXT,
        user_agent = str(),
        post_content = str()
        ):
        """
        Method that initializes the Monitor class.

        :param monitor_id:
            The monitor ID that uniquely identifies this entry.

        :param customer_id:
            The customer ID of the customer associated with this monitor.

        :param host_scheme_id:
            The HostScheme ID indicating the host related to this monitor.

        :param user_ordering:
            The user ordering in the user interface.

        :param path:
            The actual path string under the host and scheme.

        :param method:
            The method to be used to access this monitor.

        :param content_check_mode:
            The mode to be applied to check content.

        :param keywords:
            The list of keywords to be tied to this monitor.

        :param content_type:
            The content-type to report in the POST header.

        :param user_agent:
            The user agent to report in the POST header.

        :param post_content:
            The content to send with the POST request.

        :type monitor_id:         int
        :type customer_id:        int
        :type host_scheme_id:     int
        :type user_ordering:      int
        :type path:               str
        :type method:             monitors.METHOD enumerated value.
        :type content_check_mode: monitors.CONTENT_CHECK_MODE enumerated value.
        :type keywords:           list of str
        :type content_type:       monitors.CONTENT_TYPE enumerated value.
        :type user_agent:         str
        :type post_content:       str

        """

        MonitorEntry.__init__(
            self,
            user_ordering = user_ordering,
            path = path,
            method = method,
            content_check_mode = content_check_mode,
            keywords = keywords,
            content_type = content_type,
            user_agent = user_agent,
            post_content = post_content
        )

        self.__monitor_id = monitor_id
        self.__customer_id = customer_id
        self.__host_scheme_id = host_scheme_id


    @property
    def monitor_id(self):
        """
        Property that holds the monitor ID.

        :type: int

        """

        return self.__monitor_id


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
    def host_scheme_id(self):
        """
        Property that holds the host/scheme ID.

        :type: int

        """

        return self.__host_scheme_id


    @host_scheme_id.setter
    def host_scheme_id(self, value):
        self.__host_scheme_id = int(value)


    def as_dictionary(self):
        v = MonitorEntry.as_dictionary(self)
        v['monitor_id'] = self.__monitor_id
        v['customer_id'] = self.__customer_id
        v['host_scheme_id'] = self.__host_scheme_id

        return v

###############################################################################
# Class Monitors:
#

class Monitors(object):
    """
    Class that can be used to manage customer Monitors data.

    """

    def __init__(self, rest_api, secret):
        """
        Method that initializes the Monitors class.

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


    def get(self, monitor_id):
        """
        Method you can use to obtain a specific monitor instance by monitor ID.

        :param monitor_id:
            The monitor ID to obtain.

        :return:
            Returns a Monitor instance holding the requested monitor instance.
            A value of None is returned on error.

        :type monitor_id: int
        :rtype:           Monitor or None

        """

        response = self.__rest_api.post_message(
            slug = "monitor/get",
            secret = self.__secret,
            message = { 'monitor_id' : monitor_id }
        )

        if response is not None and 'status' in response:
            status = response['status']
            if status == 'OK' and 'monitor' in response:
                monitor_data = response['monitor']
                result = self.__convert_to_monitor(monitor_data)
            else:
                result = None
        else:
            result = None

        return result


    def delete(self, monitor):
        """
        Method you can use to delete a monitor.  If this is the only monitor
        associated with a given host/scheme, then the host/scheme will also be
        deleted.

        :param monitor:
            The monitor to be deleted.

        :return:
            Returns True on success.  Returns False on error.

        :type monitor: Monitor
        :rtype:        bool

        """

        response = self.__rest_api.post_message(
            slug = "monitor/delete",
            secret = self.__secret,
            message = {
                'monitor_id' : monitor.monitor_id
            }
        )

        result = (
                response is not None
            and 'status' in response
            and response['status'] == 'OK'
        )

        return result


    def purge(self, customer_id):
        """
        Method you can use to delete all monitors, and by extension,
        host/schemes tied to a specific customer.

        Use this method with care.

        :param customer_id:
            The customer to have associated monitor information deleted.

        :return:
            Returns true on success.  Returns false on error.

        :type server: Server
        :rtype:       bool

        """

        response = self.__rest_api.post_message(
            slug = "monitor/delete",
            secret = self.__secret,
            message = { 'customer_id' : customer_id }
        )

        result = (
                response is not None
            and 'status' in response
            and response['status'] == 'OK'
        )

        return result


    def list(self, customer_id = None):
        """
        Method you can use to obtain a list of monitors.

        :param customer_id:
            An optional customer ID used to constraint the list to only
            monitors to a single customer.  A value of None will cause
            monitors for all customers to be returned.

        :return:
            if customer_id is None, then this method returns a dictionary
            of monitor instances indexed by monitor ID.  If customer_id is
            not None, then this method returns a list of monitor instances
            indexed by user ordering.  The list will contain null entries
            where no monitor was defined.

        :type customer_id: int or None
        :rtype:            list or None

        """

        if customer_id is not None:
            message = { 'customer_id' : customer_id }
        else:
            message = dict()

        response = self.__rest_api.post_message(
            slug = "monitor/list",
            secret = self.__secret,
            message = message
        )

        if response is not None and 'status' in response:
            status = response['status']
            if status == 'OK' and 'data' in response:
                monitors_data = response['data']
                if customer_id is None:
                    result = dict()
                    for user_ordering, monitor_data in monitors_data.items():
                        monitor_data['user_ordering'] = user_ordering
                        m = self.__convert_to_monitor(monitor_data)
                        result[m.monitor_id] = m
                else:
                    result_dict = dict()
                    highest_user_ordering = -1
                    for user_ordering, monitor_data in monitors_data.items():
                        monitor_data['user_ordering'] = user_ordering
                        m = self.__convert_to_monitor(monitor_data)
                        result_dict[m.user_ordering] = m

                        highest_user_ordering = max(
                            highest_user_ordering,
                            m.user_ordering
                        )

                    result = list()
                    for user_ordering in range(highest_user_ordering + 1):
                        if user_ordering in result_dict:
                            result.append(result_dict[user_ordering])
                        else:
                            result.append(None)
            else:
                result = None
        else:
            result = None

        return result


    def update(self, customer_id, update_data):
        """
        Method you can use to update monitors and host/schemes tied to a given
        customer.

        :param customer_id:
            The customer ID of the customer to be updated.

        :param update_data:
            A dictionary holding monitor updates.

        :return:
            Returns an empty list on success.  On false, returns a list of
            tuples containing an user ordering value and error message for
            each issue found.

        :type customer_id: int or None
        :type update_data: dict
        :rtype:            dict or None

        """

        response = self.__rest_api.post_message(
            slug = "monitor/update",
            secret = self.__secret,
            message = {
                'customer_id' : customer_id,
                'data' : update_data
            }
        )

        if response is not None and 'status' in response:
            status = response['status']
            if status == 'OK':
                result = list()
            elif 'errors' in response:
                error_data = response['errors']
                result = list()
                for entry in error_data:
                    user_ordering = entry['user_ordering']
                    error_message = entry['text']
                    if user_ordering == 0xFFFF:
                        result.append( ( None, error_message ) )
                    else:
                        result.append( ( user_ordering, error_message ) )
            else:
                result = [ ( None, "unexpected response" ) ]
        else:
            result = [ ( None, "unexpected response" ) ]

        return result


    def __convert_to_monitor(self, returned_data):
        """
        Method used internally to convert a response to a Monitor instance.

        :param returned_data:
            A dictionary holding the returned data.

        :return:
            Returns the monitor data or None on error.

        :type returned_data: dict
        :rtype:              Monitor or None

        """

        try:
            monitor_id = int(returned_data['monitor_id'])
            customer_id = int(returned_data['customer_id'])
            host_scheme_id = int(returned_data['host_scheme_id'])
            user_ordering = int(returned_data['user_ordering'])
            path = str(returned_data['path'])
            method = METHOD.by_name(returned_data['method'].upper())
            content_check_mode = CONTENT_CHECK_MODE.by_name(
                returned_data['content_check_mode'].upper()
            )
            encoded_keywords = list(returned_data['keywords'])
            content_type = CONTENT_TYPE.by_name(
                returned_data['post_content_type']
            )
            user_agent = str(returned_data['post_user_agent'])
            encoded_post_content = str(returned_data['post_content'])
        except:
            monitor_id = None
            customer_id = None
            host_scheme_id = None
            user_ordering = None
            path = None
            method = None
            content_check_mode = None
            encoded_keywords = None
            content_type = None
            user_agent = None
            encoded_post_content = None

        if monitor_id is not None:
            try:
                keywords = [ base64.standard_b64decode(k)
                             for k in encoded_keywords
                           ]
            except:
                keywords = None

            if keywords is not None:
                try:
                    post_content = base64.b64decode(
                        encoded_post_content,
                        validate = True
                    )
                except:
                    post_content = None

                if post_content is not None:
                    result = Monitor(
                        monitor_id = monitor_id,
                        customer_id = customer_id,
                        host_scheme_id = host_scheme_id,
                        user_ordering = user_ordering,
                        path = path,
                        method = method,
                        content_check_mode = content_check_mode,
                        keywords = keywords,
                        content_type = content_type,
                        user_agent = user_agent,
                        post_content = post_content
                    )
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
