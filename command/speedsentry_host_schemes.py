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
Class providing a API you can use to process host/scheme information.

"""

###############################################################################
# Import:
#

import sys

import libraries.host_schemes as host_schemes
import libraries.rest_api_common_v1 as rest_api_common_v1
import libraries.outbound_rest_api_v1 as outbound_rest_api_v1

###############################################################################
# Globals:
#

HOST_SCHEME_BRIEF = "Allows you to manage customer hosts and schemes."
"""
Brief description for the hs command.

"""

HOST_SCHEME_HELP = """
The hs command allows you to directly manipulate cutomer host and scheme data.
The hs command supports the following subcommands:

  hs get <host scheme id> [ <host_scheme id> [ <host scheme id> ... ]]
    Gets host/scheme data by internal ID.

  hs create <customer_id> <url>
    Creates a new host/scheme instance for a given customer.

  hs modify <host_scheme_id> <field> <value> [ <field> <value>
                                             [ <field> <value> ... ]]
    Modifies settings related to a specific host/scheme.

  hs delete <host scheme id>
    Deletes a host/scheme by host scheme ID.

  hs purge <customer id>
    Purges all the host/scheme data tied to a specific customer.

  hs list [ <customer id> ]
    Lists host schemes, optionally limited to a specific customer.

"""
"""
Help text for this extension.

"""

HOST_SCHEME_GET_HELP = """
The server get command allows you to view information regarding one or more
host/scheme instances.  The syntax for the command is:

  hs get <host scheme id> [ <host scheme id> [ <host_scheme_id> ]]

Where <host scheme id> is an internal host/scheme instance.

The data will be presented in a tabulated format.

"""
"""
Help text for this extension.

"""

HOST_SCHEME_CREATE_HELP = """
The hs create command allows you to create a new database entry for a customer
host/scheme.

  hs create <customer id> <url>

Where <customer id> is the ID of the customer tied to this host/scheme and
<url> is the URL, including the scheme.  The URL should be of the form
"http://myserver.com".

"""
"""
Help text for this extension.

"""

HOST_SCHEME_MODIFY_HELP = """
The hs modify command allows you to modify an existing database entry for
a customer host/scheme.

  hs modify <host scheme id> <field> <value> [ <field> <value>
                                             [ <field> <value> ... ]]

You specify server settings using field/value pairs.  At this time the
following fields can be modified:

  customer_id - The numeric customer ID of the customer tied to this
                host/scheme instance.

  url -         The combined scheme and host formatted as "scheme://host".

"""
"""
Help text for this extension.

"""

HOST_SCHEME_DELETE_HELP = """
The hs delete command allows you to delete a host scheme from the system.  Note
that deleting a host/scheme will also cause any customer slugs associated with
that host/scheme to also be deleted.

  hs delete <host scheme id>

"""
"""
Help text for this extension.

"""

HOST_SCHEME_PURGE_HELP = """
The hs purge command allows you to delete all host schemes, and, by extension,
slugs associated with a specific user.

  hs purge <customer id>

"""
"""
Help text for this extension.

"""

HOST_SCHEME_LIST_HELP = """
The hs list command allows you to list host schemes.  You can optionally
constrain the list to only show host/schemes for a single customer by
specifying the customer ID.

  server list [ <customer id> ]

You can optionally constrain the list to a single customer by specifying a
customer ID.

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


