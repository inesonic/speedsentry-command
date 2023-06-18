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
import os
import json
import base64
import time
import datetime

import libraries.rest_api_common_v1 as rest_api_common_v1
import libraries.outbound_rest_api_v1 as outbound_rest_api_v1

###############################################################################
# Class Customer:
#

class Customer(object):
    """
    Class that encapsulates information about a single customer.

    """

    def __init__(
        self,
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
        supports_rollups,
        paused
        ):
        """
        Method that initializes the Region instance.

        :param customer_id:
            The customer ID for this customer.

        :param maximum_number_monitors:
            The maximum number of monitors this customer can use.

        :param polling_interval:
            The polling interval for this customer.

        :param expiration_days:
            The maximum number of days customer latency data will reside on our
            servers before being expunged.

        :param customer_active:
            If True, then the customer is active.  If False, then the customer
            is not active.  An active customer is one that has a valid
            subscription and has confirmed their email address.

        :param multi_region_checking:
            If True, then latency measurements will be taken across multiple
            regions.  If False, only a single randomly selected region will be
            used.

        :param supports_wordpress:
            If True, then the WordPress REST API is enabled.  If False, then
            the WordPress REST API is disabled.

        :param supports_rest_api:
            If True, then the customer REST API is enabled.  If False, then the
            customer REST API is disabled.

        :param supports_content_checking:
            If True, then content match checking is enabled.  If False, then
            content match checking is disabled.

        :param supports_keyword_checking:
            If True, then keyword checking is enabled.  If False, the keyword
            checking is disabled.

        :param supports_post_method:
            If True, then the customer can use POST method to check REST APIs.

        :param supports_latency_tracking:
            If True, then latency tracking is supported and will be performed
            automatically.  If False, then no latency tracking will be
            performed.

        :param supports_ssl_expiration_checking:
            If True, then the SSL expiration date/time will be checked.  If
            False, then the SSL expiratin date/time will not be checked.

        :param supports_ping_based_polling:
            If True, then ping based monitoring will be enabled.  If False,
            then ping based polling will not be enabled.

        :param supports_blacklist_checking:
            If True, then blacklist checking will be enabled.  If False, then
            blacklist checking will not be enabled.

        :param supports_domain_expiration_checking:
            If True, then the domain expiration date/time will be checked. If
            False, then no domain expiration checking will be performed.

        :param supports_maintenance_mode:
            If True, then the customer supports a maintenance mode settings.
            If False, then maintenance mode is not supported.

        :param supports_rollups:
            If True, then the customer account allows for weekly rollups.  If
            False, then rollups are not to be supported.

        :param paused:
            If True, then the customer is in maintenance mode. If False, the
            customer is not in maintenance mode.

        :type customer_id:                         int
        :type maximum_number_monitors:             int
        :type polling_interval:                    int
        :type expiration_days:                     int
        :type customer_active:                     bool
        :type multi_region_checking:               bool
        :type supports_wordpress:                  bool
        :type supports_rest_api:                   bool
        :type supports_content_checking:           bool
        :type supports_keyword_checking:           bool
        :type supports_post_method:                bool
        :type supports_latency_tracking:           bool
        :type supports_ssl_expiration_checking:    bool
        :type supports_ping_based_polling:         bool
        :type supports_blacklist_checking:         bool
        :type supports_domain_expiration_checking: bool
        :type supports_maintenance_mode:           bool
        :type supports_rollups:                    bool
        :type paused:                              bool

        """

        super().__init__()

        self.__customer_id = int(customer_id)
        self.__maximum_number_monitors = int(maximum_number_monitors)
        self.__polling_interval = int(polling_interval)
        self.__expiration_days = int(expiration_days)
        self.__customer_active = bool(customer_active)
        self.__multi_region_checking = bool(multi_region_checking)
        self.__supports_wordpress = bool(supports_wordpress)
        self.__supports_rest_api = bool(supports_rest_api)
        self.__supports_content_checking = bool(supports_content_checking)
        self.__supports_keyword_checking = bool(supports_keyword_checking)
        self.__supports_post_method = bool(supports_post_method)
        self.__supports_latency_tracking = bool(supports_latency_tracking)
        self.__supports_ssl_expiration_checking = bool(
            supports_ssl_expiration_checking
        )
        self.__supports_ping_based_polling = bool(supports_ping_based_polling)
        self.__supports_blacklist_checking = bool(supports_blacklist_checking)
        self.__supports_domain_expiration_checking = bool(
            supports_domain_expiration_checking
        )
        self.__supports_maintenance_mode = bool(supports_maintenance_mode)
        self.__supports_rollups = bool(supports_rollups)
        self.__paused = bool(paused)


    @property
    def customer_id(self):
        """
        Read-only property that holds the customer_id.

        :type: int

        """

        return self.__customer_id


    @property
    def maximum_number_monitors(self):
        """
        Property that holds the maximum number of monitors this customer can
        deploy.

        :type: int

        """

        return self.__maximum_number_monitors


    @maximum_number_monitors.setter
    def maximum_number_monitors(self, value):
        self.__maximum_number_monitors = int(value)


    @property
    def polling_interval(self):
        """
        Property that holds the polling interval for this customer.

        :type: int

        """

        return self.__polling_interval


    @polling_interval.setter
    def polling_interval(self, value):
        self.__polling_interval = int(value)


    @property
    def expiration_days(self):
        """
        Property that holds the customer latency data expiration time, in days.

        :type: bool

        """

        return self.__expiration_days


    @expiration_days.setter
    def expiration_days(self, value):
        self.__expiration_days = bool(value)


    @property
    def customer_active(self):
        """
        Property that holds True if the customer is active.

        :type: bool

        """

        return self.__customer_active


    @customer_active.setter
    def customer_active(self, value):
        self.__customer_active = bool(value)


    @property
    def multi_region_checking(self):
        """
        Property that holds True if latency is measured across multiple
        regions.

        :type: bool

        """

        return self.__multi_region_checking


    @multi_region_checking.setter
    def multi_region_checking(self, value):
        self.__multi_region_checking = bool(value)


    @property
    def supports_wordpress(self):
        """
        Property that holds True if the customer WordPress API in enabled.

        :type: bool

        """

        return self.__supports_wordpress


    @supports_wordpress.setter
    def supports_wordpress(self, value):
        self.__supports_wordpress = bool(value)


    @property
    def supports_rest_api(self):
        """
        Property that holds True if the customer REST API is enabled.

        :type: bool

        """

        return self.__supports_rest_api


    @supports_rest_api.setter
    def supports_rest_api(self, value):
        self.__supports_rest_api = bool(value)


    @property
    def supports_content_checking(self):
        """
        Property that holds True if content match checking is enabled for this
        customer.

        :type: bool

        """

        return self.__supports_content_checking


    @supports_content_checking.setter
    def supports_content_checking(self, value):
        self.__supports_content_checking = bool(value)


    @property
    def supports_keyword_checking(self):
        """
        Property that holds True if keyword checking is enabled for this
        customer.

        :type: bool

        """

        return self.__supports_keyword_checking


    @supports_keyword_checking.setter
    def supports_keyword_checking(self, value):
        self.__supports_keyword_checking = bool(value)


    @property
    def supports_post_method(self):
        """
        Property that holds True if the customer can configure and use POST
        based messages.

        :type: bool

        """

        return self.__supports_post_method


    @supports_post_method.setter
    def supports_post_method(self, value):
        self.__supports_post_method = bool(value)


    @property
    def supports_latency_tracking(self):
        """
        Property that holds True if latency tracking is enabled for this
        customer.

        :type: bool

        """

        return self.__supports_latency_tracking


    @supports_latency_tracking.setter
    def supports_latency_tracking(self, value):
        self.__supports_latency_tracking = bool(value)


    @property
    def supports_ssl_expiration_checking(self):
        """
        Property that holds True if SSL certificate expiration checking is
        enabled for this customer.

        :type: bool

        """

        return self.__supports_ssl_expiration_checking


    @supports_ssl_expiration_checking.setter
    def supports_ssl_expiration_checking(self, value):
        self.__supports_ssl_expiration_checking = bool(value)


    @property
    def supports_ping_based_polling(self):
        """
        Property that holds True if ping based polling is enabled for this
        customer.

        :type: bool

        """

        return self.__supports_ping_based_polling


    @supports_ping_based_polling.setter
    def supports_ping_based_polling(self, value):
        self.__supports_ping_based_polling = bool(value)


    @property
    def supports_blacklist_checking(self):
        """
        Property that holds True if blacklist checking is enabled for this
        customer.

        :type: bool

        """

        return self.__supports_blacklist_checking


    @supports_blacklist_checking.setter
    def supports_blacklist_checking(self, value):
        self.__supports_blacklist_checking = bool(value)


    @property
    def supports_domain_expiration_checking(self):
        """
        Property that holds True if domain expiration checking is enabled for
        this customer.

        :type: bool

        """

        return self.__supports_domain_expiration_checking


    @supports_domain_expiration_checking.setter
    def supports_domain_expiration_checking(self, value):
        self.__supports_domain_expiration_checking = bool(value)


    @property
    def supports_maintenance_mode(self):
        """
        Property that holds True if maintenance mode is supported for this
        customer.

        :type: bool

        """

        return self.__supports_maintenance_mode


    @supports_maintenance_mode.setter
    def supports_maintenance_mode(self, value):
        self.__supports_maintenance_mode = bool(value)


    @property
    def supports_rollups(self):
        """
        Property that holds True if weekly rollups should be supported for this
        customer.

        :type: bool

        """

        return self.__supports_rollups


    @supports_rollups.setter
    def supports_rollups(self, value):
        self.__supports_rollups = bool(value)


    @property
    def paused(self):
        """
        Read-only property that holds True if the customer is in maintenance
        mode.

        :type: bool

        """

        return self.__paused

