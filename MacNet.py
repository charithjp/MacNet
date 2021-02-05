#!/usr/bin/env python

"""MacNet.py: Interface library to communicate with MacNet"""

__author__ = "Charith Perera"

import socket
import json


class MacNet:
    address = None
    port = None
    sock = None

    # This isn't used for anything yet but could be handy to track?
    comm_error_counter = 0

    def __init__(self, address, port):
        # Error and authentication handling needed
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((address, port))

    def read_voltage(self, start_ch, read_num=1):
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
        rx_json = self._transact_json(tx=tx_json, param_matching=["FClass", "FNum", "Chan", "Len"])
        if 'result' in rx_json:
            return rx_json["result"]["Voltage"]
        elif 'error' in rx_json:
            print("Error in read")
            return None

    def read_current(self, start_ch, read_num=1):
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
        rx_json = self._transact_json(tx=tx_json, param_matching=["FClass", "FNum", "Chan", "Len"])
        if 'result' in rx_json:
            return rx_json["result"]["Current"]
        elif 'error' in rx_json:
            print("Error in read")
            return None

    def read_aux(self, channel):
        tx_json = {
                        "jsonrpc": "2.0",
                        "method": "MacNet",
                        "params":
                        {
                            "FClass": 4,
                            "FNum": 4,
                            "Chan": channel
                        },
                        "id": 1987
                    }
        rx_json = self._transact_json(tx=tx_json, param_matching=["FClass", "FNum", "Chan"])
        if 'result' in rx_json:
            return rx_json["result"]
        elif 'error' in rx_json:
            print("Error in read")
            return None

    def read_file_procedure_comment(self, channel):
        tx_json = {
                        "jsonrpc": "2.0",
                        "method": "MacNet",
                        "params":
                        {
                            "FClass": 4,
                            "FNum": 6,
                            "Chan": channel
                        },
                        "id": 1987
                    }
        rx_json = self._transact_json(tx=tx_json, param_matching=["FClass", "FNum", "Chan"])
        if 'result' in rx_json:
            return rx_json["result"]
        elif 'error' in rx_json:
            print("Error in read")
            return None

    def read_channel(self, channel):
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
        rx_json = self._transact_json(tx=tx_json, param_matching=["FClass", "FNum", "Chan"])
        if 'result' in rx_json:
            return rx_json["result"]
        elif 'error' in rx_json:
            print("Error in read")
            return None

    def smb_read_status(self, channel):
        tx_json = {
                        "jsonrpc": "2.0",
                        "method": "MacNet",
                        "params":
                        {
                            "FClass": 7,
                            "FNum": 1,
                            "Chan": channel
                        },
                        "id": 1987
                    }
        rx_json = self._transact_json(tx=tx_json, param_matching=["FClass", "FNum", "Chan"])
        if 'result' in rx_json:
            return rx_json["result"]
        elif 'error' in rx_json:
            print("Error in read")
            return None

    def smb_read_from_scanlist(self, channel, address, value=True):
        tx_json = {
                        "jsonrpc": "2.0",
                        "method": "MacNet",
                        "params":
                        {
                            "FClass": 7,
                            "FNum": 4,
                            "Chan": channel,
                            "SMBRegAddr": address

                        },
                        "id": 1987
                    }
        rx_json = self._transact_json(tx=tx_json)
        if 'result' in rx_json:
            if value:
                return rx_json["result"]["SMBRegValue"]
            else:
                return rx_json["result"]
        elif 'error' in rx_json:
            print("Error in read")
            return None

    def _decode_RF1(self, rf_1):
        rf1_lookup = {0: "Available",
                      1: "Charge",
                      2: "Discharge",
                      3: "AdvCycle",
                      4: "Rest",
                      5: "Pause",
                      7: "End",
                      8: "Ext_Chg",
                      9: "Ext_Dis",
                      19: "Pls_Chg",
                      20: "Pls_Dis",
                      21: "IO_Out",
                      22: "EnvChambr_and_FRA",
                      23: "Scan",
                      26: "SubRout",
                      29: "Problem",
                      30: "Suspended",
                      31: "Complete"
                     }

        try:
            return rf1_lookup[rf_1]
        except:
            return "UNKNOWN RF1"

    def _decode_RF2(self, rf_2):
        rf2_lookup = {0: "Start_Of_Step",
                      1: "Step_Time",
                      4: "Current_Increment",
                      5: "Voltage_Increment",
                      8: "Amp_Hour",
                      9: "Watt_Hour",
                      17: "Pause_Step",
                      18: "Auxiliary_Input",
                      33: "Pulse_Low",
                      34: "Pulse_High",
                      37: "Digital_Input",

                      128: "None",
                      129: "Step_Time",
                      130: "Test_Time",
                      131: "Cycle_Number",
                      132: "Current",
                      133: "Voltage",
                      134: "Power",
                      135: "Resistance",
                      136: "Amp_Hour",
                      137: "Watt_Hour",
                      138: "Half_Cycle_Ahr",
                      139: "Half_Cycle_Whr",
                      140: "Previous_Ahr",
                      141: "Previous_Whr",
                      142: "First_Half_Cycle_Ahr",

                      143: "First_Half_Cycle_Whr",
                      144: "Last_Half_Cycle_Ahr",
                      145: "Last_Half_Cycle_Whr",
                      146: "External",
                      147: "Loop_Count",
                      150: "Voltage-Hour",
                      151: "Ahr_Previous",
                      152: "Half_Cycle_Ahr",
                      153: "Half_Cycle_Time",
                      154: "Delta_I",
                      155: "Delta_V",
                      157: "Aux_Volt",
                      158: "Thermocouple",
                      159: "Thermistor",
                      160: "Pressure",
                      161: "Max-Deviation",
                      162: "Mean-Deviation",
                      163: "SMBus_Alarm",
                      164: "Function",
                      165: "Digital_Input",
                      189: "Safety_Capacity",
                      190: "Safety_Voltage",
                      191: "Safety_Overcharge",
                      192: "Suspend_Or_Pause",

                      193: "Normal_End",
                      194: "Timeout_Fault",
                      195: "Timeout_Fault",
                      196: "Overcharge_Safety",
                      197: "Voltage_Safety",
                      198: "Slave_Error",
                      199: "Operator_Forced_Step",
                      252: "Slave_Current_Control_Error",
                      253: "Safety_Absolute",
                      254: "Lost_Current_Control",
                      255: "Buffer_Full"
                      }
        try:
            return rf2_lookup[rf_2]
        except:
            return "UNKNOWN RF2"

    def _transact_json(self, tx=None, buf_size=10000, param_matching=None, retries=3):
        # Parameter matching is to make sure the Parameters that are passed in return the same, otherwise we didn't get
        # the type of return we are expecting from the Maccor.))
        tx_int = str(tx).replace("'", '"')  # The Maccor is picky in what kind of quotes are used
        tx_json = json.loads(tx_int)

        # If we get parameters to match, we match by recursing without parameters and verifying if we match.
        # If we match, return, otherwise increment the comm_error_counter
        if type(param_matching) is list:
            for i in range(retries):
                try:
                    rx_json = self._transact_json(tx=tx, buf_size=buf_size, param_matching=None, retries=0)
                    #print([tx_int, rx_json])
                    for each in param_matching:
                        assert(tx_json["params"][each] == rx_json['result'][each])
                        #print([each, tx_json["params"][each], rx_json['result'][each]])

                    return rx_json

                except:
                    print("Comm Error")
                    self.comm_error_counter = self.comm_error_counter + 1

        else:
            self.sock.sendall(tx_int.encode())  # Send the JSON string
            rx_int = self.sock.recv(buf_size)
            decoded_json_dict = json.loads(rx_int.decode('utf-8'))

            return decoded_json_dict


if __name__ == '__main__':
    import time

    Maccor_IP = "192.168.63.145"
    ch = 1
    conn = MacNet(address=Maccor_IP, port=57570)

    print(conn.read_file_procedure_comment(channel=ch))
    ch_read = conn.read_channel(channel=ch)
    print(ch_read)
    print("RF1 Status = " + conn._decode_RF1(ch_read['RF1']))
    print("RF2 Status = " + conn._decode_RF2(ch_read['RF2']))
