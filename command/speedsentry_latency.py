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
Class providing a API you can use to process latencies information.

"""

###############################################################################
# Import:
#

import sys
import json

import libraries.latencies as latencies
import libraries.servers as servers
import libraries.rest_api_common_v1 as rest_api_common_v1
import libraries.outbound_rest_api_v1 as outbound_rest_api_v1

###############################################################################
# Globals:
#

LATENCY_BRIEF = "Allows you to record and view monitor latency data."
"""
Brief description for the latency command.

"""

LATENCY_HELP = """
The latency command allows you to manipulate latencies.  The latency command
supports the following subcommands:

  latency record <ipv4 address> <ipv6 address>
                 <server status> <cpu loading> <memory loading>
                 <number monitors> <records file>
    Records latency information from a given server.

  latency get <field> <value> [ <field> <value> [ <field> <value> ... ]]
    Obtains raw latency data.

  latency purge <customer id> [ <customer id> [ <customer id> ... ]]
    Deletes latency information for one or more customers.

  latency plot [ <field> [ <value> ] [ <field> [ <value ]
               [ <field> [ <value> ... ]]]]
    Generates either a plot of latency over time or a latency histogram.

  latency statistics <field> <value> [ <field> <value> [ <field> <value> ... ]]
    Obtains statistics on latency over a time frame.

"""
"""
Help text for this extension.

"""

LATENCY_RECORD_HELP = """
The latency record command allows you to record latency information as if
reported by a specific polling server.  The syntax for the command is:

  latency record <ipv4 address> <ipv6 address>
                 <server status> <cpu loading> <memory loading>
                 <number monitors> <records file>

Where:
  <ipv4 address> - Is the IPv4 address of the server.  An empty string should
                   be used if the server has no recorded IPv4 address.

  <ipv6 address> - Is the IPv6 address of the server.  An empty string should
                   be used if the server has no recorded IPv6 address.

  <server status> - Holds the server status.  Values should be one of
                    "active", "inactive", or "defunct".

  <cpu loading> - The CPU loading to report.  Value should range between 0 and
                  1.0 (inclusive).

  <memory loading> - The memory loading to report.  Value should range between
                     0 and 1.0 (inclusive).

  <number monitors> - The number of monitors currently managed by this server.

  <records file> - A file containing a whitespace separated list of entries to
                   be reported.  Each line contains a single record.  Fields
                   should be ordered as monitor ID, Unix timestamp, latency
                   in seconds.

"""
"""
Help text for this extension.

"""

LATENCY_GET_HELP = """
The latency get command allows you to obtain raw latency information.  The
syntax for the command is:

  latency get <field> <value> [ <field> <value> [ <field> <value> ... ]]

Where the <field> <value> entries are pairs used to constraint the latency
data.  Value values are:

+----------+-----------------+------------------------------------------------+
| Field    | Value           | Purpose                                        |
+==========+=================+================================================+
| Customer | customer_id     | Specifies a single customer to fetch all       |
|          |                 | latency values for.  This field is mutually    |
|          |                 | exclusive with "monitor".                      |
+----------+-----------------+------------------------------------------------+
| monitor  | monitor_id      | Specifies a single monitor to fetch all        |
|          |                 | latency values for.  This field is mutually    |
|          |                 | exclusive with "customer".                     |
+----------+-----------------+------------------------------------------------+
| server   | server_id       | Specifies a specific server to fetch latency   |
|          |                 | values for.  This field is mutually exclusive  |
|          |                 | with "region".                                 |
+----------+-----------------+------------------------------------------------+
| region   | region_id       | Specifies a specific region to fetch latency   |
|          |                 | values for.  This field is mutually exclusive  |
|          |                 | with "server".                                 |
+----------+-----------------+------------------------------------------------+
| start    | start_timestamp | Specifies a start Unix timestamp for the       |
|          |                 | latency values.                                |
+----------+-----------------+------------------------------------------------+
| end      | end timestamp   | Specifies an end Unix timestamp for the        |
|          |                 | latency values.                                |
+----------+-----------------+------------------------------------------------+

"""
"""
Help text for this extension.

