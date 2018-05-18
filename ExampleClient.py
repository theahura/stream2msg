"""
Description: Example echo client.
Author: Amol Kapoor
"""

import sys
from stream2msg import SocketWrapper


s = SocketWrapper(is_listener=False, socket_info=('localhost', 5001))

try:
    while True:
        message = raw_input("Input echo info.\n")
        s.send_data(message)
        print(s.get_message())
except KeyboardInterrupt:
    s.close_socket()
    sys.exit()
