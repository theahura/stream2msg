"""
Description: Example echo server.
Author: Amol Kapoor
"""

import sys
import SocketWrapper as sw


s = sw.SocketWrapper(is_listener=True, socket_info=('localhost', 5001))

try:
    while True:
        message = s.get_message()
        print message
        s.send_data(message[-1])
except KeyboardInterrupt:
    s.close_socket()
    sys.exit()
