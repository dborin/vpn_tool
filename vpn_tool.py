#!/usr/bin/env python

# Simple tool for having a GUI button to start VPNC and know if you're
# still connected.  Includes disconnect and quit options.

# Requires an 'images/' dir as a subdir of the same dir the script is
# running from.

# Assumes you've installed VPNC and it is working correctly. Quitting this
# tool WILL NOT automagically disconnect your VPNC connection (if present).
# Conversely, this tool WILL detect an already running VPNC instance and should
# be able to disconnect it.

# This was tested on Ubuntu 14.04 (Trusty Tahr).  Use at your own risk
import argparse
import json
import os
import re
import sys
import subprocess

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import GLib as glib

PING_FREQUENCY = 10 # seconds

class VPNTool:
    def __init__(self, config_data):
        self.config_data = config_data
        self.ind = appindicator.Indicator.new_with_path('vpn_status',
                                              'VPN Status Indicator',
                                              appindicator.IndicatorCategory.APPLICATION_STATUS,
                                              os.path.join(os.getcwd(), 'images'))
        self.ind.set_title("VPN Status Indicator")
        self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.ind.set_icon_full(self.config_data['disconnected_image'], "VPN Status Indicator")
        self.ind.set_attention_icon(self.config_data['connected_image'])
        self.ind.get_title()

        self.menu_setup()
        self.ind.set_menu(self.menu)

    def menu_setup(self):
        self.menu = gtk.Menu()
        for gateway in self.config_data['gateways']:
            menu_item = gtk.MenuItem('Connect - %s' % gateway['name'])
            menu_item.connect('activate', self.on_click, gateway['host'])
            menu_item.show()
            self.menu.append(menu_item)

        self.on_disconnect = gtk.MenuItem('Disconnect')
        self.on_disconnect.connect('activate', self.off_click)
        self.on_disconnect.show()
        self.menu.append(self.on_disconnect)

        self.quit_item = gtk.MenuItem('Quit')
        self.quit_item.connect('activate', self.quit)
        self.quit_item.show()
        self.menu.append(self.quit_item)

    def main(self):
        self.check_vpn()
        glib.timeout_add_seconds(PING_FREQUENCY, self.check_vpn)
        gtk.main()

    def quit(self, widget):
        sys.exit(0)

    def on_click(self, widget, gateway):
        self.vpn_connect(gateway)

    def off_click(self, widget):
        self.vpn_disconnect()

    def vpn_connect(self, gateway):
        command = ['xterm', '-e', "sudo vpnc-connect --gateway %s" % gateway]
        subprocess.call(command)

    def vpn_disconnect(self):
        command = ['xterm', '-e', "sudo vpnc-disconnect"]
        subprocess.call(command)

    def check_vpn(self):
        is_vpn = self.vpn_checker()
        if is_vpn:
            self.ind.set_status(appindicator.IndicatorStatus.ATTENTION)
        else:
            self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
        return True

    def vpn_checker(self):
        vpn_found = False

        if os.path.isfile('/var/run/vpnc/pid'):
            pid_file = open('/var/run/vpnc/pid')
            pid = pid_file.read().rstrip()
            pid_file.close()
        else:
            pid = ''

        command = ['/bin/ps', '-e', '-f']
        search_string = 'root.*%s.*vpnc' % pid
        currently_running = subprocess.check_output(command)
        if re.search(search_string, currently_running):
            vpn_found = True

        return vpn_found

def read_config(filename):
    json_data = open(filename)
    return json.load(json_data)

def options():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--conf', dest='config', default='default.json',
            help="relative or absolute path to .json file (default: %(default)s)")
    return parser.parse_args()

if __name__ == "__main__":
    args = options()
    config_data = read_config(args.config)
    indicator = VPNTool(config_data)
    indicator.main()
