from abc import ABC
import asyncio
from binascii import hexlify
from dataclasses import dataclass
import enum
from typing import List, Union
from enum import Enum, IntEnum
from inspect import isawaitable
from unittest import result
from sockets.async_linux_socket import (
    create_socket,
    readeth,
    send_recv_eth,
    sendeth,
)
from utils import (
    get_if_hwaddr
)
from  enums import(
    Timers,
    ETH_TYPE_INSYS
) 

from layer_2_headers import(
    EthernetHeader,
    InsysPLCHeader,
)
import logging

from messages import (
    HC_LISTEN_CALC_RESULT,

)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("slac_session")

EVSE_PLC_MAC = b"\x00\x05\xB6\x0A\xF1\xF9"

SLAC_ASS_START = 0x0b01


class InsysCmdType(IntEnum) :
    SLAC_ASS_START = 0x0b01
    TERM_D_LINK = 0x0b07
    SLAC_ASS_STOP = 0x0b03

class Timouts(IntEnum) :
    WAIT_HC_STOP_LISTEN_FOR_SLAC_ASSN_CNF = 5
    WAIT_D_LINK_READY_IND = 7
    WAIT_HC_START_LISTEN_FOR_SLAC_ASSN_CNF = 5
    WAIT_SEQUENCE = 5
    WAIT_SLAC_INIT = 10
    













