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
Class providing a API you can use to process event information.

"""

###############################################################################
# Import:
#

import sys
import time
import datetime

import libraries.events as events
import libraries.rest_api_common_v1 as rest_api_common_v1
import libraries.outbound_rest_api_v1 as outbound_rest_api_v1

###############################################################################
# Globals:
#

EVENT_BRIEF = "Allows you to add, remove, modify and list events."
"""
Brief description for the event command.

"""

EVENT_HELP = """
The event command allows you to manipulate events.  The event command
supports the following subcommands:

  event report <monitor id> <event type> <status>
               [ <message> [ <hex MD5 sum> [ <timestamp> ]]]
    Triggers a new event to be reported.

  event status ( monitor <monitor id> | customer <customer id> )
    Displays status of a single monitor or all monitors tied to a customer.

  event get <field> <value> [ <field> <value> [ <field> <value> ... ]]
    Reports information about events given a specified criteria.
"""
"""
Help text for this extension.

"""

EVENT_REPORT_HELP = """
The event report command allows you to report a new event.

  event report <monitor id> <event type> <status>
               [ <message> [ <hex hash> [ <timestamp> ]]]

Where <monitor id> is the ID of the monitor that triggered this event.  The
<event type> field should be one of "working", "no_response",
"content_changed", "keywords", "customer_x" (where x is a value between 1
and 10), "transaction", "inquiry", "support_request", or
"storage_limit_reached" indicating the cause of the event.  The status
field must be one of "unknown", "working", "failed" indicating the status of
the monitor when this event was detected.  The optional <message> field should
contain a message to be included with the event.  This message can be such
things as the returned status code or the missing keyword.  The optional
<hex hash> field should contain the hash for the received page that would
generate the event.  The optional <timestamp> field should contain the Unix
timestamp for the event.  If not specified, then the current time is used.

"""
"""
Help text for this extension.

"""

EVENT_GET_HELP = """
The event report command allows you to get information about events.

  event get <field> <value> [ <field> <value> [ <field> <value> ... ]]

You can include field/value pairs to constrain the events you want information
about.  The following field/value pairs are supported.

+----------+-------------------+----------------------------------------------+
| Field    | Value             | Function                                     |
+==========+===================+==============================================+
| customer | <customer id>     | Constrains events to those belonging to a    |
|          |                   | specific customer.                           |
+----------+-------------------+----------------------------------------------+
| monitor  | <monitor id>      | Constrains events to those belonging to a    |
|          |                   | specific monitor.                            |
+----------+-------------------+----------------------------------------------+
| start    | <start timestamp> | Indicates only events at or after this       |
|          |                   | timestamp should be included.                |
+----------+-------------------+----------------------------------------------+
| end      | <end timestamp>   | Indicates only events at or before this      |
|          |                   | timestamp should be included.                |
+----------+-------------------+----------------------------------------------+

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


