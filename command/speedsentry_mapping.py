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

import libraries.customer_mapping as customer_mapping
import libraries.rest_api_common_v1 as rest_api_common_v1
import libraries.outbound_rest_api_v1 as outbound_rest_api_v1

###############################################################################
# Globals:
#

MAPPING_BRIEF = "Allows you to manage customer/server mappings."
"""
Brief description for the mapping command.

"""

MAPPING_HELP = """
The mapping command allows you to manipulate customer/server mappings as well
as view the current mappings.  The mapping command supports the following
subcommands:

  mapping get <customer id>
    Gets customer/server mapping for a specific customer.

  mapping update <customer id> [ <server id> [ <server id> ... ]]
    Maps a collection of servers to this customer.

  mapping activate <customer id>
    Activates a customer.

  mapping deactivate <customer id>
    Deactivates a customer.

  mapping list [ <server id> ]
    Lists all known mappings.
"""

MAPPING_GET_HELP = """
The mapping get command allows you to view information regarding the mapping
for a single customer.  The syntax for the command is:

  mapping get <customer id>

Where <customer id> is the customer of interest.

Note that the server ID in parenthesis is the designated primary server.

"""

MAPPING_UPDATE_HELP = """
The mapping update command allows you to change the currently recorded
customer/server mapping for a single customer.  The syntax for the command is:

  mapping update <customer id> [ <server id> [ <server id> [ ... ]]]

Where the first <server id> value is interpreted as the primary server.

"""

MAPPING_ACTIVATE_HELP = """
The mapping activate command allows you to activate a customer's settings
across polling servers.  The syntax for the command is:

  mapping activate <customer id>

Where <customer id> is the customer of interest.

"""

MAPPING_DEACTIVATE_HELP = """
The mapping deactivate command allows you to deactivate a customer on all
polling servers to which the customer has been assigned.  The syntax for the
command is:

  mapping deactivate <customer id>

Where <customer id> is the customer of interest.

"""

MAPPING_LIST_HELP = """
The mapping list command allows you to view mappings across more than one
customer, optionally restricted to customers that reference a specific server.
The syntax for the command is:

  mapping list [ <server id> ]

Note that server ID in parenthesis is the designated primary server for a given
customer.

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


def mapping_get(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the mapping get command.

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
            customer_id = None

        if customer_id is not None and \
           customer_id > 0 and         \
           customer_id <= 0xFFFFFFFF   :
            c = customer_mapping.CustomerMapping(
                rest_api = rest_api,
                secret = secret
            )

            result = c.get(customer_id)
            if result is not None:
                __dump(result)
            else:
                success = False
                sys.stderr.write("*** Failed response.\n")
        else:
            success = False
            sys.stderr.write("*** Invalid customer ID.\n")
    else:
        sys.stderr.write("*** You must provide at one customer ID.\n")
        success = False

    return success


def mapping_update(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the mapping update command.

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
        try:
            customer_id = int(positional_arguments[0])
        except:
            customer_id = None

        if customer_id is not None and \
           customer_id > 0 and         \
           customer_id <= 0xFFFFFFFF   :
            try:
                servers = [ int(s) for s in positional_arguments[1:] ]
            except:
                servers = None

            if servers is not None:
                if len(servers) > 0:
                    primary_server = servers[0]
                else:
                    primary_server = 0

                c = customer_mapping.CustomerMapping(
                    rest_api = rest_api,
                    secret = secret
                )

                success = c.update(customer_id, primary_server, servers)
                if not success:
                    sys.stderr.write("*** Failed response.\n")
            else:
                success = False
                sys.stderr.write("*** Invalid server ID.\n")
        else:
            success = False
            sys.stderr.write("*** Invalid customer ID.\n")
    else:
        sys.stderr.write("*** You must provide at least a customer ID.\n")
        success = False

    return success


def mapping_activate(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the mapping activate command.

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
            customer_id = None

        if customer_id is not None and \
           customer_id > 0 and         \
           customer_id <= 0xFFFFFFFF   :
            c = customer_mapping.CustomerMapping(
                rest_api = rest_api,
                secret = secret
            )

            result = c.activate(customer_id)
            if not result:
                success = False
                sys.stderr.write("*** Failed to activate.\n")
        else:
            success = False
            sys.stderr.write("*** Invalid customer ID.\n")
    else:
        sys.stderr.write("*** You must provide at one customer ID.\n")
        success = False

    return success


def mapping_deactivate(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the mapping activate command.

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
            customer_id = None

        if customer_id is not None and \
           customer_id > 0 and         \
           customer_id <= 0xFFFFFFFF   :
            c = customer_mapping.CustomerMapping(
                rest_api = rest_api,
                secret = secret
            )

            result = c.deactivate(customer_id)
            if not result:
                success = False
                sys.stderr.write("*** Failed to deactivate.\n")
        else:
            success = False
            sys.stderr.write("*** Invalid customer ID.\n")
    else:
        sys.stderr.write("*** You must provide at one customer ID.\n")
        success = False

    return success


def mapping_list(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the mapping list command.

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
    if number_arguments == 0 or number_arguments == 1:
        server_id = None
        if number_arguments == 1:
            try:
                server_id = int(positional_arguments[0])
            except:
                server_id = None

            if server_id is None or server_id < 1 or server_id > 0xFFFF:
                success = False
                sys.stderr.write("*** Invalid server ID.\n")

        if success:
            c = customer_mapping.CustomerMapping(
                rest_api = rest_api,
                secret = secret
            )

            result = c.list(server_id)
            if result is not None:
                for customer_id, data in result.items():
                    sys.stdout.write("%7d: "%customer_id)
                    __dump(data)
            else:
                sys.stderr.write("*** Failed response.\n")
    else:
        sys.stderr.write("*** Invalid number of parameters.\n")
        success = False

    return success


def __dump(mapping):
    """
    Function that dumps mapping information.

    :param mapping:
        The mapping to be dumped.

    :type mapping: Mapping instance.

    """

    s = str()
    for server_id in mapping:
        if server_id == mapping.primary_server_id:
            e = "(%d)"%server_id
        else:
            e = "%d"%server_id

        if s:
            s += " " + e;
        else:
            s = e

    sys.stdout.write(s + "\n")

###############################################################################
# Extension configuration:
#

COMMANDS = {
    'mapping' : {
        'brief' : MAPPING_BRIEF,
        'help' : MAPPING_HELP,
        'subcommands' : {
            'get' : {
                'help' : MAPPING_GET_HELP,
                'execute' : mapping_get,
            },
            'update' : {
                'help' : MAPPING_UPDATE_HELP,
                'execute' : mapping_update,
            },
            'activate' : {
                'help' : MAPPING_ACTIVATE_HELP,
                'execute' : mapping_activate,
            },
            'deactivate' : {
                'help' : MAPPING_DEACTIVATE_HELP,
                'execute' : mapping_deactivate,
            },
            'list' : {
                'help' : MAPPING_LIST_HELP,
                'execute' : mapping_list,
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
