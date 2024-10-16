from scapy.all import *

# Defining the custom protocol
class CustomProtocol(Packet):
    name = "CustomProtocol"
    fields_desc = [ByteField("type", 0), ShortField("length", 0), StrField("data", "")]

# Creating a packet using the custom protocol
packet = CustomProtocol(type=1, length=4, data="custom protocol packet")
packet.show()
