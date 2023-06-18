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
Class providing a API you can use to process resources information.

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

import libraries.rest_api_common_v1 as rest_api_common_v1
import libraries.outbound_rest_api_v1 as outbound_rest_api_v1

###############################################################################
# Class Resources:
#

class Resources(object):
    """
    Class that can be used to manage server regions.

    """

    def __init__(self, rest_api, secret):
        """
        Method that initializes the Regions class.

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


    def available(self, customer_id):
        """
        Method you can use to determine what resource entries are available for
        a given customer.

        :param customer_id:
            The ID of customer of interest.

        :param value_type:
            The value type represented as an integer value.

        :param value:
            The value to add for this resource.

        :param timestamp:
            Am optional timestamp to assign to this entry.

        :return:
            Returns a list of value types or None on error.

        :type customer_id: int
        :type value_type:  int
        :type value:       float
        :type timestamp:   int
        :rtype:            bool

        """

        response = self.__rest_api.post_message(
            slug = "resource/available",
            secret = self.__secret,
            message = { 'customer_id' : customer_id }
        )

        if response is not None       and \
           'status' in response       and \
           'value_types' in response  and \
           response['status'] == 'OK'     :
            result = response['value_types']
        else:
            result = None

        return result


    def create(self, customer_id, value_type, value, timestamp = None):
        """
        Method you can use to write a new resources data entry.

        :param customer_id:
            The ID of customer of interest.

        :param value_type:
            The value type represented as an integer value.

        :param value:
            The value to add for this resource.

        :param timestamp:
            Am optional timestamp to assign to this entry.

        :return:
            Returns True on success or False on error.

        :type customer_id: int
        :type value_type:  int
        :type value:       float
        :type timestamp:   int
        :rtype:            bool

        """

        if timestamp is None:
            timestamp = int(time.time())

        response = self.__rest_api.post_message(
            slug = "resource/create",
            secret = self.__secret,
            message = {
                'customer_id' : customer_id,
                'value_type' : value_type,
                'value' : value,
                'timestamp' : timestamp
            }
        )

        return (
                response is not None
            and 'status' in response
            and response['status'] == 'OK'
        )


    def list(
        self,
        customer_id,
        value_type,
        start_timestamp = None,
        end_timestamp = None
        ):
        """
        Method you can use to list resource values.

        :param customer_id:
            The ID of customer of interest.

        :param value_type:
            The value type represented as an integer value.

        :param start_timestamp:
            The start timestamp.  A value of None means no explicit start
            timestamp.

        :param end_timestamp:
            The end timestamp.  A value of None means no explicit end
            timestamp.

        :return:
            Returns a dictionary holding the result data.

        :type customer_id:     int
        :type value_type:      int
        :type start_timestamp: int or None
        :type end_timestamp:   int or None
        :rtype:                dict

        """

        message = {
            'customer_id' : customer_id,
            'value_type' : value_type
        }

        if start_timestamp is not None:
            message['start_timestamp'] = start_timestamp

        if end_timestamp is not None:
            message['end_timestamp'] = end_timestamp

        response = self.__rest_api.post_message(
            slug = "resource/list",
            secret = self.__secret,
            message = message
        )

        if response is not None and 'status' in response:
            status = response['status']
            if status == 'OK' and 'data' in response:
                result = response['data']
            else:
                result = None
        else:
            result = None

        return result


    def purge(self, customer_id, timestamp):
        """
        Method you can use to purge old resource data entries.

        :param customer_id:
            The customer ID of the customer to purge entries for.

        :param timestamp:
            The timestamp providing a threshold for purging.

        :return:
            Returns True on success.  Returns False on error.

        :type customer_id: int
        :type timestamp:   int
        :rtype:            bool

        """

        response = self.__rest_api.post_message(
            slug = "resource/purge",
            secret = self.__secret,
            message = {
                'customer_id' : customer_id,
                'timestamp' : timestamp
            }
        )


        return (
                response is not None
            and 'status' in response
            and response['status'] == 'OK'
        )


    def plot(
        self,
        customer_id = None,
        value_type = None,
        start_timestamp = None,
        end_timestamp = None,
        scale_factor = None,
        width = None,
        height = None,
        plot_title = None,
        plot_format = None,
        x_axis_label = None,
        y_axis_label = None,
        date_format = None
        ):
        """
        Method you can use to get a resource plot.

        :param customer_id:
            The customer ID of the desired customer.  A value of None indicates
            all customers.  Note that you should specify customer_id or
            monitor_id, never both.

        :param value_type:
            The value type of the value to be plotted.  A value of None
            indicates the default value type.

        :param start_timestamp:
            The start timestamp for the entries.  A value of None indicates the
            earliest entries are desired.

        :param end_timestmap:
            The end timestamp for the entries.  A value of None indicates now.

        :param scale_factor:
            The scale factor to apply to the vertical axis.

        :param width:
            The desired plot width, in pixels.

        :param height:
            The desired plot height, in pixels.

        :param plot_title:
            The title text to use for the plot.

        :param plot_format:
            The desired plot format.

        :param x_axis_label:
            The X axis label.

        :param y_axis_label:
            The Y axis label.

        :param date_format:
            The date format to apply.

        :return:
            Returns either a tuple containing the raw latency entries followed
            by the longer term aggregated entries or None if an error occurred.

        :type customer_id:     int or None
        :type value_type:      int or None
        :type start_timestamp: int or None
        :type end_timestamp:   int or None
        :type scale_factor:    float or None
        :type width:           int or None
        :type height:          int or None
        :type plot_title:      str or None
        :type plot_format:     str or None
        :type x_axis_label:    str or None
        :type y_axis_label:    str or None
        :type date_format:     str or None
        :rtype:                tuple or None

        """

        message = {}
        if customer_id is not None:
            message['customer_id'] = customer_id

        if value_type is not None:
            message['value_type'] = value_type

        if start_timestamp is not None:
            message['start_timestamp'] = start_timestamp

        if end_timestamp is not None:
            message['end_timestamp'] = end_timestamp

        if scale_factor is not None:
            message['scale_factor'] = scale_factor

        if width is not None:
            message['width'] = width

        if height is not None:
            message['height'] = height

        if plot_title is not None:
            message['title'] = plot_title

        if plot_format is not None:
            message['format'] = plot_format

        if x_axis_label is not None:
            message['x_axis_label'] = x_axis_label

        if y_axis_label is not None:
            message['y_axis_label'] = y_axis_label

        if date_format is not None:
            message['date_format'] = date_format

        binary_message = json.dumps(message)
        result = self.__rest_api.post_binary_message(
            slug = "resource/plot",
            secret = self.__secret,
            message = binary_message.encode('utf-8')
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
