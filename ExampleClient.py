"""
Description: Example echo client.
Author: Amol Kapoor
"""

import sys
from SocketWrapper import SocketWrapper


s = SocketWrapper(is_listener=False, socket_info=('localhost', 5000))

try:
    while True:
        message = raw_input("Input echo info.\n")
        s.send_data(message)
        print(s.get_message())
except KeyboardInterrupt:
    s.close_socket()
    sys.exit()
