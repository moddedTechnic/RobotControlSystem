"""Utilities relating to the currently connected network"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = ['get_ssid']

import subprocess
import sys
from typing import Callable


class InvalidNetworkException(Exception):
    """An invalid network was detected"""


if sys.platform == 'win32':
    def get_ssid() -> str:
        """Get the ssid of the current network"""
        current_network = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces']).decode('utf-8').split('\n')
        ssid_line = [x.strip() for x in current_network if 'SSID' in x and 'BSSID' not in x]
        if not ssid_line:
            raise InvalidNetworkException
        ssid_list = ssid_line[0].split(':')
        connected_ssid = ssid_list[1].strip()
        return connected_ssid

else:
    def get_ssid() -> str:
        """Get the ssid of the current network"""
        raise OSError(f'The current platform ({sys.platform}) is not supported')
