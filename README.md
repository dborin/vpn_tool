vpn_tool
========

appindicator for Linux for use with VPNC

This was testing using Ubuntu 14.04 (Trusty Tahr).  USE AT YOUR OWN RISK!

###SETUP

You'll need to create a configuration JSON file (I stick with `default.json`). It needs to be in the same directory as the vpn_tool.py file.

```
{
  "gateways": [
    {
      "name": "host1",
      "host": "vpn.host1.example.com" },
    {
      "name": "host2",
      "host": "vpn.host2.example.com" }
    ],
  "config_file": "/etc/vpnc/myconfig.conf",
  "image_directory": "/home/toks/vpn_tool/images",
  "disconnected_image": "lock_grey_open",
  "connected_image": "lock_red"
}
```

I had to install `gi` to get access to Gtk, AppIndicator3 and Glib.  Your mileage may vary depending upon your flavor of Linux.

###RUN

It is beyond the scope of this tool's documents to explain how to configure and run VPNC.  However, assuming you have it configured correctly:

`$ ./vpn_tool.py`

...should do the trick.

Feel free to email me borin8765+github at gmail dot com if you have questions.  Can't guarantee I'll be able to fix 'em since I'm pretty lost myself.