class SlacEvseSession () : 

    def __init__(self, evse_id: str, iface: str):
        self.iface = iface
        self.evse_id = evse_id
        
        host_mac = get_if_hwaddr(self.iface)
        self.socket = create_socket(iface=self.iface, port=0)
        self.evse_plc_mac = EVSE_PLC_MAC
        self.evse_mac = host_mac

        self.ev_mac : bytes = None
        
        self.run_id : bytes = None

        logger.info("Initilalizing <SLAC Handler> Module")


    async def send_frame(self, frame_to_send: bytes) -> None:
        """
        Async wrapper for a sendeth that checks if sendeth is an awaitable
        """
        # TODO: Add this to a send method
        bytes_sent = sendeth(
            s=self.socket, frame_to_send=frame_to_send, iface=self.iface
        )
        if isawaitable(bytes_sent):
            await bytes_sent

        
    async def rcv_frame(self, rcv_frame_size: int, timeout: Union[float, int]) -> bytes:
        """
        Helper function to diminush the lines of code when calling the
        asyncio.wait_for with readeth

        :param rcv_frame_size: size of the frame to be received
        :param timeout: timeout for the specific message that is being expected
        :return:
        """
        return await asyncio.wait_for(
            readeth(self.socket, self.iface, rcv_frame_size),
            timeout,
        )

    async def insys_type_indicator (self , type_to_check:bytes) :
        pass

    async def evse_start_slac_association (self) -> bool:
        """
        TODO : Write The Documentation
        Step 1 : Creating Ethrenet Header
        Step 2 : Creating The Insys PLC Header
        
        """
        err = False
        sequence_state = 0
        logger.info("Running The Start Slac Association Handle")
        eth_header = EthernetHeader (
            dst_mac= self.evse_plc_mac,
            src_mac= self.evse_mac,
        ) 

        insys_header  = InsysPLCHeader(SLAC_ASS_START)
        slac_start_ass_payload = bytes(58)

        frame = (
            eth_header.pack_big()
            + insys_header.pack_big()
            + slac_start_ass_payload
        )
        await self.send_frame(frame)

        while True:
            if sequence_state == 0 :
                try:
                    data_rcvd = await self.rcv_frame(
                        rcv_frame_size=60,
                        timeout=Timouts.WAIT_SLAC_INIT,
                    )

                except asyncio.TimeoutError as e:
                    # raise TimeoutError("SLAC Association Start Confirmation Timeout raised") from e
                    logger.info("SLAC Association Start Confirmation Timeout raised")
                    err = True
                    break

                if data_rcvd[15] == 0x0b and data_rcvd[16]== 0x02 :
                    
                    if data_rcvd[17] == 0:
                        logger.info("SLAC Start association Confirmation : <failure>")
                        err = True
                        # TODO : Think about What if is Failure What Seuqence should Procced

                    elif data_rcvd[17] == 1:
                        logger.info("SLAC Start Association Confirmation : <Succesfull>")
                        sequence_state = 1

            elif sequence_state == 1 :
                try :
                    data_rcvd = await self.rcv_frame(
                        rcv_frame_size=60,
                        timeout=Timouts.WAIT_SLAC_INIT,
                    )
                    

                except asyncio.TimeoutError as e:
                    # raise TimeoutError("SLAC ASSOCIATION START Timeout raised") from e
                    logger.info("SLAC ASSOCIATION START Timeout raised")
                    err = True
                    break
                
                if data_rcvd[15] == 0x0b and data_rcvd[16]== 0x0c :
                    sequence_state = 2

            elif sequence_state == 2:
                try :
                    data_rcvd = await self.rcv_frame(
                        rcv_frame_size=92,
                        timeout=Timouts.WAIT_SLAC_INIT,
                    )

                except asyncio.TimeoutError as e:
                    # raise TimeoutError("SLAC Listen Calculation Timeout raised") from e
                    logger.info("SLAC Listen Calculation Timeout raised")
                    err = True
                    break

                if data_rcvd[15] == 0x0b and data_rcvd[16]== 0x05 :
                    payload = HC_LISTEN_CALC_RESULT.from_bytes(data_rcvd)
                    print( hexlify(payload.ev_mac) )
                    print( hexlify (payload.run_id))
                    sequence_state = 3

            elif sequence_state == 3:
                try :
                    data_rcvd = await self.rcv_frame(
                        rcv_frame_size=60,
                        timeout=Timouts.WAIT_SLAC_INIT,
                    )

                except asyncio.TimeoutError as e:
                    # raise TimeoutError("SLAC D_Link Recive Status Timout") from e
                    logger.info("SLAC D_Link Recive Status Timout")
                    err = True
                    break

                if data_rcvd[15] == 0x0b and data_rcvd[16] == 0x06:
                    
                    if data_rcvd[17] == 0:
                        logger.info("SLAC D_Link Established : <Link Established> ")
                        break

                    elif data_rcvd[17] == 1:
                        logger.info("SLAC D_Link Established : <No Link>")
                        err = True
                        break
                        # TODO : Think about What if is Failure What Sequence should Procced

        return err

    async def terminating_data_link(self) -> bool:

        logger.info("Running The Terminating Data Link Handle")
        eth_header = EthernetHeader (
            dst_mac= self.evse_plc_mac,
            src_mac= self.evse_mac,
        ) 

        insys_header  = InsysPLCHeader(InsysCmdType.TERM_D_LINK)
        terminate_datalink_frame = bytes(59)

        frame = (
            eth_header.pack_big()
            + insys_header.pack_big()
            + terminate_datalink_frame
        )
        await self.send_frame(frame)
        while True :
            try :
                data_rcvd = await self.rcv_frame(
                    rcv_frame_size=60,
                    timeout=Timers.SLAC_INIT_TIMEOUT,
                )

            except asyncio.TimeoutError as e:
                raise TimeoutError("SLAC ASSOCIATION START Timeout raised") from e

            if data_rcvd[15] == 0x0b and data_rcvd[16]== 0x08 :
                
                if data_rcvd[17] == 0 :
                    logger.info("Termiation Request Has been done succesfully")
                    break

                elif data_rcvd[17] == 1 :
                    logger.info("Termination ERROR")

            print(data_rcvd)

    async def evse_stop_slac_association (self) :
        sequence_state = 0
        err = False

        logger.info("Running The Stop Slac Association Handle")
        eth_header = EthernetHeader (
            dst_mac= self.evse_plc_mac,
            src_mac= self.evse_mac,
        ) 

        insys_header = InsysPLCHeader(InsysCmdType.SLAC_ASS_STOP)
        slac_stop_ass_payload = b"\x00"

        frame = (
            eth_header.pack_big()
            + insys_header.pack_big()
            + slac_stop_ass_payload
        )
        await self.send_frame(frame)
        while True:

            if sequence_state == 0 :
                try :
                    data_rcvd = await self.rcv_frame(
                        rcv_frame_size=60,
                        timeout=Timouts.WAIT_HC_STOP_LISTEN_FOR_SLAC_ASSN_CNF,
                    )

                except asyncio.TimeoutError as e:
                    # raise TimeoutError("Timout In Confirmation Response of Stop Slac Association") from e
                    logger.info("Timout In Confirmation Response of Stop Slac Association")
                    err = True
                    break
                
                if data_rcvd[15] == 0x0b and data_rcvd[16]== 0x04 :
                
                    if data_rcvd[17] == 0:
                        logger.info("Slac Stop :failure")
                        err = True
                        break
                    elif data_rcvd[17] == 1:
                        logger.info("Slac Stop :success")
                        sequence_state = 1
                    elif data_rcvd[17] == 2:
                        logger.info("System State is already unoccupied")

            elif sequence_state == 1:

                try:
                    data_rcvd = await self.rcv_frame(
                        rcv_frame_size=60,
                        timeout=Timouts.WAIT_D_LINK_READY_IND,
                    )

                except asyncio.TimeoutError as e:
                    # raise TimeoutError("Timout In Confirmation Response of Data Link  No link") from e
                    logger.info("Timout In Confirmation Response of Data Link  No link")
                    err = True
                    break

                if data_rcvd[15] == 0x0b and data_rcvd[16] == 0x06:
                
                    if data_rcvd[17] == 1:
                        logger.info("Data Link  :No Link ")
                        err = True
                        break
                    else:
                        pass
        return err


class SlacSessionHandler(SlacEvseSession):
    def __init__(self, evse_id: str, iface: str):
        super().__init__(evse_id, iface)


                   




            


                






        

