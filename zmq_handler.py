import asyncio
import zmq
import zmq.asyncio
import logging
import pickle
from enums import (
    ModuleState,
)
from cp_handler import CPStates


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("COMM_Handler")



class ZMQHandler () :
    def __init__(
            self,
        ) -> None:

        self.context = zmq.asyncio.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:5555")
        self.rcv_msg: bytes = b"0"
        self.res_msg: bytes = b"0"

    async def zmq_recieve(self):

        self.rcv_msg = await self.socket.recv()
        return self.rcv_msg

    async def zmq_send (self, state: str, message, protocol: str = "slac"):

        dumped_msg = pickle.dumps (
            {
             "state": state,
             "message": message,
             "protocol": protocol,
            }
        )
        await self.socket.send(dumped_msg)


class CommunicationHandler (ZMQHandler) :
    def __init__(self) -> None:
        super().__init__()
        logger.info("Initilalizing <Comminucation Handler> Module")

    async def start (self) :
        # await self.zmq_send(b"slac")
        # module_state = await self.zmq_recieve()
        module_state = b"1"
        if module_state == b"1" :
            logger.info("SLAC MODULE CONNECTED TO GIRA CONTROLLER" )

        else :
            logger.info("WARNINGGGGGG" )


    async def infrom_controller_cp_state (self,cp_state : CPStates ) :
        logger.info( f"Informing Controller About The Cp State {cp_state}" )

    async def get_permision_for_digital_comm(self) :
        pass

    async def inform_slac_process(self,slac_state) :
        pass

    async def start_digital_comm (self) :
        pass

    async def get_cp_write_from_controller (self) :

        await self.zmq_send(state="initializing",message="cp_write")
        stream  = await self.zmq_recieve()
        dumped :dict = pickle.loads(stream)

        value = dumped.get("message")
        cp_value = pickle.loads(value)

        if isinstance(cp_value,CPStates) :
            return cp_value
        else :
            return CPStates.F








        # msg = stream.get("message")   
        # print(stream)






