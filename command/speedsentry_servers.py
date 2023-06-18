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
Class providing a API you can use to process server information.

"""

###############################################################################
# Import:
#

import sys

import libraries.regions as regions
import libraries.servers as servers
import libraries.rest_api_common_v1 as rest_api_common_v1
import libraries.outbound_rest_api_v1 as outbound_rest_api_v1

###############################################################################
# Globals:
#

SERVER_BRIEF = "Allows you to manage backend polling servers."
"""
Brief description for the server command.

"""

SERVER_HELP = """
The server command allows you to manipulate server data as well as some server
functions.  The server command supports the following subcommands:

  server get (<server ID> | <server identifier>)
             [ (<server ID> | <server identifier>)
             [ (<server ID> | <server identifier) ... ]]
    Gets server data by server ID or identifier.

  server create <region id> <server identifier>
    Creates a new server entry.

  server modify <server id> <field> <value> [ <field> <value>
                                            [ <field> <value> ... ]]
    Modifies settings related to a given server.

  server delete <server ID>
    Deletes a server by ID.  This will also remove customer data collected by
    this server.  In most situations, you should reassign the server's work
    and mark the server as defunct using the server modify command.

  server list [ <field> <value [ <field> <value ]]
    Lists all the servers.

  server activate <server id>
    Activates a server and conditionally updates the region settings across the
    fleet of polling servers.

  server deactivate <server id>
    Deactivates a server and conditionally updates the region settings across
    the fleet of polling servers.  Monitors being served by this polling server
    are *not* reassigned.

  server start <server id>
    Pushes down customer data to a polling server and commands the server to
    go active.  The server must have been previously activated using the
    "server activate" command.

  server reassign <from server id> [ <to server id> ]
    Reassigns work from one server to another and deactivates the "from"
    server.  The old server must be deactivated before triggering this
    function.

  server redistribute [ <region id> ]
    Redistributes work across servers in a given region to balance workloads.
    You can use this command after adding new servers to reduce the total
    workload on each server.
"""

SERVER_GET_HELP = """
The server get command allows you to view information regarding one or more
servers.  The syntax for the command is:

  server get <server identifier> [ <sserver identifier>
                                 [ <server identifier> ... ]]

Where <server identifier> represents either a numeric server ID or the server
identifier string as registered in the database.

The data will be presented in a tabulated format.

"""

SERVER_CREATE_HELP = """
The server create command allows you to create a new database entry for a
server.  Upon creation, the server will be marked as inactive.

  server create <region id> <server identifier>

Where <region id> is the ID of the region where the server resides and
<server identifier> is either the publically visible hostname or the publically
visible IP address of the server.  Note that the region ID must be valid for
this command to work.  Also note that the identifier is not checked.

"""

SERVER_MODIFY_HELP = """
The server modify command allows you to modify an existing database entry for
a server.  Note that this command does not modify the server state and the
server can only be modified if it's inactive.

  server modify <server id> <field> <value> [ <field> <value>
                                            [ <field> <value> ... ]]

You specify server settings using field/value pairs.  At this time the
following fields can be modified:

  region_id -  The numeric region ID where the server is reported to reside.
               You can get a list of available regions using the "region list"
               command.

  identifier - The server's identifier string.  This should be either the
               publically visible hostname of the server of the server's
               publically visible IP address.

  status -     The reported server status.  Value should be one of "active",
               "inactive", or "defunct".  Again this command will not modify
               the server state, only the value indicated by the database.  As
               a general rule, you should not use this command to set the
               server state to "active".

Please note the server activate and server deactivate commands that do adjust
the server state as well as adjustments to region data for all other servers,
if needed.

"""

SERVER_DELETE_HELP = """
The server delete command allows you to delete a server from the system.  Note
that deleting a server will also delete all the customer data collected by that
server so use this command with care.

  server delete <server id>

Note that the server's status must be "defunct" in order for the server to be
deleted.

"""

SERVER_LIST_HELP = """
The server list command allows you to list servers.  You can optionally
constrain the list to only show servers in a given region and or only
servers with a specific status.

  server list [ <field> <value> [ <field> <value> ]]

You can optionally constrain the list by specifying field/value pairs.  At this
time the following fields are supported.

  region_id - The numeric region ID where the server is reported to reside.
              You can get a list of available regions using the "region list"
              command.

  status -    The reported server status.  Value should be one of "active",
              "inactive", or "defunct".

