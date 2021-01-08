# Copyright (c) 2021 Riverbed Technology, Inc.
#
# This software is licensed under the terms and conditions of the MIT License
# accompanying the software ("License").  This software is distributed "AS IS"
# as set forth in the License.


"""
This script presents a python example of using Command Line Interface (CLI)
to show version, networking state, current connections (flows) and bandwidth
statistics of a SteelHead appliance.
First of all, the steelhead module needs to be imported, from which the
SteelHead class is used. An authentication object is created by
instantiating the UserAuth class with user name and password to access the
SteelHead appliance. Afterwards, a SteelHead object is created by
instantiating the SteelHead class with the host name or IP address of the
SteelHead appliance and the existing authentication object. Then, we can use
the SteelHead object to execute command on the SteelHead appliance as follows:
steelhead_object.cli.exec_command("command_to_be_executed").
This example script should be executed as follows:
cac_rest_api.py <HOST> [-c access_code]
"""

from __future__ import (absolute_import, unicode_literals, print_function,
                        division)

import logging, sys
from steelscript.common.app import Application
from steelscript.common.service import OAuth
from steelscript.common import Service


class ClientAcceleratorControllerCLIApp(Application):
    def add_positional_args(self):
        self.add_positional_arg('host', 'Client Accelerator hostname or IP address')

    def add_options(self, parser):
        super(ClientAcceleratorControllerCLIApp, self).add_options(parser)

        parser.add_option('-c', '--oauth', help="access_code to connect to the api")

    def validate_args(self):
        super(ClientAcceleratorControllerCLIApp, self).validate_args()

        if not self.options.oauth:
            self.parser.error("Access_code needs to be specified")

    def main(self):
        
        cac = Service("appliance", self.options.host, auth=OAuth(self.options.oauth))

        print("\n********** Services **********\n")
        path = '/api/appliance/1.0.0/services'
        content_dict = cac.conn.json_request('GET', path)
        print(content_dict)

        print("\n********** License **********\n")
        path = '/api/appliance/1.0.0/status/license'
        content_dict=cac.conn.json_request('GET', path)
        print(content_dict)

        del cac

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    ClientAcceleratorControllerCLIApp().run()