def event_report(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the event report command.

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
    if number_arguments >= 3 or number_arguments <= 6:
        try:
            monitor_id = int(positional_arguments[0])
        except:
            monitor_id = None

        if monitor_id is not None and monitor_id > 0:
            try:
                event_type = events.EVENT_TYPE.by_name(
                    positional_arguments[1].upper().replace('-','_')
                )
            except:
                event_type = None

            try:
                monitor_status = events.MONITOR_STATUS.by_name(
                    positional_arguments[2].upper().replace('-', '_')
                )
            except:
                monitor_status = None

            if event_type is not None:
                if number_arguments >= 4:
                    message = positional_arguments[3]
                else:
                    message = str();

                if number_arguments >= 5:
                    hex_hash = positional_arguments[4]
                    page_hash = bytes.fromhex(hex_hash)
                else:
                    page_hash = bytes()

                if number_arguments == 6:
                    try:
                        timestamp = int(positional_arguments[5])
                    except:
                        timestamp = None
                else:
                    timestamp = int(time.time())

                if timestamp is not None or timestamp > 0:
                    e = events.Events(rest_api, secret)
                    success = e.report(
                        monitor_id = monitor_id,
                        page_hash = page_hash,
                        event_type = event_type,
                        monitor_status = monitor_status,
                        message = message,
                        timestamp = timestamp,
                    )

                    if not success:
                        sys.stderr.write("*** Failed to report event.\n")
                        success = False
                else:
                    sys.stderr.write("*** Invalid event type.\n")
                    success = False
            else:
                sys.stderr.write("*** Invalid event type.\n")
                success = False
        else:
            sys.stderr.write("*** Invalid monitor ID.\n")
            success = False
    else:
        sys.stderr.write("*** Invalid number of parameters.\n")
        success = False

    return success


def event_status(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the event create command.

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
    number_parameters = len(positional_arguments)
    monitor_status = None
    if number_parameters == 0:
        e = events.Events(rest_api, secret)
        monitor_status = e.status()
    elif number_parameters == 2:
        field = positional_arguments[0]
        try:
            value = int(positional_arguments[1])
        except:
            value = None

        if value is not None:
            if field == 'customer':
                e = events.Events(rest_api, secret)
                monitor_status = e.status(customer_id = value)
            elif field == 'monitor':
                e = events.Events(rest_api, secret)
                monitor_status = e.status(monitor_id = value)
            else:
                sys.stderr.write("*** Must specify customer or monitor.\n")
                success = False
        else:
            sys.stderr.write("*** Invalid value.\n")
            success = False
    else:
        sys.stderr.write("*** You must provide at least one event name.\n")
        success = False

    if success:
      sys.stdout.write("+------------+---------+\n");
      sys.stdout.write("| monitor id | status  |\n");
      sys.stdout.write("+============+=========+\n");

      for id, status in monitor_status.items():
          sys.stdout.write("| %10d | %-7s |\n"%(id, str(status).lower()))
          sys.stdout.write("+------------+---------+\n");

    return success


def event_get(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the event get command.

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
    number_arguments = len(positional_arguments)
    if (number_arguments % 2) == 0:
        index = 0
        customer_id = None
        monitor_id = None
        start_timestamp = None
        end_timestamp = None

        while success and index < number_arguments:
            field_name = positional_arguments[index + 0].lower()
            try:
                value = int(positional_arguments[index + 1])
            except:
                value = None

            if value is not None:
                if field_name == 'customer':
                    customer_id = value
                elif field_name == 'monitor':
                    monitor_id = value
                elif field_name == 'start':
                    start_timestamp = value
                elif field_name == 'end':
                    end_timestamp = value
                else:
                    sys.stderr.write("*** Invalid field: %s\n"%field_name)
                    success = False

                index += 2
            else:
                sys.stderr.write("*** Invalid field value.\n")
                success = False

        if success:
            e = events.Events(rest_api, secret)
            event_list = e.get(
                customer_id = customer_id,
                monitor_id = monitor_id,
                start_timestamp = start_timestamp,
                end_timestamp = end_timestamp
            )

            if events is not None:
                __dump(event_list)
            else:
                sys.stderr.write("*** Failed to retrieve events.\n")
                success = False
    else:
        sys.stderr.write("*** Invalid number of arguments.\n")
        success = False

    return success


def __dump(events):
    """
    Method used internally to dump events.

    :param events:
        The list of events to be dumped.

    :type events: list

    """

    sys.stdout.write(
        "+-------------+---------------------+----------+------------+"
        "-------------+-----------------+\n"
    )
    sys.stdout.write(
        "| timestamp   | date/time           | event_id | monitor_id | "
        "customer_id | event_type      |\n"
    )
    sys.stdout.write(
        "+=============+=====================+==========+============+"
        "=============+=================+\n"
    )

    for event in events:
        sys.stdout.write(
            "| %-11d | %19s | %8d | %10d | %11d | %-15s |\n"%(
                event.timestamp,
                str(datetime.datetime.fromtimestamp(event.timestamp)),
                event.event_id,
                event.monitor_id,
                event.customer_id,
                str(event.event_type).lower()
            )
        )
        sys.stdout.write(
            "+-------------+---------------------+----------+------------+"
            "-------------+-----------------+\n"
        )

###############################################################################
# Extension configuration:
#

COMMANDS = {
    'event' : {
        'brief' : EVENT_BRIEF,
        'help' : EVENT_HELP,
        'subcommands' : {
            'report' : {
                'help' : EVENT_REPORT_HELP,
                'execute' : event_report,
            },
            'status' : {
                'help' : EVENT_HELP,
                'execute' : event_status,
            },
            'get' : {
                'help' : EVENT_GET_HELP,
                'execute' : event_get,
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
