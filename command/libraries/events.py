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
Class providing a API you can use to process events information.

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
# Class Globals:
#

EVENT_TYPE = enumeration.Enum("""
    INVALID
    WORKING
    NO_RESPONSE
    CONTENT_CHANGED
    KEYWORDS
    SSL_CERTIFICATE_EXPIRING
    SSL_CERTIFICATE_RENEWED
    CUSTOMER_1
    CUSTOMER_2
    CUSTOMER_3
    CUSTOMER_4
    CUSTOMER_5
    CUSTOMER_6
    CUSTOMER_7
    CUSTOMER_8
    CUSTOMER_9
    CUSTOMER_10
    TRANSACTION
    INQUIRY
    SUPPORT_REQUEST
    STORAGE_LIMIT_REACHED
""")
"""
Enumeration of supported event types.

"""

MONITOR_STATUS = enumeration.Enum("UNKNOWN FAILED WORKING")
"""
Enumeration of supported monitor status values.

"""

###############################################################################
# Class Event:
#

class Event(object):
    """
    Class that encapsulates information about a single event.

    """

    def __init__(
        self,
        event_id,
        monitor_id,
        customer_id,
        timestamp,
        event_type
        ):
        """
        Method that initializes the Event instance.

        :param event_id:
            The event ID for this event.

        :param monitor_id:
            The monitor that triggered this event.

        :param customer_id:
            The customer ID of the customer owning the monitor.

        :param timestamp:
            The Unix timestamp indicating when the event occurred.

        :param event_type:
            The type of event that occurred.

        :type event_id:    int
        :type monitor_id:  int
        :type customer_id: int
        :type timestamp:   int
        :type event_type:  EVENT_TYPE enumerated value

        """

        super().__init__()

        self.__event_id = int(event_id)
        self.__monitor_id = int(monitor_id)
        self.__customer_id = int(customer_id)
        self.__timestamp = int(timestamp)
        self.__event_type = event_type


    @property
    def event_id(self):
        """
        Read-only property that holds the event ID.

        :type: int

        """

        return self.__event_id


    @property
    def monitor_id(self):
        """
        Property that holds the monitor ID.

        :type: int

        """

        return self.__monitor_id


    @monitor_id.setter
    def monitor_id(self, value):
        self.__monitor_id = int(monitor_id)


    @property
    def customer_id(self):
        """
        Property that holds the customer ID.

        :type: int

        """

        return self.__customer_id


    @customer_id.setter
    def customer_id(self, value):
        self.__customer_id = int(customer_id)


    @property
    def timestamp(self):
        """
        Property that holds the timestamp.

        :type: int

        """

        return self.__timestamp


    @timestamp.setter
    def timestamp(self, value):
        self.__timestamp = int(timestamp)


    @property
    def event_type(self):
        """
        Property that holds the event_type.

        :type: int

        """

        return self.__event_type


    @event_type.setter
    def event_type(self, value):
        self.__event_type = int(event_type)

###############################################################################
# Class Events:
#

