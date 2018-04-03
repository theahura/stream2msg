"""
Description: Socket wrapper that handles basic message sending needs like length
limiting.
Author: Amol Kapoor
"""

import socket


class SocketWrapper(object):

    def __init__(self, is_listener, socket_info, socket=None):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if socket:
            self.socket = socket
        elif not is_listener:
            self.socket = s
            self.socket.connect(socket_info)
        else:
            s.bind(socket_info)
            s.listen(5)
            self.socket, address = s.accept()
            s.close()

    def send_data(self, data, metadata=[]):

        if type(data) != str:
            raise ValueError('Send data expects string data')

        data = '---'.join([str(md) for md in metadata]) + '---' + data

        if len(str(len(data))) > 10:
            raise ValueError('Data being sent is too large')

        data = str(len(data)) + '___' + data

        if len(data) < 10:
            raise ValueError('Data being sent is too small')

        try:
            self.socket.send(data)
        except Exception as e:
            print e
            self.close_socket()
            raise

    def close_socket(self):
        try:
            self.socket.send('10_killthread')
        except socket.error, e:
            print e
            pass
        self.socket.close()

    def get_message(self):
        data_str = self.socket.recv(10)

        if not data_str:
            return None

        message_size, data_str = data_str.split('___', 1)
        message_size = int(message_size)

        while len(data_str) < message_size:
            new_data = self.socket.recv(
                min(4096, message_size - len(data_str)))

            if not new_data:
                return None

            data_str += new_data

        if data_str == 'killthread':
            self.socket.close()
            return None

        if '---' in data_str:
            data = data_str.split('---')
        else:
            data = [data_str]

        return data