###############################################################################
# Class Customers:
#

class Customers(object):
    """
    Class that can be used to manage customer data.

    """

    def __init__(self, rest_api, secret):
        """
        Method that initializes the Customers class.

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


    def get(self, customer_id):
        """
        Method you can use to obtain customer data by customer ID.

        :param customer_id:
            The ID of the desired customer.

        :return:
            Returns a Customer instance holding information about the customer.
            A value of None is returned on error.  A value of False is returned
            if the customer does not exist.

        :type customer_id: int
        :rtype:            Customer

        """

        response = self.__rest_api.post_message(
            slug = "customer/get",
            secret = self.__secret,
            message = { 'customer_id' : customer_id }
        )

        if response is not None and 'status' in response:
            status = response['status']
            if status == 'OK' and 'customer' in response:
                result = self.__parse_response(response['customer'])
            else:
                result = False
        else:
            result = None

        return result


    def update(
        self,
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
        ):
        """
        Method you can use to add a new customer or update an existing
        customer.

        :param customer_id:
            The ID that has been assigned to this customer.

        :param maximum_number_monitors:
            The maximum number of monitors this customer can use.

        :param polling_interval:
            The per-monitor polling interval.

        :param expiration_days:
            The maximum number of days customer latency data will reside on our
            servers before being expunged.

        :param customer_active:
            If True, then the customer has been enabled.  If False, then the
            customer is currently disabled.  Customers are enabled when they
            have a valid subscription and have confirmed their email address.

        :param multi_region_checking:
            If True, then latency measurements will be taken across multiple
            regions.  If False, only a single randomly selected region will be
            used.

        :param supports_wordpress:
            If True, then the WordPress REST API is enabled.  If False, then
            the WordPress REST API is disabled.

        :param supports_rest_api:
            If True, then the customer REST API is enabled.  If False, then the
            customer REST API is disabled.

        :param supports_content_checking:
            If True, then content match checking is enabled.  If False, then
            content match checking is disabled.

        :param supports_keyword_checking:
            If True, then keyword checking is enabled.  If False, the keyword
            checking is disabled.

        :param supports_post_method:
            If True, then the customer can use POST method to check REST APIs.

        :param supports_latency_tracking:
            If True, then latency tracking is supported and will be performed
            automatically.  If False, then no latency tracking will be
            performed.

        :param supports_ssl_expiration_checking:
            If True, then the SSL expiration date/time will be checked.  If
            False, then the SSL expiratin date/time will not be checked.

        :param supports_ping_based_polling:
            If True, then ping based monitoring will be enabled.  If False,
            then ping based polling will not be enabled.

        :param supports_blacklist_checking:
            If True, then blacklist checking will be enabled.  If False, then
            blacklist checking will not be enabled.

        :param supports_domain_expiration_checking:
            If True, then the domain expiration date/time will be checked. If
            False, then no domain expiration checking will be performed.

        :param supports_maintenance_mode:
            If True, then the customer can use maintenance mode.  If False,
            then the customer can-not use maintenance mode.

        :param supports_rollups:
            If True, then the customer can enable and receive weekly rollups.
            If False, then rollups are not supported.

        :return:
            Returns a new Customer instance on success.  None is returned on
            error.

        :type customer_id:                         int
        :type maximum_number_monitors:             int
        :type polling_interval:                    int
        :type expiration_days:                     int
        :type customer_active:                     bool
        :type multi_region_checking:               bool
        :type supports_wordpress:                  bool
        :type supports_rest_api:                   bool
        :type supports_content_checking:           bool
        :type supports_keyword_checking:           bool
        :type supports_post_method:                bool
        :type supports_latency_tracking:           bool
        :type supports_ssl_expiration_checking:    bool
        :type supports_ping_based_polling:         bool
        :type supports_blacklist_checking:         bool
        :type supports_domain_expiration_checking: bool
        :type supports_maintenance_mode:           bool
        :type supports_rollups:                    bool
        :rtype:                                    Customer or None

        """

        response = self.__rest_api.post_message(
            slug = "customer/create",
            secret = self.__secret,
            message = {
                'customer_id' :
                    int(customer_id),
                'maximum_number_monitors' :
                    int(maximum_number_monitors),
                'polling_interval' :
                    int(polling_interval),
                'expiration_days' :
                    int(expiration_days),
                'customer_active' :
                    bool(customer_active),
                'multi_region_checking' :
                    bool(multi_region_checking),
                'supports_wordpress' :
                    bool(supports_wordpress),
                'supports_rest_api' :
                    bool(supports_rest_api),
                'supports_content_checking' :
                    bool(supports_content_checking),
                'supports_keyword_checking' :
                    bool(supports_keyword_checking),
                'supports_post_method' :
                    bool(supports_post_method),
                'supports_latency_tracking' :
                    bool(supports_latency_tracking),
                'supports_ssl_expiration_checking' :
                    bool(supports_ssl_expiration_checking),
                'supports_ping_based_polling' :
                    bool(supports_ping_based_polling),
                'supports_blacklist_checking' :
                    bool(supports_blacklist_checking),
                'supports_domain_expiration_checking' :
                    bool(supports_domain_expiration_checking),
                'supports_maintenance_mode' :
                    bool(supports_maintenance_mode),
                'supports_rollups' :
                    bool(supports_rollups)
            }
        )

        if response is not None and 'status' in response:
            status = response['status']
            if status == 'OK' and 'customer' in response:
                result = self.__parse_response(response['customer'])
            else:
                result = None
        else:
            result = None

        return result


    def delete(self, customer):
        """
        Method you can use to delete a customer.  Note that deleting a customer
        will also delete all data associated with that customer.

        Use this method with care.

        :param customer:
            The customer to be deleted.

        :return:
            Returns true on success.  Returns false on error.

        :type customer: Customer
        :rtype:         bool

        """

        response = self.__rest_api.post_message(
            slug = "customer/delete",
            secret = self.__secret,
            message = { 'customer_id' : customer.customer_id }
        )

        result = (
                response is not None
            and 'status' in response
            and response['status'] == 'OK'
        )

        return result


    def purge(self, customers):
        """
        Method you can use to purge a list of customers by customer ID.  Note
        that deleting a customer will also delete all data associated with
        that customer.

        Use this method with care.

        :param customers:
            The list of customers to be deleted.  The list should contain the
            customer IDs.

        :return:
            Returns true on success.  Returns false on error.

        :type customers: list
        :rtype:          bool

        """

        response = self.__rest_api.post_message(
            slug = "customer/purge",
            secret = self.__secret,
            message = list(customers)
        )

        result = (
                response is not None
            and 'status' in response
            and response['status'] == 'OK'
        )

        return result


    def get_all(self):
        """
        Method you can use to obtain a list of all customers.

        :return:
            Returns a dictionary holding all customers indexed by customer ID.
            None is returned if an error occurs.

        :rtype: dict or None

        """

        response = self.__rest_api.post_message(
            slug = "customer/list",
            secret = self.__secret,
            message = { }
        )

        if response is not None and 'status' in response:
            status = response['status']
            if status == 'OK' and 'customers' in response:
                result = dict()
                customers_data = response['customers']
                for customer_id, customer_data in customers_data.items():
                    result[customer_id] = self.__parse_response(customer_data)
            else:
                result = None
        else:
            result = None

        return result


    def get_secret(self, customer_id):
        """
        Method you can use to obtain the secrets for a customer.

        :param customer_id:
            The customer ID of the customer in question.

        :return:
            Returns a tuple containing the customer identifier and customer
            secret.

        :type customer_id: int
        :rtype:            tuple or None

        """

        response = self.__rest_api.post_message(
            slug = "customer/get_secret",
            secret = self.__secret,
            message = { 'customer_id' : customer_id }
        )

        if response is not None and 'status' in response:
            status = response['status']
            if status == 'OK' and 'customer' in response:
                customer_data = response['customer']
                customer_identifier = customer_data['identifier']
                customer_secret_base64 = customer_data['secret']
                customer_secret = base64.b64decode(customer_secret_base64)

                result = ( customer_identifier, customer_secret )
            else:
                result = None
        else:
            result = None

        return result


    def reset_secret(self, customer_id):
        """
        Method you can use to reset the secrets for a customer.

        :param customer_id:
            The customer ID of the customer in question.

        :return:
            Returns a tuple containing the customer identifier and customer
            secret.

        :type customer_id: int
        :rtype:            tuple or None

        """

        response = self.__rest_api.post_message(
            slug = "customer/reset_secret",
            secret = self.__secret,
            message = { 'customer_id' : customer_id }
        )

        result = (
                response is not None
            and 'status' in response
            and response['status'] == 'OK'
        )

        return result


    def pause(self, customer_id, now_paused):
        """
        Method you can use to pause or resume customer polling.

        :param customer_id:
            The customer ID of the customer in question.

        :param now_paused:
            If True, then the customer's polling will be paused.  If False,
            then the customer's polling will be resumed.

        :return:
            Returns a tuple containing the customer identifier and customer
            secret.

        :type customer_id: int
        :rtype:            tuple or None

        """

        response = self.__rest_api.post_message(
            slug = "customer/pause",
            secret = self.__secret,
            message = {
                'customer_id' : customer_id,
                'pause' : now_paused
            }
        )

        result = (
                response is not None
            and 'status' in response
            and response['status'] == 'OK'
        )

        return result


    def __parse_response(self, response_data):
        """
        Method used internally to parse a response to generate a Customer
        instance.

        :param response_data:
            The response data to be parsed.

        :return:
            Returns the resulting Customer instance.

        :type response_data: dict
        :rtype:              Customer

        """

        try:
            customer_id = int(
                response_data['customer_id']
            )
            maximum_number_monitors = int(
                response_data['maximum_number_monitors']
            )
            polling_interval = int(
                response_data['polling_interval']
            )
#            expiration_days = int(
#                response_data['expiration_days']
#            )
            customer_active = bool(
                response_data['customer_active']
            )
            multi_region_checking = bool(
                response_data['multi_region_checking']
            )
            supports_wordpress = bool(
                response_data['supports_wordpress']
            )
            supports_rest_api = bool(
                response_data['supports_rest_api']
            )
            supports_content_checking = bool(
                response_data['supports_content_checking']
            )
            supports_keyword_checking = bool(
                response_data['supports_keyword_checking']
            )
            supports_post_method = bool(
                response_data['supports_post_method']
            )
            supports_latency_tracking = bool(
                response_data['supports_latency_tracking']
            )
            supports_ssl_expiration_checking = bool(
                response_data['supports_ssl_expiration_checking']
            )
            supports_ping_based_polling = bool(
                response_data['supports_ping_based_polling']
            )
            supports_blacklist_checking = bool(
                response_data['supports_blacklist_checking']
            )
            supports_domain_expiration_checking = bool(
                response_data['supports_domain_expiration_checking']
            )
            supports_maintenance_mode = bool(
                response_data['supports_maintenance_mode']
            )
            supports_rollups = bool(
                response_data['supports_rollups']
            )
            paused = bool(response_data['paused'])
        except:
            customer_id = None
            maximum_number_monitors = None
            polling_interval = None
#            expiration_days = None
            customer_active = None
            multi_region_checking = None
            supports_wordpress = None
            supports_rest_api = None
            supports_content_checking = None
            supports_keyword_checking = None
            supports_post_method = None
            supports_latency_tracking = None
            supports_ssl_expiration_checking = None
            supports_ping_based_polling = None
            supports_blacklist_checking = None
            supports_domain_expiration_checking = None
            supports_maintenance_mode = None
            supports_rollups = None
            paused = None

        if customer_id is not None:
            result = Customer(
                customer_id,
                maximum_number_monitors,
                polling_interval,
                0, # expiration_days,
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
                supports_rollups,
                paused
            )
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
