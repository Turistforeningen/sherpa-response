import os
import socket
import json
import threading

class Listener(threading.Thread):
    def __init__(self, callback, *args, **kwargs):
        super(Listener, self).__init__(*args, **kwargs)
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind(("0.0.0.0", int(os.environ['UDP_PORT'])))
        self.callback = callback
        print("Listening for measurements on 0.0.0.0:%s" % os.environ['UDP_PORT'])

    def run(self):
        while True:
            data, addr = self.udp_socket.recvfrom(1024)
            data = json.loads(data)
            self.callback(data['path'], data['response_time'])
