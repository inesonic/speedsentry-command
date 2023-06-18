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
Class providing a API you can use to process customer information.

"""

###############################################################################
# Import:
#

import sys
import base64

import libraries.customers as customers
import libraries.rest_api_common_v1 as rest_api_common_v1
import libraries.outbound_rest_api_v1 as outbound_rest_api_v1

###############################################################################
# Globals:
#

CUSTOMER_BRIEF = "Allows you to add, remove, modify and list customers."
"""
Brief description for the customers command.

"""

CUSTOMER_HELP = """
The customer command allows you to manipulate customer data as seen by the
database controller and polling servers.  The customer command supports the
following subcommands:

  customer get <customer id> [<customer id> [<customer id> ...]]
    Gets a customer by customer ID.

  customer update <customer id> <number monitors> <expiration days>
                  [ <capability> [ <capability> [ <capability> ... ]]]
    Creates or updates a customer with the specified capabilities.

  customer delete <customer id>
    Deletes a customer and all information tied to this customer.

  customer purge <customer id> [ <customer id> [ <customer id> ... ]]
    Deletes a groupd of customer IDs.

  customer list
    Generates a list of every known customer.

  customer gets <customer id>
    Gets the REST API secrets for a specific customer.

  customer resets <customer id>
    Resets the REST API secrets for a specific customer.

  customer pause <customer id>
    Pause polling for a specific customer.

  customer resume <customer id>
    Resumes polling for a specific customer after the customer was paused.

"""
"""
Help text for this extension.

"""

CUSTOMER_GET_HELP = """
The customer get command allows you to view information regarding one or more
customers.  The syntax for the command is:

  customer get <customer id> [ <customer id> [ customer id> ... ]]

Where <customer id> represents the numeric customer ID for a given customer.

The data will be presented in a tabulated format.

"""
"""
Help text for this extension.

"""

CUSTOMER_UPDATE_HELP = """
The customer update command allows you to create a new database entry for a
customer or update an existing database entry for a customer.

  customer update <customer id> <number monitors> <polling interval>
                  <expiration days> [ <capability> [ <capability>
                  [ <capability> ... ]]]

Where:
    <customer id> -      The internal customer ID.

    <number monitors> -  The maximum number of monitors this customer can
                         deploy.

    <polling interval> - The polling interval, per monitor, in seconds.

    <expiration days> -  The expiration time for customer latency data, in
                         days.

The <capability> fields are names for specific capabilities to be enabled.
Supported capabilities are:

+--------------------+--------------------------------------------------------+
| Capability         | Function                                               |
+====================+========================================================+
| active             | If included, then the customer will be marked as       |
|                    | active.  If excluded, then the customer will be marked |
|                    | inactive and will not be serviced.                     |
+--------------------+--------------------------------------------------------+
| multi_region       | If included, then the customer will have latency       |
|                    | measured across multiple regions.                      |
+--------------------+--------------------------------------------------------+
| wordpress          | If included, then the customer WordPress API will be   |
|                    | enabled.                                               |
+--------------------+--------------------------------------------------------+
| rest_api           | If included, then the customer REST API will be        |
|                    | enabled.  A secret will be generated for the customer  |
|                    | if no secret already exists.                           |
+--------------------+--------------------------------------------------------+
| content_checking   | If included, then content checking will be enabled for |
|                    | the customer.  This specifically enables only basic    |
|                    | content checking.                                      |
+--------------------+--------------------------------------------------------+
| keyword_checking   | If included, then keyword checking will be enabled for |
|                    | the customer.                                          |
+--------------------+--------------------------------------------------------+
| post_method        | If included, then the customer and use POST method to  |
|                    | monitor remote endpoints.                              |
+--------------------+--------------------------------------------------------+
| latency_tracking   | If included, then latency data will be collected.      |
+--------------------+--------------------------------------------------------+
| ssl_checking       | If included, then SSL certificate expiration date/time |
|                    | values will be collected.                              |
+--------------------+--------------------------------------------------------+
| ping_checking      | If included, then ping based testing will be performed |
|                    | from a single region.                                  |
+--------------------+--------------------------------------------------------+
| blacklist_checking | If included, then blacklists will be scanned           |
|                    | periodically.                                          |
+--------------------+--------------------------------------------------------+
| domain_checking    | If included, then domain expiration date/time checking |
|                    | will be performed.                                     |
+--------------------+--------------------------------------------------------+
| maintenance_mode   | If included then the customer will be allowed to use   |
|                    | maintenance mode.                                      |
+--------------------+--------------------------------------------------------+
| rollups            | If included then the customer can receive rollups.     |
+--------------------+--------------------------------------------------------+