"""

LATENCY_PURGE_HELP = """
The latency purge command allows you to delete latency information for multiple
customers at once in an efficient manner.

  latency purge <customer id> [ <customer id> [ <customer id> ... ]]

"""
"""
Help text for this extension.

"""

LATENCY_PLOT_HELP = """
The latency plot command allows you to plot latency information either over
time or as a histogram.  The syntax for the command is:

  latency plot [ <field> [ <value> ] [ <field> [ <value ]
               [ <field> [ <value> ... ]]]]

You can specify parameters using fields where most fields require a value.  The
supported fields are:

+-----------------+-----------------+-----------------------------------------+
| Field           | <value>         | Function                                |
+-----------------+-----------------+-----------------------------------------+
| log             | - none -        | Indicates a logarithmic scale for       |
|                 |                 | latency. This setting is ignored for    |
|                 |                 | histograms.                             |
+-----------------+-----------------+-----------------------------------------+
| linear          | - none -        | Indicates a linear scale for latency.   |
|                 |                 | This setting is ignored for histograms. |
+-----------------+-----------------+-----------------------------------------+
| title           | <title>         | The plot title.                         |
+-----------------+-----------------+-----------------------------------------+
| format          | <format>        | Indicates the format of the plot.       |
|                 |                 | Example values are "JPG" and "PNG".     |
+-----------------+-----------------+-----------------------------------------+
| type            | <type>          | The type of plot to generate.  Accepted |
|                 |                 | values are "history" and "histogram".   |
+-----------------+-----------------+-----------------------------------------+
| x_axis_label    | <label>         | The X axis label text.                  |
+-----------------+-----------------+-----------------------------------------+
| y_axis_label    | <label>         | The Y axis label text.                  |
+-----------------+-----------------+-----------------------------------------+
| date_format     | <date format>   | The date format string.                 |
+-----------------+-----------------+-----------------------------------------+
| output          | <filename>      | The output filename.                    |
+-----------------+-----------------+-----------------------------------------+
| customer        | <customer id>   | The customer ID used to limit monitors. |
+-----------------+-----------------+-----------------------------------------+
| monitor         | <monitor id>    | The monitor ID used to specify a        |
|                 |                 | specific monitor.                       |
+-----------------+-----------------+-----------------------------------------+
| server          | <server id>     | The server ID of the server that took   |
|                 |                 | the latency measurements.               |
+-----------------+-----------------+-----------------------------------------+
| region          | <region id>     | The region ID of the region where the   |
|                 |                 | measurement was taken.                  |
+-----------------+-----------------+-----------------------------------------+
| start           | <timestamp>     | The start timestamp to apply to the     |
|                 |                 | measurements.                           |
+-----------------+-----------------+-----------------------------------------+
| end             | <timestamp>     | The end timestamp to apply to the       |
|                 |                 | measurements.                           |
+-----------------+-----------------+-----------------------------------------+
| minimum_latency | <latency sec>   | The minimum latency value to show.      |
|                 |                 | Value is in seconds.                    |
+-----------------+-----------------+-----------------------------------------+
| maximum_latency | <latency sec>   | The maximum latency value to show.      |
|                 |                 | Value is in seconds.                    |
+-----------------+-----------------+-----------------------------------------+
| width           | <width pixels>  | The plot width, in pixels.              |
+-----------------+-----------------+-----------------------------------------+
| height          | <height pixels> | The plot height, in pixels.             |
+-----------------+-----------------+-----------------------------------------+

"""
"""
Help text for this extension.

"""

LATENCY_STATISTICS_HELP = """
The latency get command allows you to obtain statistics about latency over a
given time period and/or other limiting factors.  The syntax for the command
is:

  latency statistics <field> <value> [ <field> <value> [ <field> <value> ... ]]

Where the <field> <value> entries are pairs used to constraint the latency
data.  Value values are:

