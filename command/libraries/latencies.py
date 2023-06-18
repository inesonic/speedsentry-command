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
Class providing a API you can use to process regions information.

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
import struct

import libraries.enumeration as enumeration
import libraries.servers as servers
import libraries.rest_api_common_v1 as rest_api_common_v1
import libraries.outbound_rest_api_v1 as outbound_rest_api_v1

###############################################################################
# Globals:
#

TIMESTAMP_OFFSET = 1609484400
"""
The time offset to apply to keep values within 32-bits.

"""

###############################################################################
# Class ShortLatency:
#

class ShortLatency(object):
    """
    Class that encapsulates information about a latency entry.

    """

    def __init__(self, timestamp, latency):
        """
        Method that holds a single latency entry.

        :param timestamp:
            The the Unix timestamp when the latency was measured.

        :param latency:
            The latency value, in seconds.

        :type timestamp: int
        :type latency:   float

        """

        super().__init__()

        self.__timestamp = timestamp
        self.__latency = latency


    @property
    def timestamp(self):
        """
        Read-only property that holds the timestamp

        :type: int

        """

        return self.__timestamp


    @property
    def latency(self):
        """
        Read-only property that holds the measured latency

        :type: float

        """

        return self.__latency

###############################################################################
# Class Latency:
#

class Latency(ShortLatency):
    """
    Class that encapsulates information about a latency entry.  This version
    includes the region ID.

    """

    def __init__(
        self,
        monitor_id,
        server_id,
        region_id,
        customer_id,
        timestamp,
        latency
        ):
        """
        Method that holds a single latency entry.

        :param monitor_id:
            The monitor ID of the monitor tied to this latency entry.

        :param server_id:
            The server ID of the server that took this measurement.

        :param region_id:
            The rgion ID of the region where the measurement was taken.

        :param customer_id:
            The customer ID of the customer associated with this monitor.

        :param timestamp:
            The the Unix timestamp when the latency was measured.

        :param latency:
            The latency value, in seconds.

        :type monitor_id:  int
        :type server_id:   int
        :type region_id:   int
        :type customer_id: int
        :type timestamp:   int
        :type latency:     float

        """

        ShortLatency.__init__(self, timestamp, latency)
        self.__monitor_id = monitor_id
        self.__server_id = server_id
        self.__region_id = region_id
        self.__customer_id = customer_id


    @property
    def monitor_id(self):
        """
        Read-only property that holds the monitor ID.

        :type: int

        """

        return self.__monitor_id


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
        Read-only property that holds the region ID.

        :type: int

        """

        return self.__region_id


    @property
    def customer_id(self):
        """
        Read-only property that holds the customer ID.

        :type: int

        """

        return self.__customer_id

###############################################################################
# Class AggregatedLatency:
#

class AggregatedLatency(Latency):
    """
    Class that encapsulates information about a latency entry.  This version
    includes the region ID.

    """

    def __init__(
        self,
        monitor_id,
        server_id,
        region_id,
        customer_id,
        timestamp,
        latency,
        mean_latency,
        variance_latency,
        minimum_latency,
        maximum_latency,
        start_timestamp,
        end_timestamp,
        number_samples
        ):
        """
        Method that holds a single agggregated latency entry.

        :param monitor_id:
            The monitor ID of the monitor tied to this latency entry.

        :param server_id:
            The server ID of the server that took this measurement.

        :param region_id:
            The rgion ID of the region where the measurement was taken.

        :param customer_id:
            The customer ID of the customer associated with this monitor.

        :param timestamp:
            The the Unix timestamp when the latency was measured.  This is the
            timestamp corresponding with the randomly selected latency value.

        :param latency:
            The latency value, in seconds.  This value is a randomly selected
            value from the population.

        :param mean_latency:
            The mean latency across this population in seconds.

        :param variance_latency:
            The variance in latency across the population, in seconds.

        :param minimum_latency:
            The minimum latency, in the population, in seconds.

        :param maximum_latency:
            The maximum latency, in the population, in seconds.

        :param start_timestamp:
            The oldest timestamp in the population.

        :param end_timestamp:
            The newest timestamp in the population.

        :param number_samples:
            The number of samples that existed in this population.

        :type monitor_id:       int
        :type server_id:        int
        :type region_id:        int
        :type customer_id:      int
        :type timestamp:        int
        :type latency:          float
        :type mean_latency:     float
        :type variance_latency: float
        :type minimum_latency:  float
        :type maximum_latency:  float
        :type start_timestamp:  int
        :type end_timestamp:    int
        :type number_samples:   int

        """

        Latency.__init__(
            self,
            monitor_id,
            server_id,
            region_id,
            customer_id,
            timestamp,
            latency
        )

        self.__mean_latency = mean_latency
        self.__variance_latency = variance_latency
        self.__minimum_latency = minimum_latency
        self.__maximum_latency = maximum_latency
        self.__start_timestamp = start_timestamp
        self.__end_timestamp = end_timestamp
        self.__number_samples = number_samples


    @property
    def mean_latency(self):
        """
        Read-only property that holds the average latency.

        :type: float

        """

        return self.__mean_latency


    @property
    def variance_latency(self):
        """
        Read-only property that holds the variance in latency.

        :type: float

        """

        return self.__variance_latency


    @property
    def minimum_latency(self):
        """
        Read-only property that holds the minimum latency.

        :type: float

        """

        return self.__minimum_latency


    @property
    def maximum_latency(self):
        """
        Read-only property that holds the maximum latency.

        :type: float

        """

        return self.__maximum_latency


    @property
    def start_timestamp(self):
        """
        Read-only property that holds the start timestamp.

        :type: int

        """

        return self.__start_timestamp


    @property
    def end_timestamp(self):
        """
        Read-only property that holds the end timestamp.

        :type: int

        """

        return self.__end_timestamp


    @property
    def number_samples(self):
        """
        Read-only property that holds the number of samples that existed in
        this population.

        :type: int

        """

        return self.__number_samples

###############################################################################
# Class Latencies:
#

class Latencies(object):
    """
    Class that can be used to manage latency data.

    """

    def __init__(self, rest_api, secret):
        """
        Method that initializes the Latencies class.

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


    def record(
        self,
        ipv4_address,
        ipv6_address,
        server_status,
        cpu_loading,
        memory_loading,
        number_monitors,
        entries
        ):
        """
        Method you can use to obtain a latency by latency ID.

        :param ipv4_address:
            The server IPv4 address.

        :param ipv6_address:
            The server IPv6 address.

        :param server_status:
            The server status to report.

        :param cpu_loading:
            The CPU loading to report.  Value should range between 0 and 1.

        :param memory_loading:
            The memory loading to report.  Value should range between 0 and 1.

        :param number_monitors:
            The number of monitors this server is handling.

        :param entries:
            An list of latency entries to be recorded.

        :return:
            Returns True on success.  Returns False on error.

        :type ipv4_address:    str
        :type ipv6_address:    str
        :type server_status:   servers.STATUS
        :type cpu_loading:     float
        :type memory_loading:  float
        :type number_monitors: int
        :rtype:                bool

        """

        ipv4_data = bytearray(ipv4_address.encode('utf-8'))
        assert(len(ipv4_data) < 16)

        ipv6_data = bytearray(ipv6_address.encode('utf-8'))
        assert(len(ipv6_data) < 16)

        if server_status == servers.STATUS.ALL_UNKNOWN:
            server_status_code = 0
        elif server_status == servers.STATUS.ACTIVE:
            server_status_code = 1
        elif server_status == servers.STATUS.INACTIVE:
            server_status_code = 2
        elif server_status == servers.STATUS.DEFUNCT:
            server_status_code = 3
        else:
            assert(False)

        payload = (
              ipv4_data + b'\x00' * (16 - len(ipv4_data))
            + ipv6_data + b'\x00' * (40 - len(ipv6_data))
            + struct.pack(
                "BBBBI",
                server_status_code,
                int(255 * cpu_loading),
                int(255 * memory_loading),
                0,
                int(number_monitors)
            )
        )

        assert(len(payload) == 64)

        for latency_entry in entries:
            print(latency_entry.timestamp - TIMESTAMP_OFFSET)
            entry_payload = struct.pack(
                "III",
                latency_entry.monitor_id,
                latency_entry.timestamp - TIMESTAMP_OFFSET,
                int(0.5 + 1000000 * latency_entry.latency)
            )

            assert(len(entry_payload) == 12)

            payload += entry_payload

        response = self.__rest_api.post_binary_message(
            slug = "latency/record",
            secret = self.__secret,
            message = bytes(payload)
        )

        result = (
                response is not None
            and 'status' in response
            and response['status'] == 'OK'
        )

        return result


    def get(
        self,
        customer_id = None,
        monitor_id = None,
        server_id = None,
        region_id = None,
        start_timestamp = None,
        end_timestamp = None
        ):
        """
        Method you can use to get latency information.

        :param customer_id:
            The customer ID of the desired customer.  A value of None indicates
            all customers.  Note that you should specify customer_id or
            monitor_id, never both.

        :param monitor_id:
            The monitor ID of the desired customer.  A value of None indicates
            all monitors.  Note that you should specify customer_id or
            monitor_id, never both.

        :param server_id:
            The server ID of the server that triggered the request.  A value of
            None indicates all servers.  Note that you should specify server_id
            or region_id, never both.

        :param region_id:
            The region ID of the server(s) that triggered the request.  A value
            of None indicates all regions.  Note that you should specify
            server_id or region_id, never both.

        :param start_timestamp:
            The start timestamp for the entries.  A value of None indicates the
            earliest entries are desired.

        :param end_timestmap:
            The end timestamp for the entries.  A value of None indicates now.

        :return:
            Returns either a tuple containing the raw latency entries followed
            by the longer term aggregated entries or None if an error occurred.

        :type customer_id:     int or None
        :type monitor_id:      int or None
        :type server_id:       int or None
        :type region_id:       int or None
        :type start_timestamp: int or None
        :type end_timestamp:   int or None
        :rtype:                tuple or None

        """

        message = {}
        if customer_id is not None:
            message['customer_id'] = customer_id

        if monitor_id is not None:
            message['monitor_id'] = monitor_id

        if server_id is not None:
            message['server_id'] = server_id

        if region_id is not None:
            message['region_id'] = region_id

        if start_timestamp is not None:
            message['start_timestamp'] = start_timestamp

        if end_timestamp is not None:
            message['end_timestamp'] = end_timestamp

        response = self.__rest_api.post_message(
            slug = "latency/get",
            secret = self.__secret,
            message = message
        )

        if response is not None and 'status' in response:
            status = response['status']
            if status == 'OK'           and \
               'recent' in response     and \
               'aggregated' in response     :
                recent_entries = response['recent']
                aggregated_entries = response['aggregated']

                raw_data = list()
                for entry in recent_entries:
                    try:
                        monitor_id = int(entry['monitor_id'])
                        server_id = int(entry['server_id'])
                        region_id = int(entry['region_id'])
                        customer_id = int(entry['customer_id'])
                        timestamp = int(entry['timestamp'])
                        latency = float(entry['latency'])
                    except:
                        monitor_id = None
                        server_id = None
                        region_id = None
                        customer_id = None
                        timestamp = None
                        latency = None

                    latency_entry = Latency(
                        monitor_id = monitor_id,
                        server_id = server_id,
                        region_id = region_id,
                        customer_id = customer_id,
                        timestamp = timestamp,
                        latency = latency
                    )

                    raw_data.append(latency_entry)

                aggregated_data = list()
                for entry in aggregated_entries:
                    try:
                        monitor_id = int(entry['monitor_id'])
                        server_id = int(entry['server_id'])
                        region_id = int(entry['region_id'])
                        customer_id = int(entry['customer_id'])
                        timestamp = int(entry['timestamp'])
                        latency = float(entry['latency'])
                        average = float(entry['average'])
                        variance = float(entry['variance'])
                        minimum = float(entry['minimum'])
                        maximum = float(entry['maximum'])
                        number_samples = int(entry['number_samples'])
                        start_timestamp = int(entry['start_timestamp'])
                        end_timestamp = int(entry['end_timestamp'])
                    except:
                        monitor_id = None
                        server_id = None
                        region_id = None
                        customer_id = None
                        timestamp = None
                        latency = None
                        average = None
                        variance = None
                        minimum = None
                        maximum = None
                        number_samples = None
                        start_timestamp = None
                        end_timestamp = None

                    latency_entry = AggregatedLatency(
                        monitor_id = monitor_id,
                        server_id = server_id,
                        region_id = region_id,
                        customer_id = customer_id,
                        timestamp = timestamp,
                        latency = latency,
                        mean_latency = average,
                        variance_latency = variance,
                        minimum_latency = minimum,
                        maximum_latency = maximum,
                        start_timestamp = start_timestamp,
                        end_timestamp = end_timestamp,
                        number_samples = number_samples
                    )

                    aggregated_data.append(latency_entry)

                result = ( raw_data, aggregated_data )
            else:
                result = None
        else:
            result = None

        return result


    def purge(self, customers):
        """
        Method you can use to purge latency information for one or more
        customers.

        :param customers:
            The list of customer IDs for customers to be purged.

        :return:
            Returns True on success.  Returns False on error.

        :type customers: list of int
        :rtype:          bool

        """

        response = self.__rest_api.post_message(
            slug = "latency/purge",
            secret = self.__secret,
            message = customers
        )

        return (
                response is not None
            and 'status' in response
            and response['status'] == 'OK'
        )


    def plot(
        self,
        customer_id = None,
        monitor_id = None,
        server_id = None,
        region_id = None,
        start_timestamp = None,
        end_timestamp = None,
        minimum_latency = None,
        maximum_latency = None,
        log_scale = None,
        width = None,
        height = None,
        plot_title = None,
        plot_format = None,
        plot_type = None,
        x_axis_label = None,
        y_axis_label = None,
        date_format = None
        ):
        """
        Method you can use to get a latency plot.

        :param customer_id:
            The customer ID of the desired customer.  A value of None indicates
            all customers.  Note that you should specify customer_id or
            monitor_id, never both.

        :param monitor_id:
            The monitor ID of the desired customer.  A value of None indicates
            all monitors.  Note that you should specify customer_id or
            monitor_id, never both.

        :param server_id:
            The server ID of the server that triggered the request.  A value of
            None indicates all servers.  Note that you should specify server_id
            or region_id, never both.

        :param region_id:
            The region ID of the server(s) that triggered the request.  A value
            of None indicates all regions.  Note that you should specify
            server_id or region_id, never both.

        :param start_timestamp:
            The start timestamp for the entries.  A value of None indicates the
            earliest entries are desired.

        :param end_timestmap:
            The end timestamp for the entries.  A value of None indicates now.

        :param minimum_latency:
            The minimum latency, in seconds.

        :param maximum_latency:
            The maximum latency, in seconds.

        :param log_scale:
            If True, latency values will be shown on a log scale.  If False, a
            linear scale will be used.

        :param width:
            The desired plot width, in pixels.

        :param height:
            The desired plot height, in pixels.

        :param plot_title:
            The title text to use for the plot.

        :param plot_format:
            The desired plot format.

        :param plot_type:
            The desired plot type.  Supported values are "history" and
            "histogram".

        :param x_axis_label:
            The X axis label.

        :param y_axis_label:
            The Y axis label.

        :param date_format:
            The date format to apply.

        :return:
            Returns either a tuple containing the raw latency entries followed
            by the longer term aggregated entries or None if an error occurred.

        :type customer_id:      int or None
        :type monitor_id:       int or None
        :type server_id:        int or None
        :type region_id:        int or None
        :type start_timestamp:  int or None
        :type end_timestamp:    int or None
        :param minimum_latency: float or None
        :param maximum_latency: float or None
        :param log_scale:       bool or None
        :param width:           int or None
        :param height:          int or None
        :param plot_title:      str or None
        :param plot_format:     str or None
        :param plot_type:       str or None
        :param x_axis_label:    str or None
        :param y_axis_label:    str or None
        :param date_format:     str or None
        :rtype:                 tuple or None

        """

        message = {}
        if customer_id is not None:
            message['customer_id'] = customer_id

        if monitor_id is not None:
            message['monitor_id'] = monitor_id

        if server_id is not None:
            message['server_id'] = server_id

        if region_id is not None:
            message['region_id'] = region_id

        if start_timestamp is not None:
            message['start_timestamp'] = start_timestamp

        if end_timestamp is not None:
            message['end_timestamp'] = end_timestamp

        if minimum_latency is not None:
            message['minimum_latency'] = minimum_latency

        if maximum_latency is not None:
            message['maximum_latency'] = maximum_latency

        if log_scale is not None:
            message['log_scale'] = log_scale

        if width is not None:
            message['width'] = width

        if height is not None:
            message['height'] = height

        if plot_title is not None:
            message['title'] = plot_title

        if plot_format is not None:
            message['format'] = plot_format

        if plot_type is not None:
            message['plot_type'] = plot_type

        if x_axis_label is not None:
            message['x_axis_label'] = x_axis_label

        if y_axis_label is not None:
            message['y_axis_label'] = y_axis_label

        if date_format is not None:
            message['date_format'] = date_format

        binary_message = json.dumps(message)
        result = self.__rest_api.post_binary_message(
            slug = "latency/plot",
            secret = self.__secret,
            message = binary_message.encode('utf-8')
        )

        return result


    def statistics(
        self,
        customer_id = None,
        monitor_id = None,
        server_id = None,
        region_id = None,
        start_timestamp = None,
        end_timestamp = None
        ):
        """
        Method you can use to get latency statistical information.

        :param customer_id:
            The customer ID of the desired customer.  A value of None indicates
            all customers.  Note that you should specify customer_id or
            monitor_id, never both.

        :param monitor_id:
            The monitor ID of the desired customer.  A value of None indicates
            all monitors.  Note that you should specify customer_id or
            monitor_id, never both.

        :param server_id:
            The server ID of the server that triggered the request.  A value of
            None indicates all servers.  Note that you should specify server_id
            or region_id, never both.

        :param region_id:
            The region ID of the server(s) that triggered the request.  A value
            of None indicates all regions.  Note that you should specify
            server_id or region_id, never both.

        :param start_timestamp:
            The start timestamp for the entries.  A value of None indicates the
            earliest entries are desired.

        :param end_timestmap:
            The end timestamp for the entries.  A value of None indicates now.

        :return:
            Returns a dictionary containing latency statistics information or
            None if an error occurred.

        :type customer_id:     int or None
        :type monitor_id:      int or None
        :type server_id:       int or None
        :type region_id:       int or None
        :type start_timestamp: int or None
        :type end_timestamp:   int or None
        :rtype:                tuple or None

        """

        message = {}
        if customer_id is not None:
            message['customer_id'] = customer_id

        if monitor_id is not None:
            message['monitor_id'] = monitor_id

        if server_id is not None:
            message['server_id'] = server_id

        if region_id is not None:
            message['region_id'] = region_id

        if start_timestamp is not None:
            message['start_timestamp'] = start_timestamp

        if end_timestamp is not None:
            message['end_timestamp'] = end_timestamp

        response = self.__rest_api.post_message(
            slug = "latency/statistics",
            secret = self.__secret,
            message = message
        )

        if response is not None and 'status' in response:
            status = response['status']
            if status == 'OK' and 'statistics' in response:
                result = response['statistics']
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
