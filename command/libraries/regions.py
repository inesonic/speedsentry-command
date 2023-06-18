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

import libraries.rest_api_common_v1 as rest_api_common_v1
import libraries.outbound_rest_api_v1 as outbound_rest_api_v1

###############################################################################
# Class Region:
#

class Region(object):
    """
    Class that encapsulates information about a single region.

    """

    def __init__(self, region_id, region_name):
        """
        Method that initializes the Region instance.

        :param region_id:
            The region's internal ID.

        :param region_name:
            The descriptive name for the region.

        :type region_id:   int
        :type region_name: str

        """

        super().__init__()

        self.__region_id = int(region_id)
        self.__region_name = str(region_name)


    @property
    def region_id(self):
        """
        Read-only property that holds the region ID.

        :type: int

        """

        return self.__region_id


    @property
    def region_name(self):
        """
        Read-write property that holds the region name.

        :type: int

        """

        return self.__region_name


    @region_name.setter
    def region_name(self, value):
        self.__region_name = str(value)

###############################################################################
# Class Regions:
#

class Regions(object):
    """
    Class that can be used to manage server regions.

    """

    def __init__(self, rest_api, secret):
        """
        Method that initializes the Regions class.

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


    def get(self, region_id):
        """
        Method you can use to obtain a region by region ID.

        :param region_id:
            The ID of the desired region.

        :return:
            Returns a Region instance holding information about the region.

        :type region_id: int
        :rtype:          Region

        """

        response = self.__rest_api.post_message(
            slug = "region/get",
            secret = self.__secret,
            message = { 'region_id' : region_id }
        )

        if response is not None and 'status' in response:
            status = response['status']
            if status == 'OK'             and \
               'region_id' in response    and \
                'region_name' in response     :
                result = Region(
                    region_id,
                    response['region_name']
                )
            else:
                result = None
        else:
            result = None

        return result


    def create(self, region_name):
        """
        Method you can use to add a new region.

        :param region_name:
            The desired name of the region.

        :return:
            Returns the newly created region instance.  None is returned on
            error.

        :type region_name: str
        :rtype:            Region or None

        """

        response = self.__rest_api.post_message(
            slug = "region/create",
            secret = self.__secret,
            message = { 'region_name' : region_name }
        )

        if response is not None and 'status' in response:
            status = response['status']
            if status == 'OK'            and \
               'region_id' in response   and \
               'region_name' in response     :
                try:
                   region_id = int(response['region_id'])
                except:
                    region_id = None

                if region_id is not None and region_id > 0:
                    result = Region(region_id, response['region_name'])
                else:
                    result = None
            else:
                result = None
        else:
            result = None

        return result


    def modify(self, region):
        """
        Method you can use to update information about a region.

        :param region:
            The modified region.

        :return:
            Returns true on success.  Returns false on error.

        :type region: Region
        :rtype:       bool

        """


        response = self.__rest_api.post_message(
            slug = "region/modify",
            secret = self.__secret,
            message = {
                'region_id' : region.region_id,
                'region_name' : region.region_name
            }
        )

        if response is not None and 'status' in response:
            status = response['status']
            if status == 'OK':
                result = True
            else:
                result = False
        else:
            result = False

        return result


    def delete(self, region):
        """
        Method you can use to delete a region.  Note that deleting a region
        will also cause all servers associated with that region to be deleted
        as well as any customer data collected by those servers.

        Use this method with care.

        :param region:
            The region to be deleted.

        :return:
            Returns true on success.  Returns false on error.

        :type region: Region
        :rtype:       bool

        """

        response = self.__rest_api.post_message(
            slug = "region/delete",
            secret = self.__secret,
            message = { 'region_id' : region.region_id }
        )

        if response is not None and 'status' in response:
            status = response['status']
            if status == 'OK':
                result = True
            else:
                result = False
        else:
            result = False

        return result


    def get_all(self):
        """
        Method you can use to obtain a list of all regions.

        :return:
            Returns a dictionary holding all region names indexed by region ID.
            None is returned if an error occurs.

        :rtype: dict or None

        """

        response = self.__rest_api.post_message(
            slug = "region/list",
            secret = self.__secret,
            message = { }
        )

        if response is not None and 'status' in response:
            status = response['status']
            if status == 'OK' and 'regions' in response:
                result = dict()
                regions_data = response['regions']
                try:
                    result = { int(k) : v for k,v in regions_data.items() }
                except:
                    result = None
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
