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
Class providing a API you can use to process monitors information.

"""

###############################################################################
# Import:
#

import sys
import yaml

import libraries.host_schemes as host_schemes
import libraries.monitors as monitors
import libraries.rest_api_common_v1 as rest_api_common_v1
import libraries.outbound_rest_api_v1 as outbound_rest_api_v1

###############################################################################
# Globals:
#

MONITOR_BRIEF = "Allows you to view and modify customer monitors."
"""
Brief description for the monitor command.

"""

MONITOR_HELP = """
The monitor command allows you to directly view and manipulate customer
monitors.  The monitor command supports the following subcommands:

  monitor get <monitor id> [ <monitor id> [ <monitor id> ... ]]
    Gets monitor data by internal ID.

  monitor delete <monitor id>
    Deletes a monitor by monitor ID.

  monitor purge <customer id>
    Purges all the monitors and host/schemes tied to a specific customer.

  monitor list [ <customer id> ]
    Lists monitors.  If you specify a customer ID then only monitors for that
    customer will be shown.

  monitor update (yaml|json) <customer id> <filename>
    Reads a monitor definition from a YAML or JSON description.

"""
"""
Help text for this extension.

"""

MONITOR_GET_HELP = """
The monitor get command allows you to view information regarding one or more
monitors instances.  The syntax for the command is:

  monitor get <monitor id> [ <monitor id> [ <monitor id> ]]

Where <monitor id> is an internal monitor ID.

The data will be presented in YAML format.

"""
"""
Help text for this extension.

"""

MONITOR_DELETE_HELP = """
The monitor delete command allows you to delete a single monitor from the
system.  If, after deleting a monitor, no monitors are tied to the same
host/scheme, the host/scheme entry will also be deleted.

  monitor delete <monitor id>

"""
"""
Help text for this extension.

"""

MONITOR_PURGE_HELP = """
The hs purge command allows you to delete all monitors, and, by extension,
host/schemes associated with a specific user.

  monitor purge <customer id>

"""
"""
Help text for this extension.

"""

MONITOR_LIST_HELP = """
The monitor list command allows you to list monitors.  You can optionally
constrain the list to only show monitors for a single customer by specifying
the customer ID.

  monitor list [ <customer id> ]

"""
"""
Help text for this extension.

"""

MONITOR_UPDATE_HELP = """
The monitor update command allows you to update monitors for a specific
customer.  You must specify the monitors using either a YAML or JSON
description.

  monitor update (yaml|json) <customer id> <filename>

Where (yaml|json) indicates the file format, <customer id> indicates the ID of
the customer to be updated and <filename> is the file holding the description.

The description should be defined as a dictionary keyed by the placement in
the user interface.  Each dictionary entry should also be a dictionary holding
the following fields:

+--------------------+-------------+------------------------------------------+
| Field              | Default     | Purpose And Supported Values             |
+====================+=============+==========================================+
| uri                |             | The URI to use for the monitor.  If the  |
|                    |             | URI is relative, then the host and       |
|                    |             | scheme from the previous monitor, based  |
|                    |             | on the ordering value supplied by the    |
|                    |             | key will be used.                        |
|                    |             |                                          |
|                    |             | Note that this field is required.        |
+--------------------+-------------+------------------------------------------+
| method             | get         | The method used to access the endpoint   |
|                    |             | specified by the URI.  Accepted values   |
|                    |             | are "get" or "post".                     |
+--------------------+-------------+------------------------------------------+
| content_check_mode | no_check    | Specifies if the content returned by the |
|                    |             | endpoint should be checked.  Supported   |
|                    |             | values are "no_check", "content_match",  |
|                    |             | "any_keywords", and "all_keywords"       |
+--------------------+-------------+------------------------------------------+
| keywords           | no keywords | A list of keywords to check for.  The    |
|                    |             | field is only used if the content check  |
|                    |             | mode is "any_keywords" or                |
|                    |             | "all_keywords".  Each value should be    |
|                    |             | base64 encoded as per RFC4648.           |
+--------------------+-------------+------------------------------------------+
| post_content_type  | text        | The content type to report when sending  |
|                    |             | a HTTP POST.  The value is ignored if    |
|                    |             | an HTTP GET is used.  Supported values   |
|                    |             | are "text", "json", and "xml".           |
+--------------------+-------------+------------------------------------------+
| post_user_agent    | InesonicBot | The uer agent string to send during      |
|                    |             | HTTP POST messages.  The value is        |
|                    |             | ignored for HTTP GET messages.           |
+--------------------+-------------+------------------------------------------+
| post_content       | no content  | The content to send as the message body  |
|                    |             | during HTTP POST messages.  The content  |
|                    |             | should be base64 encoded as per RFC4648. |
+--------------------+-------------+------------------------------------------+

Note that only the "uri" field is required.  All other fields are optional and
will take-on default values.

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


