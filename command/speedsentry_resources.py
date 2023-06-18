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
Class providing a API you can use to process resource information.

"""

###############################################################################
# Import:
#

import sys

import libraries.resources as resources
import libraries.rest_api_common_v1 as rest_api_common_v1
import libraries.outbound_rest_api_v1 as outbound_rest_api_v1

###############################################################################
# Globals:
#

RESOURCES_BRIEF = "Allows you to add, list, purge, or plot resource data."
"""
Brief description for the resources command.

"""

RESOURCES_HELP = """
The resources command allows you add, list, purge, or plot resource data.  The
resources command supports the following subcommands:

  resources available <customer id>
    Lists what value types have assigned resource values.

  resources create <customer id> <value type> <value> [ <timestamp> ]
    Inserts a new resource entry.

  resources list <customer id> <value type>
                 [ <start timestamp> [ <end timestamp> ]]
    Lists resources data.

  resources purge <customer id> <timestamp>
    Purges resources based on a timestamp.

  resources plot [ <field> [ <value> ] [ <field> [ <value ]
               [ <field> [ <value> ... ]]]]
    Generates a plot of a resource.
"""
"""
Help text for this extension.

"""

RESOURCES_AVAILABLE_HELP = """
The resources available command allows you to add a new resources entry for a
type of value.   The syntax for the command is:

  resources available <customer id>

Where:
  <customer id> - The ID of the customer to query.

"""

RESOURCES_CREATE_HELP = """
The resources create command allows you to add a new resources entry for a
type of value.   The syntax for the command is:

  resources create <customer id> <value type> <value> [ <timestamp> ]

Where:
  <customer id> - The ID of the customer tied to the desired entry.

  <value type> -  The value type specified as an integer between 0 and 255,
                  inclusive.

  <value> -       The floating point value to be stored.

  <timestamp> -   The optional timestamp to assign to the value.  If not
                  specified, then now is used.

"""

RESOURCES_LIST_HELP = """
The resources list command allows you to list values for a given customer and
value type.  You can also constrain the time range for the values.

  resources list <customer id> <value type>
                 [ <start timestamp> [ <end timestamp> ]]

Where:
  <customer id> -     The ID of the customer tied to the desired entry.

  <value type> -      The value type specified as an integer between 0 and
                      255, inclusive.

  <start timestamp> - The earliest timestamp to include in the list, inclusive.

  <end timestamp> -   The latest timestamp to include in the list, inclusive.

"""

RESOURCES_PURGE_HELP = """
The resources purge command allows you to delete older than a given timestamp.
The syntax for the command is:

  resources purge <customer id> <timestamp>

Where:
  <customer id> - The ID of the customer to remove entries for.

  <timestamp> -   The timestamp to use as a threshold.

"""

RESOURCES_PLOT_HELP = """
The resources plot command allows you to obtain a plot of customer resource
data.  The syntax for the command is:

  resources plot [ <field> [ <value> ] [ <field> [ <value ]
               [ <field> [ <value> ... ]]]]

You can specify parameters using fields where most fields require a value.  The
supported fields are:

+-----------------+-----------------+-----------------------------------------+
| Field           | <value>         | Function                                |
+-----------------+-----------------+-----------------------------------------+
| title           | <title>         | The plot title.                         |
+-----------------+-----------------+-----------------------------------------+
| format          | <format>        | Indicates the format of the plot.       |
|                 |                 | Example values are "JPG" and "PNG".     |
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
| value_type      | <value type>    | The value type to be shown.             |
+-----------------+-----------------+-----------------------------------------+
| start           | <timestamp>     | The start timestamp to apply to the     |
|                 |                 | measurements.                           |
+-----------------+-----------------+-----------------------------------------+
| end             | <timestamp>     | The end timestamp to apply to the       |
|                 |                 | measurements.                           |
+-----------------+-----------------+-----------------------------------------+
| scale_factor    | <scale factor>  | The scale factor to apply to the Y      |
|                 |                 | axis.                                   |
+-----------------+-----------------+-----------------------------------------+
| width           | <width pixels>  | The plot width, in pixels.              |
+-----------------+-----------------+-----------------------------------------+
| height          | <height pixels> | The plot height, in pixels.             |
+-----------------+-----------------+-----------------------------------------+

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