+----------+-----------------+------------------------------------------------+
| Field    | Value           | Purpose                                        |
+==========+=================+================================================+
| Customer | customer_id     | Specifies a single customer to fetch all       |
|          |                 | latency values for.  This field is mutually    |
|          |                 | exclusive with "monitor".                      |
+----------+-----------------+------------------------------------------------+
| monitor  | monitor_id      | Specifies a single monitor to fetch all        |
|          |                 | latency values for.  This field is mutually    |
|          |                 | exclusive with "customer".                     |
+----------+-----------------+------------------------------------------------+
| server   | server_id       | Specifies a specific server to fetch latency   |
|          |                 | values for.  This field is mutually exclusive  |
|          |                 | with "region".                                 |
+----------+-----------------+------------------------------------------------+
| region   | region_id       | Specifies a specific region to fetch latency   |
|          |                 | values for.  This field is mutually exclusive  |
|          |                 | with "server".                                 |
+----------+-----------------+------------------------------------------------+
| start    | start_timestamp | Specifies a start Unix timestamp for the       |
|          |                 | latency values.                                |
+----------+-----------------+------------------------------------------------+
| end      | end timestamp   | Specifies an end Unix timestamp for the        |
|          |                 | latency values.                                |
+----------+-----------------+------------------------------------------------+

"""
"""
Help text for this extension.

"""

###############################################################################
# Functions:
#

def add_arguments(command_line_parser):
    """
    Function you can use to add additional arguments to the command line
    parser.

    :param command_line_parser:
        The command line parser to be modified.

    :type command_line_parser: argparse.ArgumentParser

    """

    pass


def latency_record(positional_arguments, arguments, rest_api, secret):
    """
    Function that records latency information.

    :param positional_arguments:
        The command line positional arguments.

    :param arguments:
        The command line arguments parsed by argparse.

    :param rest_api:
        The outbound REST API to use to communicate with Inesonic
        infrastructure.

    :param secret:
        The secret required to use the Inesonic REST API.

    :return:
        Returns True on success.  Returns False on error.

    :type positional_arguments: list
    :type arguments:            argparse.Namespace
    :type rest_api:             outbound_rest_api_v1.Server
    :type secret:               bytes
    :rtype:                     bool

    """

    success = True
    if len(positional_arguments) == 7:
        try:
            ipv4_address = str(positional_arguments[0])
            ipv6_address = str(positional_arguments[1])
            server_status = servers.STATUS.by_name(
                positional_arguments[2].upper().replace('-','_')
            )
            cpu_loading = float(positional_arguments[3])
            memory_loading = float(positional_arguments[4])
            number_monitors = int(positional_arguments[5])
            records_file = str(positional_arguments[6])
        except Exception as e:
            success = False
            sys.stderr.write("*** Invalid parameter.\n")

        if success:
            if cpu_loading >= 0 and cpu_loading <= 1       and \
               memory_loading >= 0 and memory_loading <= 1 and \
               number_monitors >= 0                            :
                entries = list()
                with open(records_file, 'r') as fh:
                    line_number = 0
                    for l in fh.readlines():
                        line_number += 1

                        if success:
                            line = l.strip()
                            fields = line.split()
                            try:
                                monitor_id = int(fields[0])
                                timestamp = int(0.5 + float(fields[1]))
                                latency = float(fields[2])
                            except:
                                success = False
                                sys.stderr.write(
                                    "*** Invalid record, line %d: $s\n"%(
                                        line_number,
                                        line
                                    )
                                )

                        if success:
                            entries.append(
                                latencies.Latency(
                                    monitor_id = monitor_id,
                                    server_id = None,
                                    region_id = None,
                                    customer_id = None,
                                    timestamp = timestamp,
                                    latency = latency
                                )
                            )
                if success:
                    l = latencies.Latencies(rest_api, secret)
                    success = l.record(
                        ipv4_address = ipv4_address,
                        ipv6_address = ipv6_address,
                        server_status = server_status,
                        cpu_loading = cpu_loading,
                        memory_loading = memory_loading,
                        number_monitors = number_monitors,
                        entries = entries
                    )

                    if not success:
                        sys.stderr.write(
                            "*** Failed to record latency data.\n"
                        )
            else:
                sys.stderr.write("*** Invalid server parameter.\n")
                success = False
    else:
        sys.stderr.write("*** You must provide at least one latency ID.\n")
        success = False

    return success


def latency_get(positional_arguments, arguments, rest_api, secret):
    """
    Function that gets latency data.

    :param positional_arguments:
        The command line positional arguments.

    :param arguments:
        The command line arguments parsed by argparse.

    :param rest_api:
        The outbound REST API to use to communicate with Inesonic
        infrastructure.

    :param secret:
        The secret required to use the Inesonic REST API.

    :return:
        Returns True on success.  Returns False on error.

    :type positional_arguments: list
    :type arguments:            argparse.Namespace
    :type rest_api:             outbound_rest_api_v1.Server
    :type secret:               bytes
    :rtype:                     bool

    """

    number_arguments = len(positional_arguments)
    if (number_arguments % 2) == 0:
        customer_id = None
        monitor_id = None
        server_id = None
        region_id = None
        start_timestamp = None
        end_timestamp = None

        success = True
        index = 0
        while success and index < number_arguments:
            field = positional_arguments[index + 0].lower()
            try:
                value = int(positional_arguments[index + 1])
            except:
                success = False
                sys.stderr.write(
                    "*** Invalid argument \"%s\".\n"%(
                        positional_arguments[index + 1]
                    )
                )

            if success:
                if field == 'customer':
                    customer_id = value
                elif field == 'monitor':
                    monitor_id = value
                elif field == 'server':
                    server_id = value
                elif field == 'region':
                    region_id = value
                elif field == 'start':
                    start_timestamp = value
                elif field == 'end':
                    end_timestamp = value
                else:
                    success = False
                    sys.stderr.write(
                        "*** Invalid field \"%s\".\n"%(
                            positional_arguments[index + 0]
                        )
                    )

            index += 2

        if success:
            l = latencies.Latencies(rest_api, secret)
            result = l.get(
                customer_id = customer_id,
                monitor_id = monitor_id,
                server_id = server_id,
                region_id = region_id,
                start_timestamp = start_timestamp,
                end_timestamp = end_timestamp
            )

            if result is not None:
                __dump(result[0], result[1])
            else:
                sys.stderr.write("*** Failed to retrieve latency data.\n")
                success = False
    else:
        sys.stderr.write("*** You must provide at least one latency name.\n")
        success = False

    return success


def latency_purge(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the latency purge command.

    :param positional_arguments:
        The command line positional arguments.

    :param arguments:
        The command line arguments parsed by argparse.

    :param rest_api:
        The outbound REST API to use to communicate with Inesonic
        infrastructure.

    :param secret:
        The secret required to use the Inesonic REST API.

    :return:
        Returns True on success.  Returns False on error.

    :type positional_arguments: list
    :type arguments:            argparse.Namespace
    :type rest_api:             outbound_rest_api_v1.Server
    :type secret:               bytes
    :rtype:                     bool

    """

    success = True
    if len(positional_arguments) >= 1:
        customer_list = list()
        for argument in positional_arguments:
            if success:
                try:
                    customer_id = int(argument)
                except:
                    customer_id = None

            if customer_id is not None and customer_id > 0:
                customer_list.append(customer_id)
            else:
                sys.stderr.write(
                    "*** Invalid customer ID \"%s\".\n"%argument
                )
                success = False
    else:
        sys.stderr.write(
            "*** Must specify at least one customer ID.\n"
        )

    if success:
        l = latencies.Latencies(rest_api, secret)
        success = l.purge(customer_list)

        if not success:
            sys.stderr.write("*** Failed to purge customer data.\n")

    return success