class Events(object):
    """
    Class that can be used to manage events.

    """

    def __init__(self, rest_api, secret):
        """
        Method that initializes the Events class.

        :param rest_api:
            The outbound REST API instance to be used.

        :param secret:
            The secret to be used.

        :type server: outbound_rest_api_v1.Server
        :type secret: bytes

        """

        super().__init__()

        self.__rest_api = rest_api
        self.__secret = secret


    def report(
        self,
        monitor_id,
        page_hash,
        event_type,
        monitor_status,
        message,
        timestamp
        ):
        """
        Method you can use to report a new event.

        :param monitor_id:
            The ID of the monitor that triggered this event.

        :param page_hash:
            The page hash for the content that triggered this event.

        :param event_type:
            The type of event detected.

        :param monitor_status:
            The current monitor status.

        :param message:
            An optional message to be sent.

        :param timestamp:
            The Unix timestamp indicating when the event occurred.

        :return:
            Returns True on success or False on error.

        :type monitor_id:     int
        :type page_hash:      bytes
        :type timestamp:      int
        :type event_type:     EVENT_TYPE enumerated value
        :type monitor_status: MONITOR_STATUS enumerated value
        :rtype:               bool

        """

        response = self.__rest_api.post_message(
            slug = "event/report",
            secret = self.__secret,
            message = {
                'monitor_id' : int(monitor_id),
                'hash' : base64.b64encode(page_hash).decode('utf-8'),
                'message' : message,
                'event_type' : str(event_type).lower(),
                'monitor_status' : str(monitor_status).lower(),
                'timestamp' : int(timestamp)
            }
        )

        return (
                response is not None
            and 'status' in response
            and response['status'] == 'OK'
        )


    def status(self, customer_id = None, monitor_id = None):
        """
        Method you can use to get the status of one or more monitors.

        :param customer_id:
            The customer ID to get events for.  The provided monitor_id
            parameter must be None if this parameter is set.

        :param monitor_id:
            The monitor ID to get events for.  The provided customer_id
            parameter must be None if this parameter is set.

        :return:
            Returns a dictionary of status values by monitor ID.  A value of
            None is returned on error.

        :type customer_id: int or None
        :type monitor_id:  int or None:
        :rtype:            dict or None

        """

        message = dict()
        if customer_id is not None:
            message['customer_id'] = int(customer_id)

        if monitor_id is not None:
            message['monitor_id'] = int(monitor_id)

        response = self.__rest_api.post_message(
            slug = "event/status",
            secret = self.__secret,
            message = message
        )

        if response is not None and 'status' in response:
            status = response['status']
            if status == 'OK' and 'monitors' in response:
                monitor_status = response['monitors']
                result = { int(i) : MONITOR_STATUS.by_name(k.upper())
                           for i, k in monitor_status.items()
                         }
            else:
                result = None
        else:
            result = None

        return result


    def get(
        self,
        customer_id = None,
        monitor_id = None,
        start_timestamp = None,
        end_timestamp = None
        ):
        """
        Method you can use to get information about events.

        :param customer_id:
            The customer ID to get events for.  The provided monitor_id
            parameter must be None if this parameter is set.

        :param monitor_id:
            The monitor ID to get events for.  The provided customer_id
            parameter must be None if this parameter is set.

        :param start_timestamp:
            The starting Unix timestamp to get information over.  Values are
            inclusive.  A value of None indicates all values.

        :param end_timestamp:
            The ending Unix timestamp to get information over.  Values are
            inclusive.  A value of None indicates now.

        :return:
            Returns a list of Event entries of None on error.

        :type customer_id:     int or None
        :type monitor_id:      int or None
        :type start_timestamp: int or None
        :type end_timestamp:   int or None
        :rtype:                list or None

        """

        message = dict()
        if customer_id is not None:
            message['customer_id'] = int(customer_id)

        if monitor_id is not None:
            message['monitor_id'] = int(monitor_id)

        if start_timestamp is not None:
            message['start_timestamp'] = int(start_timestamp)

        if end_timestamp is not None:
            message['end_timestamp'] = int(end_timestamp)


        response = self.__rest_api.post_message(
            slug = "event/get",
            secret = self.__secret,
            message = message
        )

        if response is not None and 'status' in response:
            status = response['status']
            if status == 'OK' and 'events' in response:
                events_data = response['events']
                result = list()
                for event_data in events_data:
                    event = self.__parse_event(event_data)
                    result.append(event)
            else:
                result = None
        else:
            result = None

        return result


    def __parse_event(self, event_data):
        """
        Method used internally to parse an event.

        :param event_data:
            A dictionary holding the returned event data.

        :return:
            Returns an Event instance or None on error.

        :type event_data: dict
        :rtype:           Event or None

        """

        try:
            event_id = int(event_data['event_id'])
            monitor_id = int(event_data['monitor_id'])
            customer_id = int(event_data['customer_id'])
            timestamp = int(event_data['timestamp'])
            event_type = EVENT_TYPE.by_name(event_data['event_type'].upper())
        except:
            event_id = None
            monitor_id = None
            timestamp = None
            event_type = None

        if event_id is not None:
            result = Event(
                event_id,
                monitor_id,
                customer_id,
                timestamp,
                event_type
            )
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
