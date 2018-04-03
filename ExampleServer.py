"""
Description: Example echo server.
Author: Amol Kapoor
"""

import sys
from SocketWrapper import SocketWrapper


s = SocketWrapper(is_listener=True, socket_info=('localhost', 5000))

try:
    while True:
        message = s.get_message()
        print message
        s.send_data(message[-1])
except KeyboardInterrupt:
    s.close_socket()
    sys.exit()
