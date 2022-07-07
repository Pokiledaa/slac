from dataclasses import dataclass
from shutil import ExecError

from enums import ETH_TYPE_INSYS


@dataclass
class EthernetHeader:
    #  6 bytes (channel peer)
    dst_mac: bytes
    #  6 bytes (channel host)
    src_mac: bytes
    #  2 bytes (channel type)
    ether_type: int = ETH_TYPE_INSYS

    def __bytes__(self, endianess: str = "big")-> bytes:
        if endianess == "big":
            value = (self.dst_mac + self.src_mac + self.ether_type.to_bytes(2, "big") )
            return value
        return (
            self.ether_type.to_bytes(2, "little")
            + (int.from_bytes(self.src_mac, "big")).to_bytes(6, "little")
            + (int.from_bytes(self.dst_mac, "big")).to_bytes(6, "little")
        )

    def pack_big(self):
        return self.__bytes__()

    def pack_little(self):
        return self.__bytes__("little")

    @classmethod
    def from_bytes(cls, payload: bytes):
        return cls(
            dst_mac=payload[:6],
            src_mac=payload[6:12],
            ether_type=int.from_bytes(payload[12:14], "big"),
        )


@dataclass
class InsysPLCHeader :
   
    insys_type : int 
    reserve : bytes = b"\x00"

    def __bytes__(self, endianess: str = "big"):
        if endianess == "big":
            # The MMType is sent in little endian format
            return self.reserve +  self.insys_type.to_bytes(2, "big")
        else :
            pass

    def pack_big(self):
        return self.__bytes__()

    def pack_little(self):
        return self.__bytes__("little")

    


