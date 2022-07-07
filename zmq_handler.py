import asyncio
import zmq
import zmq.asyncio
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("COMM_Handler")



class ZMQHandler () :
    def __init__(
            self,
        ) -> None:

        self.context = zmq.asyncio.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:5556")
        self.rcv_msg : bytes = None
        

        self.res_msg : bytes = None
        


    async def rcv_loop (self,queue : asyncio.Queue ) :
        while (True) :
            self.rcv_msg= await self.socket.recv()
            try :
                queue.put_nowait(self.rcv_msg)
            except asyncio.QueueFull :
                await queue.put(self.rcv_msg)
            
           

    async def send_response (self,response : bytes) :

        await self.socket.send(response)



class CommunicationHandler (ZMQHandler) :
    def __init__(self) -> None:
        super().__init__()

        logger.info("Initilalizing <Comminucation Handler> Module")



    


    async def infrom_controller_cp_state (self) :
        pass
