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

import libraries.regions as regions
import libraries.rest_api_common_v1 as rest_api_common_v1
import libraries.outbound_rest_api_v1 as outbound_rest_api_v1

###############################################################################
# Globals:
#

REGION_BRIEF = "Allows you to add, remove, modify and list regions."
"""
Brief description for the region command.

"""

REGION_HELP = """
The region command allows you to manipulate regions.  The region command
supports the following subcommands:

  region get <region ID> [<region ID> [<region ID> ...]]
    Gets a region by region ID.

  region create <region name> [<region name> [<region name> ...]]
    Creates a new region description.

  region modify <region ID> <region description>
    Modifies the description of a region.

  region delete <region ID>
    Deletes a region by region ID.

  region list
    Generates a list of every know region.
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


def region_get(positional_arguments, arguments, rest_api, secret):
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
        region_ids = list()
        i = 0
        while success and i < number_arguments:
            argument = positional_arguments[i]
            try:
                region_id = int(argument)
            except:
                region_id = None

            if region_id is None or region_id < 0:
                sys.stderr.write(
                    "*** Invalid region ID %s\n"%argument
                )
                success = False
            else:
                i += 1
                region_ids.append(region_id)

        r = regions.Regions(rest_api, secret)
        for region_id in region_ids:
            region_data = r.get(region_id)
            if region_data is not None:
                sys.stdout.write(
                    "%5d %s\n"%(
                        region_data.region_id,
                        region_data.region_name
                    )
                )
            else:
                sys.stdout.write(
                    "%5d *** Invalid Region ***\n"%region_id
                )
    else:
        sys.stderr.write("*** You must provide at least one region ID.\n")
        success = False

    return success


def region_create(positional_arguments, arguments, rest_api, secret):
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
    if len(positional_arguments) > 0:
        r = regions.Regions(rest_api, secret)
        for region_name in positional_arguments:
            region_data = r.create(region_name)
            if region_data is not None:
                sys.stdout.write(
                    "%5d %s\n"%(
                        region_data.region_id,
                        region_data.region_name
                    )
                )
            else:
                sys.stdout.write(
                    "%5d *** Invalid Region ***\n"%region_id
                )
    else:
        sys.stderr.write("*** You must provide at least one region name.\n")
        success = False

    return success


def region_modify(positional_arguments, arguments, rest_api, secret):
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
    if len(positional_arguments) == 2:
        try:
            region_id = int(positional_arguments[0])
        except:
            region_id = None

        if region_id is None or region_id < 0:
            sys.stderr.write(
                "*** Invalid region ID %s\n"%argument
            )
            success = False
        else:
            region_name = positional_arguments[1]

        r = regions.Regions(rest_api, secret)
        region_data = r.get(region_id)
        if region_data is not None:
            region_data.region_name = region_name
            success = r.modify(region_data)
            if not success:
                sys.stderr.write(
                    "*** Could not modify region %d\n"%region_id
                )
                success = False
        else:
            sys.stderr.write(
                "*** Region %d is does not exists.\n"%region_id
            )
            success = False
    else:
        sys.stderr.write("*** You must provide a region ID and region name.\n")
        success = False

    return success


def region_delete(positional_arguments, arguments, rest_api, secret):
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

    number_arguments = len(positional_arguments)
    success = True
    if number_arguments > 0:
        region_ids = list()
        i = 0
        while success and i < number_arguments:
            argument = positional_arguments[i]
            try:
                region_id = int(argument)
            except:
                region_id = None

            if region_id is None or region_id < 0:
                sys.stderr.write(
                    "*** Invalid region ID %s\n"%argument
                )
                success = False
            else:
                i += 1
                region_ids.append(region_id)

        r = regions.Regions(rest_api, secret)
        for region_id in region_ids:
            region_data = r.get(region_id)
            if region_data is not None:
                success = r.delete(region_data)
                if success:
                    sys.stdout.write(
                        "deleted %5d %s\n"%(
                            region_data.region_id,
                            region_data.region_name
                        )
                    )
                else:
                    sys.stdout.write(
                        "failed  %5d %s\n"%(
                            region_data.region_id,
                            region_data.region_name
                        )
                    )
            else:
                sys.stdout.write(
                    "%5d *** Invalid Region ***\n"%region_id
                )
    else:
        sys.stderr.write("*** You must provide at least one region ID.\n")
        success = False

    return success


def region_list(positional_arguments, arguments, rest_api, secret):
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
    if len(positional_arguments) == 0:
        r = regions.Regions(rest_api, secret)
        regions_data = r.get_all()
        if regions_data is not None:
            for region_id, region_name in regions_data.items():
                sys.stdout.write("%5d %s\n"%(region_id, region_name))
        else:
            sys.stderr.write(
                "*** Failed to get regions data.\n"
            )
        success = False
    else:
        sys.stderr.write(
            "*** Command region list does not accept arguments.\n"
        )
        success = False

    return success

###############################################################################
# Extension configuration:
#

COMMANDS = {
    'region' : {
        'brief' : REGION_BRIEF,
        'help' : REGION_HELP,
        'subcommands' : {
            'get' : {
                'help' : REGION_HELP,
                'execute' : region_get,
            },
            'create' : {
                'help' : REGION_HELP,
                'execute' : region_create,
            },
            'modify' : {
                'help' : REGION_HELP,
                'execute' : region_modify,
            },
            'delete' : {
                'help' : REGION_HELP,
                'execute' : region_delete,
            },
            'list' : {
                'help' : REGION_HELP,
                'execute' : region_list,
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