def latency_plot(positional_arguments, arguments, rest_api, secret):
    """
    Function that plot latency information.

    :param positional_arguments:
        The command line positional arguments.

    :param arguments:
        The command line arguments parsed by argparse.

    :param rest_api:
        The outbound REST API to use to communicate with Inesonic
        infrastructure.

    :param secret:
        The secret required to use the Inesonic REST API.

    :return:
        Returns True on success.  Returns False on error.

    :type positional_arguments: list
    :type arguments:            argparse.Namespace
    :type rest_api:             outbound_rest_api_v1.Server
    :type secret:               bytes
    :rtype:                     bool

    """

    success = True
    number_arguments = len(positional_arguments)
    if number_arguments % 2 == 0:
        customer_id = None
        monitor_id = None
        server_id = None
        region_id = None
        start_timestamp = None
        end_timestamp = None
        minimum_latency = None
        maximum_latency = None
        log_scale = None
        width = None
        height = None
        plot_title = None
        plot_format = None
        plot_type = None
        x_axis_label = None
        y_axis_label = None
        date_format = None
        output = None

        index = 0
        while success and index < number_arguments:
            field_name = positional_arguments[index].lower().replace('-', '_')
            if field_name == 'log':
                log_scale = True
                index += 1
            elif field_name == 'linear':
                log_scale = False
                index += 1
            else:
                parameter = positional_arguments[index + 1]

                if field_name == 'title':
                    plot_title = parameter
                    index += 2
                elif field_name == 'format':
                    plot_format = parameter
                    index += 2
                elif field_name == 'type':
                    plot_type = parameter
                    index += 2
                elif field_name == 'x_axis_label':
                    x_axis_label = parameter
                    index += 2
                elif field_name == 'y_axis_label':
                    y_axis_label = parameter
                    index += 2
                elif field_name == 'date_format':
                    date_format = parameter
                    index += 2
                elif field_name == 'output':
                    output = parameter
                    index += 2
                else:
                    try:
                        value = float(parameter)
                    except:
                        sys.stderr.write(
                            "*** Invalid parameter value.\n"
                        )
                        success = False

                    if success:
                        if field_name == 'customer':
                            customer_id = int(value)
                            index += 2
                        elif field_name == 'monitor':
                            monitor_id = int(value)
                            index += 2
                        elif field_name == 'server':
                            server_id = int(value)
                            index += 2
                        elif field_name == 'region':
                            region_id = int(value)
                            index += 2
                        elif field_name == 'start':
                            start_timestamp = int(value)
                            index += 2
                        elif field_name == 'end':
                            end_timestamp = int(value)
                            index += 2
                        elif field_name == 'minimum_latency':
                            minimum_latency = value
                            index += 2
                        elif field_name == 'maximum_latency':
                            maximum_latency = value
                            index += 2
                        elif field_name == 'width':
                            width = int(value)
                            index += 2
                        elif field_name == 'height':
                            height = int(value)
                            index += 2
                        else:
                            success = False
                            sys.stderr.write(
                                "*** Invalid parameter name.\n"
                            )

        if success:
            l = latencies.Latencies(rest_api, secret)
            plot_data = l.plot(
                customer_id = customer_id,
                monitor_id = monitor_id,
                server_id = server_id,
                region_id = region_id,
                start_timestamp = start_timestamp,
                end_timestamp = end_timestamp,
                minimum_latency = minimum_latency,
                maximum_latency = maximum_latency,
                log_scale = log_scale,
                width = width,
                height = height,
                plot_title = plot_title,
                plot_format = plot_format,
                plot_type = plot_type,
                x_axis_label = x_axis_label,
                y_axis_label = y_axis_label,
                date_format = date_format
            )

            if output is None:
                if plot_format is None:
                    output = 'plot.png'
                else:
                    output = 'plot.' + plot_format.lower()

            with open(output, 'w+b') as fh:
                fh.write(plot_data)
    else:
        sys.stderr.write("*** You must provide at least one latency ID.\n")
        success = False

    return success