"""
"""
Help text for this extension.

"""

CUSTOMER_DELETE_HELP = """
The customer delete command allows you to delete a customer from the system.
Note that deleting a customer will also delete all data associated with that
customer.

  customer delete <customer id>

"""
"""
Help text for this extension.

"""

CUSTOMER_PURGE_HELP = """
The customer purge command allows you to delete multiple customers at once in
an efficient manner.  Note that deleting a customer will also delete all data
associated with that customer.

  customer purge <customer id> [ <customer id> [ <customer id> ... ]]

"""
"""
Help text for this extension.

"""

CUSTOMER_LIST_HELP = """
The customer list command allows you to list all customers.

  customer list
"""
"""
Help text for this extension.

"""

CUSTOMER_GETS_HELP = """
The customer gets command allows you to obtain the secrets for a customer REST
API account.  The syntax for the command is:

  customer gets <customer id>

Where <customer id> represents the numeric customer ID for a given customer.

"""
"""
Help text for this extension.

"""

CUSTOMER_RESETS_HELP = """
The customer resets command allows you to reset the secrets for a customer REST
API account.  The syntax for the command is:

  customer resets <customer id>

Where <customer id> represents the numeric customer ID for a given customer.

"""
"""
Help text for this extension.

"""

CUSTOMER_PAUSE_HELP = """
The customer pause command allows you to pause polling for a specific customer.
The syntax for the command is:

  customer pause <customer id>

Where <customer id> represents the numeric customer ID for a given customer.

"""
"""
Help text for this extension.

"""

CUSTOMER_RESUME_HELP = """
The customer resume command allows you to resume polling for a specific
customer.  The syntax for the command is:

  customer resume <customer id>

Where <customer id> represents the numeric customer ID for a given customer.

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


