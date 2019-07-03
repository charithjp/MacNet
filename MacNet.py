#!/usr/bin/env python

"""MacNet.py: Interface library to communicate with MacNet"""

__author__ = "Charith Perera"


import socket
import json


class MacNet:
    address = None
    port = None
    sock = None

    def __init__(self, address, port):
        # Error and authentication handling needed
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((address, port))

    def read_voltage(self, start_ch=0, read_num=1):
        tx_json = {
                        "jsonrpc": "2.0",
                        "method": "MacNet",
                        "params":
                        {
                            "FClass": 4,
                            "FNum": 2,
                            "Chan": start_ch,
                            "Len": read_num
                        },
                        "id": 1987
                    }
        rx_json = self._transact_json(tx=tx_json)
        if 'result' in rx_json:
            return rx_json["result"]["Voltage"]
        elif 'error' in rx_json:
            print("Error in read")
            return None

    def read_current(self, start_ch=0, read_num=1):
        tx_json = {
                        "jsonrpc": "2.0",
                        "method": "MacNet",
                        "params":
                        {
                            "FClass": 4,
                            "FNum": 3,
                            "Chan": start_ch,
                            "Len": read_num
                        },
                        "id": 1987
                    }
        rx_json = self._transact_json(tx=tx_json)
        if 'result' in rx_json:
            return rx_json["result"]["Current"]
        elif 'error' in rx_json:
            print("Error in read")
            return None

    def read_channel(self, channel=0):
        tx_json = {
                        "jsonrpc": "2.0",
                        "method": "MacNet",
                        "params":
                        {
                            "FClass": 4,
                            "FNum": 7,
                            "Chan": channel
                        },
                        "id": 1987
                    }
        rx_json = self._transact_json(tx=tx_json)
        if 'result' in rx_json:
            return rx_json["result"]
        elif 'error' in rx_json:
            print("Error in read")
            return None

    def _transact_json(self, tx=None, buf_size=10000):
        tx_int = str(tx).replace("'", '"')  # The Maccor is picky in what kind of quotes are used
        self.sock.sendall(tx_int.encode())  # Send the JSON string
        rx_int = self.sock.recv(buf_size)
        return json.loads(rx_int)


if __name__ == '__main__':
    conn = MacNet(address="192.168.133.194", port=57570)
    temp = conn.read_voltage(start_ch=0, read_num=24)
    print(temp)
    temp = conn.read_current(start_ch=0, read_num=24)
    print(temp)
    print(conn.read_channel(channel=23))
