"""
Description: Socket wrapper that handles basic message sending needs like length
limiting.
Author: Amol Kapoor
"""

import socket


class SocketWrapper(object):
    """Wrapper for low level socket that handles sending/receiving messages."""

    def __init__(self, is_listener, socket_info, user_socket=None):
        """Initializes a socket wrapper.

        @param is_listener: bool, socket is a listener if true.
        @param socket_info: (ip, port)
        @param socket: a user-defined socket for custom socket behaviors.
        """
        self.closed = False
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if user_socket:
            self.socket = user_socket
        elif not is_listener:
            self.socket = s
            self.socket.connect(socket_info)
        else:
            s.bind(socket_info)
            s.listen(5)
            self.socket, address = s.accept()
            s.close()

    def send_data(self, data, metadata=[]):
        """Sends string data through socket.

        Tags data with length. Metadata is tagged in front as strings. Typing
        needs to be tracked by the user on the receiving end."""

        if self.closed:
            raise SystemError('Socket closed')

        if type(data) != str:
            raise ValueError('Send data expects string data')
        data = '---'.join([str(md) for md in metadata]) + '---' + data
        data = str(len(data)) + '___' + data

        try:
            self.socket.send(data)
        except Exception as e:
            print e
            self.close_socket()
            raise

    def close_socket(self):
        """Closes the socket and attempts to notify other socket of close."""
        self.closed = True
        self.socket.close()

    def get_message(self):
        """Gets a message.

        Grabs the first 10 chars to get length of the message, then gets the
        rest. Returns an array with metadata in front and the data in the last
        index."""
        if self.closed:
            raise SystemError('Socket closed')

        data_str = ''
        while '___' not in data_str:
            new_data_str = self.socket.recv(1)
            if not new_data_str:
                self.close_socket()
                return None
            data_str += new_data_str
        message_size, data_str = data_str.split('___', 1)
        message_size = int(message_size)
        while len(data_str) < message_size:
            new_data = self.socket.recv(
                min(4096, message_size - len(data_str)))
            if not new_data:
                self.close_socket()
                return None
            data_str += new_data
        if '---' in data_str:
            data = data_str.split('---')
        else:
            data = [data_str]
        return data