def resources_available(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the resources available command.

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
    success = True
    if number_arguments == 1:
        try:
            customer_id = int(positional_arguments[0])
        except:
            sys.stderr.write("*** Invalid customer ID.\n")
            customer_id = None
            success = False

        if success:
            r = resources.Resources(rest_api, secret)
            value_types = r.available(customer_id)

            if value_types is not None:
                sys.stdout.write(str(value_types) + "\n")
            else:
                sys.stderr.write("*** Failed to add resource entry.\n")
    else:
        sys.stderr.write("*** Invalid number of arguments.\n")
        success = False

    return success


def resources_create(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the resources create command.

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
    success = True
    if number_arguments == 3 or number_arguments == 4:
        try:
            customer_id = int(positional_arguments[0])
        except:
            sys.stderr.write("*** Invalid customer ID.\n")
            customer_id = None
            success = False

        if success:
            try:
                value_type = int(positional_arguments[1])
            except:
                sys.stderr.write("*** Invalid value type.\n")
                value_type = None
                success = False

        if success:
            try:
                value = float(positional_arguments[2])
            except:
                sys.stderr.write("*** Invalid value.\n")
                value = None
                success = False

        if success and number_arguments == 4:
            try:
                timestamp = int(positional_arguments[3])
            except:
                sys.stderr.write("*** Invalid timestamp.\n")
                timestamp = None
                success = False
        else:
            timestamp = None

        if success:
            r = resources.Resources(rest_api, secret)
            success = r.create(customer_id, value_type, value, timestamp)

            if not success:
                sys.stderr.write("*** Failed to add resource entry.\n")
    else:
        sys.stderr.write("*** Invalid number of arguments.\n")
        success = False

    return success


def resources_list(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the region modify command.

    :param positional_arguments:
        The command line positional arguments.

    :param arguments:
        The command line arguments parsed by argparse.

    :param rest_api:
        The outbound REST API to use to communicate with Inesonic
        infrastructure.

    :return:
        Returns True on success.  Returns False on error.

    :type positional_arguments: list
    :type arguments:            argparse.Namespace
    :type rest_api:             outbound_rest_api_v1.Server
    :rtype:                     bool

    """

    success = True
    if len(positional_arguments) >= 2 and len(positional_arguments) <= 4:
        try:
            customer_id = int(positional_arguments[0])
        except:
            sys.stderr.write("*** Invalid customer ID.\n")
            customer_id = None
            success = False

        if success:
            try:
                value_type = int(positional_arguments[1])
            except:
                sys.stderr.write("*** Invalid value type.\n")
                value_type = None
                success = False

        if success:
            if len(positional_arguments) >= 3:
                try:
                    start_timestamp = int(positional_arguments[2])
                except:
                    sys.stderr.write("*** Invalid start timestamp.\n")
                    start_timestamp = None
                    success = False
            else:
                start_timestamp = None

        if success:
            if len(positional_arguments) >= 4:
                try:
                    end_timestamp = int(positional_arguments[2])
                except:
                    sys.stderr.write("*** Invalid end timestamp.\n")
                    end_timestamp = None
                    success = False
            else:
                end_timestamp = None

        if success:
            r = resources.Resources(rest_api, secret)
            result = r.list(
                customer_id = customer_id,
                value_type = value_type,
                start_timestamp = start_timestamp,
                end_timestamp = end_timestamp
            )

            if result is not None:
                resource_data = result['resources']
                for entry in resource_data:
                    v = entry['value']
                    ts = entry['timestamp']
                    sys.stdout.write("%10d\t%f\n"%(ts, v))
            else:
                sys.stderr.write("*** Failed to get resource data.\n")
                success = False
    else:
        sys.stderr.write("*** You must provide a region ID and region name.\n")
        success = False

    return success


def resources_purge(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the resources purge command.

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
    success = True
    if number_arguments == 2:
        try:
            customer_id = int(positional_arguments[0])
        except:
            sys.stderr.write("*** Invalid customer ID.\n")
            customer_id = None
            success = False

        if success:
            try:
                timestamp = int(positional_arguments[1])
            except:
                sys.stderr.write("*** Invalid timestamp.\n")
                timestamp = None
                success = False

        if success:
            r = resources.Resources(rest_api, secret)
            success = r.purge(customer_id, timestamp)

            if not success:
                sys.stderr.write("*** Failed to purge entries.\n")
    else:
        sys.stderr.write("*** Invalid number of arguments.\n")
        success = False

    return success


def resources_plot(positional_arguments, arguments, rest_api, secret):
    """
    Function that plots resources information.

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
        value_type = None
        start_timestamp = None
        end_timestamp = None
        scale_factor = None
        width = None
        height = None
        plot_title = None
        plot_format = None
        x_axis_label = None
        y_axis_label = None
        date_format = None
        output = None

        index = 0
        while success and index < number_arguments:
            field_name = positional_arguments[index].lower().replace('-', '_')
            parameter = positional_arguments[index + 1]

            if field_name == 'title':
                plot_title = parameter
                index += 2
            elif field_name == 'format':
                plot_format = parameter
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
                    elif field_name == 'value_type':
                        value_type = int(value)
                        index += 2
                    elif field_name == 'start':
                        start_timestamp = int(value)
                        index += 2
                    elif field_name == 'end':
                        end_timestamp = int(value)
                        index += 2
                    elif field_name == 'scale_factor':
                        scale_factor = float(value)
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
            r = resources.Resources(rest_api, secret)
            plot_data = r.plot(
                customer_id = customer_id,
                value_type = value_type,
                start_timestamp = start_timestamp,
                end_timestamp = end_timestamp,
                scale_factor = scale_factor,
                width = width,
                height = height,
                plot_title = plot_title,
                plot_format = plot_format,
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
        sys.stderr.write("*** Invalid number of parameters.\n")
        success = False

    return success

###############################################################################
# Extension configuration:
#

COMMANDS = {
    'resources' : {
        'brief' : RESOURCES_BRIEF,
        'help' : RESOURCES_HELP,
        'subcommands' : {
            'available' : {
                'help' : RESOURCES_AVAILABLE_HELP,
                'execute' : resources_available,
            },
            'create' : {
                'help' : RESOURCES_CREATE_HELP,
                'execute' : resources_create,
            },
            'list' : {
                'help' : RESOURCES_LIST_HELP,
                'execute' : resources_list,
            },
            'purge' : {
                'help' : RESOURCES_PURGE_HELP,
                'execute' : resources_purge,
            },
            'plot' : {
                'help' : RESOURCES_PLOT_HELP,
                'execute' : resources_plot,
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