"""

SERVER_ACTIVATE_HELP = """
The server activate command tells the database controller to change a server's
status to active.  If the server being activated is in a new region, then the
number of active regions changed and all servers will be updated to reflect
the new number of regions and region assignments.

The command syntax is:

   server activate <server id>

Where <server id> is the ID of the server to be activated.

If the server is already active, then no change to the system will be made.

"""

SERVER_DEACTIVATE_HELP = """
The server deactivate command tells the database controller to change a
server's status to inactive.  If the server being deactivated is the last
server in a region, then the number of active regions changed and all servers
will be updated to reflect the new number of regions and region assignments.

The command syntax is:

   server deactivate <server id>

Where <server id> is the ID of the server to be deactivated.

If the server is already inactive, then no change to the system will be made.

"""

SERVER_START_HELP = """
The server start command tells the database controller to push down all
customer data to a given polling server and then tell the polling server to
start normal operation.  This command will be rejected if the server's status
is not "active".

You can use this command if, for some reason, you must stop and restart a
polling server that is already active and has assigned custoemrs.

The command syntax is:

   server start <server id>

Where <server id> is the ID of the server to be started.

"""

SERVER_REASSIGN_HELP = """
The server reassign command reassigns work performed by a given server.  You
can redistribute work to another specific server or you can distribute work
across all servers in the same region.  Once work has been reassigned, the
original server's state will be changed to inactive preventing new work being
assigned to it.

The old server's state must also be set to inactive before triggering this
function so that new work is not assigned to the server during the reassignment
process.

  server reassign <from server id> [ <to server id> ]

The <from server id> field is the ID of the server work is being taken from.
If you include the <to server id> parameter, then work will be moved to this
new server.

"""

SERVER_REDISTRIBUTE_HELP = """
The server redistribute command redistributes work across all the servers in a
single region to more evenly balance out work between servers.

  server redistribute <region id>

The <region id> is the region to distribute work across.

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