def latency_statistics(positional_arguments, arguments, rest_api, secret):
    """
    Function that gets latency statistics.

    :param positional_arguments:
        The command line positional arguments.

    :param arguments:
        The command line arguments parsed by argparse.

    :param rest_api:
        The outbound REST API to use to communicate with Inesonic
        infrastructure.

    :param secret:
        The secret required to use the Inesonic REST API.

    :return:
        Returns True on success.  Returns False on error.

    :type positional_arguments: list
    :type arguments:            argparse.Namespace
    :type rest_api:             outbound_rest_api_v1.Server
    :type secret:               bytes
    :rtype:                     bool

    """

    number_arguments = len(positional_arguments)
    if (number_arguments % 2) == 0:
        customer_id = None
        monitor_id = None
        server_id = None
        region_id = None
        start_timestamp = None
        end_timestamp = None

        success = True
        index = 0
        while success and index < number_arguments:
            field = positional_arguments[index + 0].lower()
            try:
                value = int(positional_arguments[index + 1])
            except:
                success = False
                sys.stderr.write(
                    "*** Invalid argument \"%s\".\n"%(
                        positional_arguments[index + 1]
                    )
                )

            if success:
                if field == 'customer':
                    customer_id = value
                elif field == 'monitor':
                    monitor_id = value
                elif field == 'server':
                    server_id = value
                elif field == 'region':
                    region_id = value
                elif field == 'start':
                    start_timestamp = value
                elif field == 'end':
                    end_timestamp = value
                else:
                    success = False
                    sys.stderr.write(
                        "*** Invalid field \"%s\".\n"%(
                            positional_arguments[index + 0]
                        )
                    )

            index += 2

        if success:
            l = latencies.Latencies(rest_api, secret)
            result = l.statistics(
                customer_id = customer_id,
                monitor_id = monitor_id,
                server_id = server_id,
                region_id = region_id,
                start_timestamp = start_timestamp,
                end_timestamp = end_timestamp
            )

            if result is not None:
                print(json.dumps(result, indent = 4))
            else:
                sys.stderr.write("*** Failed to retrieve latency data.\n")
                success = False
    else:
        sys.stderr.write("*** You must provide at least one latency name.\n")
        success = False

    return success