def customer_get(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the customer get command.

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
        customer_ids = list()
        i = 0
        while success and i < number_arguments:
            argument = positional_arguments[i]
            try:
                customer_id = int(argument)
            except:
                customer_id = None

            if customer_id is None or customer_id < 0:
                sys.stderr.write(
                    "*** Invalid customer ID %s\n"%argument
                )
                success = False
            else:
                i += 1
                customer_ids.append(customer_id)

        customers_data = list()
        c = customers.Customers(rest_api, secret)
        for customer_id in customer_ids:
            customer_data = c.get(customer_id)
            if customer_data is not None:
                customers_data.append(customer_data)
            else:
                sys.stdout.write(
                    "%5d *** Invalid customer ID ***\n"%customer_id
                )

        __dump(customers_data)
    else:
        sys.stderr.write("*** You must provide at least one region ID.\n")
        success = False

    return success


def customer_update(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the customer update command.

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
    if number_arguments >= 4:
        try:
            customer_id = int(positional_arguments[0])
            maximum_number_monitors = int(positional_arguments[1])
            polling_interval = int(positional_arguments[2])
            expiration_days = int(positional_arguments[3])
        except:
            customer_id = None
            maximum_number_monitors = None
            polling_interval = None
            expiration_days = None

        if customer_id is not None     and \
           customer_id > 0             and \
           maximum_number_monitors > 0 and \
           expiration_days >= 0            :
            customer_active = False
            multi_region_checking = False
            supports_wordpress = False
            supports_rest_api = False
            supports_content_checking = False
            supports_keyword_checking = False
            supports_post_method = False
            supports_latency_tracking = False
            supports_ssl_expiration_checking = False
            supports_ping_based_polling = False
            supports_blacklist_checking = False
            supports_domain_expiration_checking = False
            supports_maintenance_mode = False
            supports_rollups = False

            i = 4
            while success and i < number_arguments:
                arg = positional_arguments[i].strip().lower().replace('-', '_')
                if   arg == 'active':
                    customer_active = True
                elif arg == 'multi_region':
                    multi_region_checking = True
                elif arg == 'wordpress':
                    supports_wordpress = True
                elif arg == 'rest_api':
                    supports_rest_api = True
                elif arg == 'content_checking':
                    supports_content_checking = True
                elif arg == 'keyword_checking':
                    supports_keyword_checking = True
                elif arg == 'post_method':
                    supports_post_method = True
                elif arg == 'latency_tracking':
                    supports_latency_tracking = True
                elif arg == 'ssl_checking':
                    supports_ssl_expiration_checking = True
                elif arg == 'ping_checking':
                    supports_ping_based_polling = True
                elif arg == 'blacklist_checking':
                    supports_blacklist_checking = True
                elif arg == 'domain_checking':
                    supports_domain_expiration_checking = True
                elif arg == 'maintenance_mode':
                    supports_maintenance_mode = True
                elif arg == 'rollups':
                    supports_rollups = True
                else:
                    sys.stderr.write(
                        "*** Invalid parameter: %s\n"%positional_arguments[i]
                    )
                    success = False

                i += 1

            if success:
                c = customers.Customers(rest_api, secret)
                customer_data = c.update(
                    customer_id,
                    maximum_number_monitors,
                    polling_interval,
                    expiration_days,
                    customer_active,
                    multi_region_checking,
                    supports_wordpress,
                    supports_rest_api,
                    supports_content_checking,
                    supports_keyword_checking,
                    supports_post_method,
                    supports_latency_tracking,
                    supports_ssl_expiration_checking,
                    supports_ping_based_polling,
                    supports_blacklist_checking,
                    supports_domain_expiration_checking,
                    supports_maintenance_mode,
                    supports_rollups
                )

                if customer_data is not None:
                    __dump([ customer_data ])
                else:
                    sys.stderr.write("*** Failed to create customer.\n")
                    success = False
        else:
            sys.stderr.write("*** Invalid numeric parameter.\n")
            success = False
    else:
        sys.stderr.write("*** You must provide at least one region name.\n")
        success = False

    return success


def customer_delete(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the customer delete command.

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

        if customer_id is not None and customer_id > 0:
            c = customers.Customers(rest_api, secret)
            customer = c.get(customer_id)
            if customer is not None:
                success = c.delete(customer)
                if not success:
                    sys.stderr.write(
                        "*** Could not delete customer %d\n"%customer_id
                    )
            else:
                success = False
                sys.stderr.write(
                    "*** Could not locate customer %d\n"%customer_id
                )
        else:
            success = False
            sys.stderr.write("*** Invalid customer ID.\n")
    else:
        sys.stderr.write("*** You must provide a single customer ID.\n")
        success = False

    return success


def customer_purge(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the customer purge command.

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
        c = customers.Customers(rest_api, secret)
        success = c.purge(customer_list)

        if not success:
            sys.stderr.write("*** Failed to purge customers.\n")

    return success


def customer_list(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the customer list command.

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
    if len(positional_arguments) == 0:
        c = customers.Customers(rest_api, secret)
        customers_dict = c.get_all()
        if customers_dict is not None:
            __dump(customers_dict.values())
        else:
            sys.stderr.write(
                "*** Failed to get customer data.\n"
            )
            success = False
    else:
        sys.stderr.write(
            "*** Command customer list does not accept arguments.\n"
        )
        success = False

    return success


def customer_gets(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the customer gets command.

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

        if customer_id is not None and customer_id > 0:
            c = customers.Customers(rest_api, secret)
            secrets = c.get_secret(customer_id)
            if secrets is not None:
                sys.stdout.write(
                    "identifier: %s\n"%secrets[0]
                )
                sys.stdout.write(
                    "secret:     %s (base64 encoded)\n"%(
                        base64.b64encode(secrets[1])
                    )
                )
            else:
                success = False
                sys.stderr.write(
                    "*** Could not locate customer %d\n"%customer_id
                )
        else:
            success = False
            sys.stderr.write("*** Invalid customer ID.\n")
    else:
        sys.stderr.write("*** You must provide a single customer ID.\n")
        success = False

    return success


def customer_resets(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the customer resets command.

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

        if customer_id is not None and customer_id > 0:
            c = customers.Customers(rest_api, secret)
            success = c.reset_secret(customer_id)
            if not success:
                sys.stderr.write(
                    "*** Failed to reset customer secret %d\n"%customer_id
                )
        else:
            success = False
            sys.stderr.write("*** Invalid customer ID.\n")
    else:
        sys.stderr.write("*** You must provide a single customer ID.\n")
        success = False

    return success


def customer_pause(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the customer pause command.

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

        if customer_id is not None and customer_id > 0:
            c = customers.Customers(rest_api, secret)
            success = c.pause(customer_id, True)
            if not success:
                sys.stderr.write(
                    "*** Failed to pause customer %d\n"%customer_id
                )
        else:
            success = False
            sys.stderr.write("*** Invalid customer ID.\n")
    else:
        sys.stderr.write("*** You must provide a single customer ID.\n")
        success = False

    return success


def customer_resume(positional_arguments, arguments, rest_api, secret):
    """
    Function that handles the customer resume command.

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

        if customer_id is not None and customer_id > 0:
            c = customers.Customers(rest_api, secret)
            success = c.pause(customer_id, False)
            if not success:
                sys.stderr.write(
                    "*** Failed to pause customer %d\n"%customer_id
                )
        else:
            success = False
            sys.stderr.write("*** Invalid customer ID.\n")
    else:
        sys.stderr.write("*** You must provide a single customer ID.\n")
        success = False

    return success


def __dump(customers_capabilities):
    """
    Method used internally to dump customer data.

    :param customers_capabilities:
       A list of Customer instances to be dumped.

    :type customers_capabilities: list

    """

    h = "+---------+--------------+---------------+------------+--------+---" \
        "-----------+-----------+----------+---------+----------+-----------" \
        "--+---------+-------+--------+----------+--------+-----------------" \
        "-+---------+--------+\n"
    s = h + \
        "| ID      | num monitors | poll interval | expiration | active | mu" \
        "lti-region | wordpress | rest-api | content | keywords | post-metho" \
        "d | latency | ssl   | ping  | blacklist | domain | maintenance-mode" \
        " | rollups | paused |\n" \
        "+=========+==============+===============+============+========+===" \
        "===========+===========+==========+=========+==========+===========" \
        "==+=========+=======+========+==========+========+=================" \
        "=+=========+========+\n"

    sys.stdout.write(s)

    for cc in customers_capabilities:
        sys.stdout.write(
            "| %7d | %12d | %13d | %10d | "%(
                cc.customer_id,
                cc.maximum_number_monitors,
                cc.polling_interval,
                cc.expiration_days
            )
        )
        sys.stdout.write(
            "%-6s | %-12s | %-9s | %-8s | %-7s | %-8s | %-11s | %-7s | %-5s "
            "| %-5s | %-9s | %-6s | %-16s | %-7s | %-6s |\n"%(
                str(cc.customer_active),
                str(cc.multi_region_checking),
                str(cc.supports_wordpress),
                str(cc.supports_rest_api),
                str(cc.supports_content_checking),
                str(cc.supports_keyword_checking),
                str(cc.supports_post_method),
                str(cc.supports_latency_tracking),
                str(cc.supports_ssl_expiration_checking),
                str(cc.supports_ping_based_polling),
                str(cc.supports_blacklist_checking),
                str(cc.supports_domain_expiration_checking),
                str(cc.supports_maintenance_mode),
                str(cc.supports_rollups),
                str(cc.paused)
            )
        )
        sys.stdout.write(h)

###############################################################################
# Extension configuration:
#

COMMANDS = {
    'customer' : {
        'brief' : CUSTOMER_BRIEF,
        'help' : CUSTOMER_HELP,
        'subcommands' : {
            'get' : {
                'help' : CUSTOMER_GET_HELP,
                'execute' : customer_get
            },
            'update' : {
                'help' : CUSTOMER_UPDATE_HELP,
                'execute' : customer_update
            },
            'delete' : {
                'help' : CUSTOMER_DELETE_HELP,
                'execute' : customer_delete
            },
            'purge' : {
                'help' : CUSTOMER_PURGE_HELP,
                'execute' : customer_purge
            },
            'list' : {
                'help' : CUSTOMER_LIST_HELP,
                'execute' : customer_list
            },
            'gets' : {
                'help' : CUSTOMER_GETS_HELP,
                'execute' : customer_gets
            },
            'resets' : {
                'help' : CUSTOMER_RESETS_HELP,
                'execute' : customer_resets
            },
            'pause' : {
                'help' : CUSTOMER_PAUSE_HELP,
                'execute' : customer_pause
            },
            'resume' : {
                'help' : CUSTOMER_RESUME_HELP,
                'execute' : customer_resume
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