def monitor_get(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the monitor get command.

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
    if number_arguments > 0:
        m = monitors.Monitors(rest_api, secret)

        monitor_data = list()
        success = True
        for monitor_id in positional_arguments:
            try:
                mi = int(monitor_id)
            except:
                mi = None

            if mi is not None and mi > 0:
                monitor = m.get(mi)
                if monitor is not None:
                    monitor_data.append(monitor.as_dictionary())
                else:
                    monitor_data.append(mi)
            else:
                sys.stderr.write(
                    "*** Invalid monitor ID: %s\n"%mi
                )
                success = False

        if success:
            __dump(monitor_data)
    else:
        sys.stderr.write(
            "*** You must provide at least one monitor ID.\n"
        )
        success = False

    return success


def monitor_delete(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the hs delete command.

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
    if len(positional_arguments) == 1:
        try:
            monitor_id = int(positional_arguments[0])
        except:
            monitor_id = None

        if monitor_id is not None   and \
           monitor_id > 0           and \
           monitor_id <= 0xFFFFFFFF     :
            m = monitors.Monitors(rest_api, secret)
            monitor = m.get(monitor_id)
            if monitor is not None:
                success = m.delete(monitor)
                if not success:
                    sys.stderr.write("*** Failed to delete monitor.\n")
                    success = False
            else:
                sys.stderr.write("*** Unknown monitor ID.\n")
                success = False
        else:
            sys.stderr.write("*** Invalid monitor ID.\n")
            success = False
    else:
        sys.stderr.write("*** You must provide a single monitor ID.\n")
        success = False

    return success


def monitor_purge(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the monitor purge command.

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
    if len(positional_arguments) == 1:
        try:
            customer_id = int(positional_arguments[0])
        except:
            customer_id = None

        if customer_id is not None   and \
           customer_id > 0           and \
           customer_id <= 0xFFFFFFFF     :
            m = monitors.Monitors(rest_api, secret)
            success = m.purge(customer_id)
            if not success:
                sys.stderr.write("*** Failed to purge monitors.\n")
                success = False
        else:
            sys.stderr.write("*** Invalid customer ID.\n")
            success = False
    else:
        sys.stderr.write("*** You must provide a customer ID.\n")
        success = False

    return success


def monitor_list(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the monitor list command.

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
    if number_arguments == 0:
        m = monitors.Monitors(rest_api, secret)
        monitors_data = m.list()
        if monitors_data is not None:
            if isinstance(monitors_data, dict):
                __dump(
                    { monitor_id : m.as_dictionary()
                      for monitor_id, m in monitors_data.items()
                    }
                )
            else:
                __dump([ m.as_dictionary() for m in monitors_data ])
        else:
            sys.stderr.write("*** Failed to retrieve monitors.\n")
            success = False
    elif number_arguments == 1:
        try:
            customer_id = int(positional_arguments[0])
        except:
            customer_id = None

        if customer_id is not None   and \
           customer_id > 0           and \
           customer_id <= 0xFFFFFFFF     :
            m = monitors.Monitors(rest_api, secret)
            monitors_data = m.list(customer_id)
            if monitors_data is not None:
                md = list()
                for m in monitors_data:
                    if m is not None:
                        md.append(m.as_dictionary())
                    else:
                        md.append(None)

                __dump(md)
            else:
                sys.stderr.write("*** Failed to retrieve host/schemes.\n")
                success = False
        else:
            sys.stderr.write("*** Invalid customer ID.\n")
            success = False
    else:
        sys.stderr.write("*** Invalid number of parameters.\n")
        success = False

    return success


def monitor_update(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the monitor update command.

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
    if len(positional_arguments) == 3:
        file_type = positional_arguments[0].strip().lower()
        if file_type == 'json' or file_type == 'yaml':
            try:
                customer_id = int(positional_arguments[1])
            except:
                customer_id = None

            if customer_id is not None   and \
               customer_id > 0           and \
               customer_id <= 0xFFFFFFFF     :
                filename = positional_arguments[2]
                with open(filename, 'r') as fh:
                    update_data_text = fh.read()

                if file_type == 'json':
                    update_data = json.loads(update_data_text)
                else:
                    try:
                        update_data = yaml.load(
                            update_data_text,
                            Loader = yaml.FullLoader
                        )
                    except Exception as e1:
                        try:
                            update_data = yaml.load(update_data_text)
                        except Excetion as e2:
                            sys.stderr.write(
                                "Could not parse update file \"%s\":\n"%(
                                    configuration_filename
                                )
                            )
                            sys.stderr.write("Pass 1:\n%s\n"%str(e1))
                            sys.stderr.write("Pass 2:\n%s\n"%str(e2))
                            success = False

                if success:
                    m = monitors.Monitors(rest_api, secret)
                    result = m.update(customer_id, update_data)
                    if result:
                        sys.stderr.write("*** Update failed:\n")
                        for user_ordering, message in result:
                            if user_ordering is not None:
                                sys.stderr.write(
                                    "    %5d %s\n"%(
                                        user_ordering,
                                        message
                                    )
                                )
                            else:
                                sys.stderr.write(
                                    "          %s\n"%message
                                )

                        success = False
            else:
                sys.stderr.write("*** Invalid customer ID.\n")
                success = False
        else:
            sys.stderr.write("*** Invalid file type.\n")
            success = False
    else:
        sys.stderr.write("*** Invalid number of parameters.\n")
        success = False

    return success


def __dump(monitor_data):
    """
    Function that dumps information about monitors.

    :param monitor_data:
        A list of all the monitor instances to be dumped.

    :type monitor_data: list of Monitor instances

    """

    dump_data = yaml.dump(monitor_data, default_flow_style = False)
    sys.stdout.write(dump_data)

###############################################################################
# Extension configuration:
#

COMMANDS = {
    'monitor' : {
        'brief' : MONITOR_BRIEF,
        'help' : MONITOR_HELP,
        'subcommands' : {
            'get' : {
                'help' : MONITOR_GET_HELP,
                'execute' : monitor_get,
            },
            'delete' : {
                'help' : MONITOR_DELETE_HELP,
                'execute' : monitor_delete,
            },
            'purge' : {
                'help' : MONITOR_PURGE_HELP,
                'execute' : monitor_purge,
            },
            'list' : {
                'help' : MONITOR_LIST_HELP,
                'execute' : monitor_list,
            },
            'update' : {
                'help' : MONITOR_UPDATE_HELP,
                'execute' : monitor_update
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