def server_get(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the region get command.

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
        s = servers.Servers(rest_api, secret)

        servers_data = list()
        for server_identifier in positional_arguments:
            server_data = s.get(server_identifier)
            if server_data is None:
                servers_data.append(server_identifier)
            else:
                servers_data.append(server_data)

        __dump(
            servers_data = servers_data,
            rest_api = rest_api,
            secret = secret
        )
    else:
        sys.stderr.write(
            "*** You must provide at least one server identifier, either a "
            "server ID or\n    server identifier string.\n"
        )
        success = False

    return success


def server_create(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the region create command.

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
    if len(positional_arguments) == 2:
        try:
            region_id = int(positional_arguments[0])
        except:
            region_id = None

        if region_id is not None and region_id > 0 and region_id <= 0xFFFF:
            identifier = positional_arguments[1]

            s = servers.Servers(rest_api, secret)
            server = s.create(region_id, identifier)

            if server is not None:
                sys.stdout.write(
                    "server id:      %d\n"
                    "region id:      %d\n"
                    "identifier:     %s\n"
                    "status:         %s\n"
                    "monitor count:  %d\n"
                    "cpu loading:    %f\n"
                    "memory loading: %f\n"%(
                        server.server_id,
                        server.region_id,
                        server.identifier,
                        str(server.status).lower(),
                        server.monitors_per_second,
                        server.cpu_loading,
                        server.memory_loading
                    )
                )
            else:
                sys.stderr.write("*** Failed to create server.\n")
                success = False
        else:
            sys.stderr.write("*** Invalid region ID.\n")
            success = False
    else:
        sys.stderr.write(
            "*** You must provide a region ID and server identifier.\n"
        )
        success = False

    return success


def server_modify(positional_arguments, arguments, rest_api, secret):
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
    number_arguments = len(positional_arguments)
    if number_arguments >= 3 and (number_arguments % 2) == 1:
        try:
            server_id = int(positional_arguments[0])
        except:
            server_id = None

        if server_id is not None and server_id > 0:
            region_id = None
            identifier = None
            status = None

            argument_index = 1
            while success and argument_index < number_arguments:
                field = positional_arguments[argument_index].lower()
                value = positional_arguments[argument_index + 1]

                if field == 'region_id' or \
                   field == 'region-id' or \
                   field == 'region'       :
                    if region_id is None:
                        try:
                            region_id = int(value)
                        except:
                            success = False

                        if not success:
                            sys.stderr.write("*** Invalid region ID.\n")
                    else:
                        sys.stderr.write("*** Duplicate region_id field.\n")
                        success = False
                elif field == 'identifier':
                    if identifier is None:
                        identifier = value
                    else:
                        sys.stderr.write("*** Duplicate identifier field.\n")
                        success = False
                elif field == 'status':
                    if status is None:
                        value = value.lower()
                        if value == 'active':
                            status = servers.STATUS.ACTIVE
                        elif value == 'inactive':
                            status = servers.STATUS.INACTIVE
                        elif value == 'defunct':
                            status = servers.STATUS.DEFUNCT
                        else:
                            sys.stderr.write("*** Invalid status value.\n")
                            success = False
                    else:
                        sys.stderr.write("*** Duplicate status field.\n")
                        success = False
                else:
                    sys.stderr.write("*** Unknown field \"%s\".\n"%field)
                    success = False

                argument_index += 2

            if success:
                s = servers.Servers(rest_api, secret)
                server = s.modify(
                    server_id = server_id,
                    region_id = region_id,
                    identifier = identifier,
                    status = status
                )

                if server is not None:
                    sys.stdout.write(
                        "server id:      %d\n"
                        "region id:      %d\n"
                        "identifier:     %s\n"
                        "status:         %s\n"
                        "monitor count:  %d\n"
                        "cpu loading:    %f\n"
                        "memory loading: %f\n"%(
                            server.server_id,
                            server.region_id,
                            server.identifier,
                            str(server.status).lower(),
                            server.monitors_per_second,
                            server.cpu_loading,
                            server.memory_loading
                        )
                    )
                else:
                    sys.stderr.write("*** Failed to modify server.\n")
                    success = False
        else:
            sys.stderr.write(
                "*** Invalid server ID %s\n"%argument
            )
            success = False
    else:
        sys.stderr.write("*** Invalid or missing parameters.\n")
        success = False

    return success


def server_delete(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the region delete command.

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
            server_id = int(positional_arguments[0])
        except:
            server_id = None

        if server_id is not None and server_id > 0 and server_id <= 0xFFFF:
            s = servers.Servers(rest_api, secret)
            server = s.get(server_id)
            if server:
                success = s.delete(server)
                if not success:
                    sys.stderr.write("*** Failed to delete server.\n")
            else:
                sys.stderr.write("*** Unknown server ID.\n")
                success = False
        else:
            sys.stderr.write("*** Invalid server ID.\n")
            success = False
    else:
        sys.stderr.write("*** You must provide a single server ID.\n")
        success = False

    return success


def server_list(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the region list command.

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
    if (number_arguments % 2) == 0:
        region_id = None
        status = None

        argument_index = 0
        while success and argument_index < number_arguments:
            field = positional_arguments[argument_index].lower()
            value = positional_arguments[argument_index + 1]

            if field == 'region_id' or \
               field == 'region-id' or \
               field == 'region'       :
                if region_id is None:
                    try:
                        region_id = int(value)
                    except:
                        success = False

                    if not success:
                        sys.stderr.write("*** Invalid region ID.\n")
                else:
                    sys.stderr.write("*** Duplicate region_id field.\n")
                    success = False
            elif field == 'status':
                if status is None:
                    value = value.lower()
                    if value == 'active':
                        status = servers.STATUS.ACTIVE
                    elif value == 'inactive':
                        status = servers.STATUS.INACTIVE
                    elif value == 'defunct':
                        status = servers.STATUS.DEFUNCT
                    else:
                        sys.stderr.write("*** Invalid status value.\n")
                        success = False
                else:
                    sys.stderr.write("*** Duplicate status field.\n")
                    success = False
            else:
                sys.stderr.write("*** Unknown field \"%s\".\n"%field)
                success = False

            argument_index += 2

        if success:
            s = servers.Servers(rest_api, secret)
            servers_data = s.list(
                region_id = region_id,
                status = status
            )

            if servers_data is not None:
                __dump(servers_data, rest_api, secret)
            else:
                sys.stderr.write("*** Failed to retrieve server list.\n")
                success = False
    else:
        sys.stderr.write("*** Invalid number of parameters.\n")
        success = False

    return success


def server_activate(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the server activate command.

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
            server_id = int(positional_arguments[0])
        except:
            server_id = None

        if server_id is not None and server_id > 0 and server_id <= 0xFFFF:
            s = servers.Servers(rest_api, secret)
            success = s.activate(server_id)
            if not success:
                sys.stderr.write("*** Failed to activate server.\n")
        else:
            sys.stderr.write("*** Invalid server ID.\n")
            success = False
    else:
        sys.stderr.write("*** You must provide a single server ID.\n")
        success = False

    return success


def server_deactivate(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the server activate command.

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
            server_id = int(positional_arguments[0])
        except:
            server_id = None

        if server_id is not None and server_id > 0 and server_id <= 0xFFFF:
            s = servers.Servers(rest_api, secret)
            success = s.deactivate(server_id)
            if not success:
                sys.stderr.write("*** Failed to deactivate server.\n")
        else:
            sys.stderr.write("*** Invalid server ID.\n")
            success = False
    else:
        sys.stderr.write("*** You must provide a single server ID.\n")
        success = False

    return success


def server_start(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the server start command.

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
            server_id = int(positional_arguments[0])
        except:
            server_id = None

        if server_id is not None and server_id > 0 and server_id <= 0xFFFF:
            s = servers.Servers(rest_api, secret)
            success = s.start(server_id)
            if not success:
                sys.stderr.write("*** Failed to start server.\n")
        else:
            sys.stderr.write("*** Invalid server ID.\n")
            success = False
    else:
        sys.stderr.write("*** You must provide a single server ID.\n")
        success = False

    return success


def server_reassign(positional_arguments, arguments, rest_api, secret):
    """
    Function that reassigns work from one server to another.

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
    if number_arguments == 1 or number_arguments == 2:
        try:
            from_server_id = int(positional_arguments[0])
        except:
            from_server_id = None

        if from_server_id is not None and \
           from_server_id > 0         and \
           from_server_id <= 0xFFFF       :
            if number_arguments == 2:
                try:
                    to_server_id = int(positional_arguments[1])
                except:
                    to_server_id = None

                if to_server_id is None  or \
                   to_server_id <= 0     or \
                   to_server_id > 0xFFFF    :
                    sys.stderr.write(
                        "*** Invalid to server id value.\n"
                    )
                    success = False
            else:
                to_server_id = None
        else:
            sys.stderr.write("*** Invalid from server id value.\n")
            success = False

        if success:
            s = servers.Servers(rest_api, secret)
            success = s.reassign(from_server_id, to_server_id)
            if not success:
                sys.stderr.write("*** Failed to reassign work.\n")
    else:
        sys.stderr.write("*** Invalid number of parameters.\n")
        success = False

    return success


def server_redistribute(positional_arguments, arguments, rest_api, secret):
    """
    Function that redistributes work from one server to another.

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
            region_id = int(positional_arguments[0])
        except:
            region_id = None

        if region_id is not None and region_id > 0 and region_id <= 0xFFFF:
            s = servers.Servers(rest_api, secret)
            success = s.redistribute(region_id)
            if not success:
                sys.stderr.write("*** Failed to redistribute work.\n")
        else:
            sys.stderr.write("*** Invalid region ID value.\n")
            success = False
    else:
        sys.stderr.write("*** Invalid number of parameters.\n")
        success = False

    return success


def __get_regions(rest_api, secret):
    """
    Function that gets all the server regions.

    :param rest_api:
        The outbound REST API to use to communicate with Inesonic
        infrastructure.

    :param secret:
        The secret required to use the Inesonic REST API.

    :return:
        Returns a tuple holding the maximum region name length followed by a
        dictionary of region names by region ID.

    :type rest_api: outbound_rest_api_v1.Server
    :type secret:   bytes
    :rtype:         tuple

    """

    r = regions.Regions(rest_api, secret)
    all_regions = r.get_all()

    maximum_region_name_length = 0
    for region_id, region_name in all_regions.items():
        maximum_region_name_length = max(
            maximum_region_name_length,
            len(region_name)
        )

    return ( maximum_region_name_length, all_regions )


def __dump(servers_data, rest_api, secret):
    """
    Function that dumps information about all the servers to stdout with a nice
    header.

    :param servers_data:
        A list of all the servers to be dumped.

    :param rest_api:
        The outbound REST API to use to communicate with Inesonic
        infrastructure.

    :param secret:
        The secret required to use the Inesonic REST API.

    :return:
        Returns a tuple holding the maximum region name length followed by a
        dictionary of region names by region ID.

    :type rest_api: outbound_rest_api_v1.Server
    :type secret:   bytes
    :rtype:         tuple

    """

    (
        maximum_region_name_length,
        all_regions
    ) = __get_regions(
        rest_api,
        secret
    )

    maximum_identifier_length = len("identifier")
    valid_servers_data = list()
    invalid_servers_data = list()

    for server_data in servers_data:
        if not isinstance(server_data, int) and \
           not isinstance(server_data, str)     :
            valid_servers_data.append(server_data)
            identifier_length = len(server_data.identifier)
            maximum_identifier_length = max(
                maximum_identifier_length,
                identifier_length
            )

    for server_data in invalid_servers_data:
        sys.stdout.write(
            "*** Unknown server %s\n"%str(server_data)
        )

    if valid_servers_data:
        maximum_region_name_length = max(
            maximum_region_name_length,
            len("region name")
        )

        fmt_string = "| %%10d | %%-%ds | %%10d | %%-%ds | %%-11s | %%19f " \
                     "| %%11f | %%14f |\n"%(
            maximum_identifier_length,
            maximum_region_name_length
        )

        fmt_head_string = "| %%10s | %%-%ds | %%10s | %%-%ds | %%-11s " \
                          "| %%19s | %%11s | %%14s |\n"%(
            maximum_identifier_length,
            maximum_region_name_length
        )

        divider_string = (
              "+-"
            + "-" * 10 + "-+-"
            + "-" * maximum_identifier_length + "-+-"
            + "-" * 10 + "-+-"
            + "-" * maximum_region_name_length + "-+-"
            + "-" * 11 + "-+-"
            + "-" * 19 + "-+-"
            + "-" * 11 + "-+-"
            + "-" * 14 + "-+\n"
        )

        sys.stdout.write(divider_string)
        sys.stdout.write(
            fmt_head_string%(
                "server id",
                "identifier",
                "region id",
                "region name",
                "status",
                "monitors per second",
                "cpu loading",
                "memory_loading"
            )
        )

        sys.stdout.write(
              "+="
            + "=" * 10 + "=+="
            + "=" * maximum_identifier_length + "=+="
            + "=" * 10 + "=+="
            + "=" * maximum_region_name_length + "=+="
            + "=" * 11 + "=+="
            + "=" * 19 + "=+="
            + "=" * 11 + "=+="
            + "=" * 14 + "=+\n"
        )

        for server_data in valid_servers_data:
            region_id = server_data.region_id
            try:
                region_name = all_regions[region_id]
            except:
                region_name = '???'

            sys.stdout.write(
                fmt_string%(
                    server_data.server_id,
                    server_data.identifier,
                    region_id,
                    region_name,
                    str(server_data.status).lower(),
                    server_data.monitors_per_second,
                    server_data.cpu_loading,
                    server_data.memory_loading
                )
            )
            sys.stdout.write(divider_string)

###############################################################################
# Extension configuration:
#

COMMANDS = {
    'server' : {
        'brief' : SERVER_BRIEF,
        'help' : SERVER_HELP,
        'subcommands' : {
            'get' : {
                'help' : SERVER_GET_HELP,
                'execute' : server_get,
            },
            'create' : {
                'help' : SERVER_CREATE_HELP,
                'execute' : server_create,
            },
            'modify' : {
                'help' : SERVER_MODIFY_HELP,
                'execute' : server_modify,
            },
            'delete' : {
                'help' : SERVER_DELETE_HELP,
                'execute' : server_delete,
            },
            'list' : {
                'help' : SERVER_LIST_HELP,
                'execute' : server_list,
            },
            'activate' : {
                'help' : SERVER_ACTIVATE_HELP,
                'execute' : server_activate,
            },
            'deactivate' : {
                'help' : SERVER_DEACTIVATE_HELP,
                'execute' : server_deactivate,
            },
            'start' : {
                'help' : SERVER_START_HELP,
                'execute' : server_start,
            },
            'reassign' : {
                'help' : SERVER_REASSIGN_HELP,
                'execute' : server_reassign,
            },
            'redistribute' : {
                'help' : SERVER_REDISTRIBUTE_HELP,
                'execute' : server_redistribute,
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
