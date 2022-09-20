import ctypes
from dataclasses import dataclass
from typing import List






@dataclass
class HC_LISTEN_CALC_RESULT :
    # EthernetHeader = 14Byte
    # Insys Header = 3Byte
    ev_mac : bytes
    run_id : bytes
    m_sounds : int
    attn : bytes

    @classmethod
    def from_bytes(cls,payload: ctypes) -> "HC_LISTEN_CALC_RESULT" :
        return cls(
            ev_mac = payload[17:22] ,
            run_id = payload[23:30] ,
            m_sounds = payload[31] ,
            attn = payload[33:91]  
        )



        

    