def __dump(raw_data, aggregated_data):
    """
    Method that dumps latency data.

    :param raw_data:
        The raw, most recent latency data.

    :param aggregated_data:
        The older aggregated data.

    :type raw_data:        list
    :type aggregated_data: list

    """

    divider_string = "+-------------+------------+-----------+-----------" \
                     "+------------+---------+---------+----------+---------" \
                     "+---------+------------+------------+----------------+\n"

    sys.stdout.write(divider_string)
    sys.stdout.write(
        "| customer_id | monitor_id | server_id | region_id | timestamp  | "
        "latency | average | variance | minimum | maximum | start_time | "
        "end_time   | number samples |\n"
    )
    sys.stdout.write(
        "+=============+============+===========+===========+============+"
        "=========+=========+==========+=========+=========+============+"
        "============+================+\n"
    )

    aggregated_format = "| %%11d | %%10d | %%9d | %%9d | %%10d | %%7.3f | " \
                        "%%7.3f | %%8.3f | %%7.3f | %%7.3f | %%10d | " \
                        "%%10d | %%14d |\n"

    for entry in raw_data:
        sys.stdout.write(
            "| %11d | %10d | %9d | %9d | %10d | %7.3f "
            "|         |          |         |         |            |"
            "            |                |\n"%(
                entry.customer_id,
                entry.monitor_id,
                entry.server_id,
                entry.region_id,
                entry.timestamp,
                entry.latency
            )
        )
        sys.stdout.write(divider_string)

    for entry in aggregated_data:
        sys.stdout.write(
            "| %11d | %10d | %9d | %9d | %10d | %7.3f | "
            "%7.3f | %8.3f | %7.3f | %7.3f | %10d | "
            "%10d | %14d |\n"%(
                entry.customer_id,
                entry.monitor_id,
                entry.server_id,
                entry.region_id,
                entry.timestamp,
                entry.latency,
                entry.mean_latency,
                entry.variance_latency,
                entry.minimum_latency,
                entry.maximum_latency,
                entry.start_timestamp,
                entry.end_timestamp,
                entry.number_samples
            )
        )
        sys.stdout.write(divider_string)

###############################################################################
# Extension configuration:
#

COMMANDS = {
    'latency' : {
        'brief' : LATENCY_BRIEF,
        'help' : LATENCY_HELP,
        'subcommands' : {
            'record' : {
                'help' : LATENCY_RECORD_HELP,
                'execute' : latency_record
            },
            'get' : {
                'help' : LATENCY_GET_HELP,
                'execute' : latency_get
            },
            'purge' : {
                'help' : LATENCY_PURGE_HELP,
                'execute' : latency_purge
            },
            'plot' : {
                'help' : LATENCY_PLOT_HELP,
                'execute' : latency_plot
            },
            'statistics' : {
                'help' : LATENCY_STATISTICS_HELP,
                'execute' : latency_statistics
            }
        }
    }
}

ADD_ARGUMENTS = add_arguments

###############################################################################
# Main:
#

if __name__ == "__main__":
    import sys
    sys.stderr.write(
        "*** This module is not intended to be run as a script..\n"
    )
    exit(1)