def host_scheme_get(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the hs get command.

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
        hs = host_schemes.HostSchemes(rest_api, secret)

        host_scheme_data = list()
        success = True
        for host_scheme_id in positional_arguments:
            try:
                hsi = int(host_scheme_id)
            except:
                hsi = None

            if hsi is not None and hsi > 0:
                host_scheme = hs.get(hsi)
                if host_scheme is not None:
                    host_scheme_data.append(host_scheme)
                else:
                    host_scheme_data.append(hsi)
            else:
                sys.stderr.write(
                    "*** Invalid host scheme ID:%s\n"%host_scheme_id
                )
                success = FAlse

        if success:
            __dump(host_scheme_data)
    else:
        sys.stderr.write(
            "*** You must provide at least one host scheme ID.\n"
        )
        success = False

    return success


def host_scheme_create(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the hs create command.

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
            customer_id = int(positional_arguments[0])
        except:
            customer_id = None

        if customer_id is not None and customer_id > 0:
            url = positional_arguments[1]

            hs = host_schemes.HostSchemes(rest_api, secret)
            host_scheme = hs.create(customer_id, url)
            if host_scheme is not None:
                sys.stdout.write(
                    "host_scheme_id:           %d\n"
                    "customer_id:              %d\n"
                    "host:                     %s\n"
                    "scheme:                   %s\n"
                    "ssl_expiration_timestmap: %d\n"%(
                        host_scheme.host_scheme_id,
                        host_scheme.customer_id,
                        host_scheme.host,
                        str(host_scheme.scheme),
                        host_scheme.ssl_expiration_timestamp
                    )
                )
            else:
                sys.stderr.write("*** Could not create host/scheme.\n")
                success = False
        else:
            sys.stderr.write("*** Invalid customer ID.\n")
            success = False
    else:
        sys.stderr.write(
            "*** You must provide a customer ID and URL (scheme:://host).\n"
        )
        success = False

    return success


def host_scheme_modify(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the hs modify command.

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
            host_scheme_id = int(positional_arguments[0])
        except:
            host_scheme_id = None

        if host_scheme_id is not None and host_scheme_id > 0:
            customer_id = None
            url = None

            argument_index = 1
            while success and argument_index < number_arguments:
                field = positional_arguments[argument_index].lower()
                value = positional_arguments[argument_index + 1]

                if field == 'customer_id' or \
                   field == 'customer-id' or \
                   field == 'customer'       :
                    if customer_id is None:
                        try:
                            customer_id = int(value)
                        except:
                            success = False

                        if not success:
                            sys.stderr.write("*** Invalid customer ID.\n")
                    else:
                        sys.stderr.write("*** Duplicate customer_id field.\n")
                        success = False
                elif field == 'url':
                    if url is None:
                        url = value
                    else:
                        sys.stderr.write("*** Duplicate URL field.\n")
                        success = False
                else:
                    sys.stderr.write("*** Unknown field \"%s\".\n"%field)
                    success = False

                argument_index += 2

            if success:
                hs = host_schemes.HostSchemes(rest_api, secret)
                host_scheme = hs.modify(
                    host_scheme_id = host_scheme_id,
                    customer_id = customer_id,
                    url = url
                )

                if host_scheme is not None:
                    sys.stdout.write(
                        "host_scheme_id:           %d\n"
                        "customer_id:              %d\n"
                        "host:                     %s\n"
                        "scheme:                   %s\n"
                        "ssl_expiration_timestmap: %d\n"%(
                            host_scheme.host_scheme_id,
                            host_scheme.customer_id,
                            host_scheme.host,
                            str(host_scheme.scheme),
                            host_scheme.ssl_expiration_timestamp
                        )
                    )
                else:
                    sys.stderr.write("*** Could not modify host/scheme.\n")
                    success = False
        else:
            sys.stderr.write(
                "*** Invalid host/scheme ID %s\n"%argument
            )
            success = False
    else:
        sys.stderr.write("*** Invalid or missing parameters.\n")
        success = False

    return success


def host_scheme_delete(positional_arguments, arguments, rest_api, secret):
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
            host_scheme_id = int(positional_arguments[0])
        except:
            host_scheme_id = None

        if host_scheme_id is not None   and \
           host_scheme_id > 0           and \
           host_scheme_id <= 0xFFFFFFFF     :
            hs = host_schemes.HostSchemes(rest_api, secret)
            host_scheme = hs.get(host_scheme_id)
            if host_scheme is not None:
                success = hs.delete(host_scheme)
                if not success:
                    sys.stderr.write("*** Failed to delete host/scheme.\n")
                    success = False
            else:
                sys.stderr.write("*** Unknown host/scheme ID.\n")
                success = False
        else:
            sys.stderr.write("*** Invalid host/scheme ID.\n")
            success = False
    else:
        sys.stderr.write("*** You must provide a single host/scheme ID.\n")
        success = False

    return success


def host_scheme_purge(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the hs purge command.

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
            hs = host_schemes.HostSchemes(rest_api, secret)
            success = hs.purge(customer_id)
            if not success:
                sys.stderr.write("*** Failed to purge host/schemes.\n")
                success = False
        else:
            sys.stderr.write("*** Invalid customer ID.\n")
            success = False
    else:
        sys.stderr.write("*** You must provide a customer ID.\n")
        success = False

    return success


def host_scheme_list(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the hs list command.

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
        hs = host_schemes.HostSchemes(rest_api, secret)
        host_scheme_data = hs.list()
        if host_scheme_data is not None:
            __dump(host_scheme_data.values())
        else:
            sys.stderr.write("*** Failed to retrieve host/schemes.\n")
            success = False
    elif number_arguments == 1:
        try:
            customer_id = int(positional_arguments[0])
        except:
            customer_id = None

        if customer_id is not None   and \
           customer_id > 0           and \
           customer_id <= 0xFFFFFFFF     :
            hs = host_schemes.HostSchemes(rest_api, secret)
            host_scheme_data = hs.list(customer_id)
            if host_scheme_data is not None:
                __dump(host_scheme_data.values())
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


def __dump(host_scheme_data):
    """
    Function that dumps information about host/schemes.

    :param host_scheme_data:
        A list of all the host/scheme instances to be dumped.

    :type host_scheme_data: list of HostScheme instances

    """

    maximum_url_length = len("scheme://host")
    valid_data = list()
    invalid_data = list()

    for host_scheme in host_scheme_data:
        if not isinstance(host_scheme, int):
            valid_data.append(host_scheme)
            url = "%s://%s"%(
                str(host_scheme.scheme),
                host_scheme.host
            )
            maximum_url_length = max(maximum_url_length, len(url))
        else:
            invalid_data.append(host_scheme)

    for host_scheme_id in invalid_data:
        sys.stdout.write(
            "*** Unknown host scheme %d\n"%host_scheme_id
        )

    if valid_data:
        fmt_string = "| %%14d | %%11d | %%-%ds | %%24d |\n"%(
            maximum_url_length
        )

        fmt_head_string = "| %%14s | %%11s | %%-%ds | %%24s |\n"%(
            maximum_url_length
        )

        divider_string = (
              "+-"
            + "-" * 14 + "-+-"
            + "-" * 11 + "-+-"
            + "-" * maximum_url_length + "-+-"
            + "-" * 24 + "-+\n"
        )

        sys.stdout.write(divider_string)
        sys.stdout.write(
            fmt_head_string%(
                "host scheme id",
                "customer id",
                "scheme://host",
                "ssl expiration timestamp"
            )
        )

        sys.stdout.write(
              "+="
            + "=" * 14 + "=+="
            + "=" * 11 + "=+="
            + "=" * maximum_url_length + "=+="
            + "=" * 24 + "=+\n"
        )

        for host_scheme in valid_data:
            sys.stdout.write(
                fmt_string%(
                    host_scheme.host_scheme_id,
                    host_scheme.customer_id,
                    "%s://%s"%(
                        str(host_scheme.scheme).lower(),
                        host_scheme.host
                    ),
                    host_scheme.ssl_expiration_timestamp
                )
            )
            sys.stdout.write(divider_string)

###############################################################################
# Extension configuration:
#

COMMANDS = {
    'hs' : {
        'brief' : HOST_SCHEME_BRIEF,
        'help' : HOST_SCHEME_HELP,
        'subcommands' : {
            'get' : {
                'help' : HOST_SCHEME_GET_HELP,
                'execute' : host_scheme_get,
            },
            'create' : {
                'help' : HOST_SCHEME_CREATE_HELP,
                'execute' : host_scheme_create,
            },
            'modify' : {
                'help' : HOST_SCHEME_MODIFY_HELP,
                'execute' : host_scheme_modify,
            },
            'delete' : {
                'help' : HOST_SCHEME_DELETE_HELP,
                'execute' : host_scheme_delete,
            },
            'purge' : {
                'help' : HOST_SCHEME_PURGE_HELP,
                'execute' : host_scheme_purge,
            },
            'list' : {
                'help' : HOST_SCHEME_LIST_HELP,
                'execute' : host_scheme_list,
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
